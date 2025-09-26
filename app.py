from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from groq import Groq
import base64
import os
import json
import geopandas as gpd
from shapely.geometry import Polygon
import glob
from typing import Dict, List
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = FastAPI(title="GeoData Analysis API", description="API pour analyser les coordonnées et couches géographiques")

# Configuration Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found! Please:\n"
        "1. Add GROQ_API_KEY=your_api_key to your .env file, or\n"
        "2. Set the environment variable: export GROQ_API_KEY='your_api_key'"
    )

client = Groq(api_key=GROQ_API_KEY)

def encode_image_from_bytes(image_bytes: bytes) -> str:
    """Encode image bytes to base64 string"""
    return base64.b64encode(image_bytes).decode("utf-8")

def extract_coordinates_from_image(image_bytes: bytes) -> List[Dict[str, float]]:
    """Extract coordinates from image using Groq Vision API"""
    base64_image = encode_image_from_bytes(image_bytes)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Extract ONLY the coordinates from the top-left table labeled 'COORDONNEES'. "
                                "Ignore everything else on the image. "
                                "Return the result strictly as a JSON list of objects with 'x' and 'y' keys, "
                                "like this: "
                                "[{\"x\": 401354.03, \"y\": 712401.54}, {\"x\": 401247.82, \"y\": 712353.35}]. "
                                "Make sure to return ONLY valid JSON, no other text."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0,
            max_tokens=512,
        )
        
        coords_text = chat_completion.choices[0].message.content.strip()
        
        # Clean the response to extract only JSON
        if coords_text.startswith("```json") and coords_text.endswith("```"):
            coords_text = coords_text[7:-3].strip()
        elif coords_text.startswith("```") and coords_text.endswith("```"):
            coords_text = coords_text[3:-3].strip()
        
        coordinates = json.loads(coords_text)
        return coordinates
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting coordinates: {str(e)}")

def get_all_geojson_layers() -> Dict[str, str]:
    """Get all GeoJSON layer files and their normalized names"""
    layers = {}
    geojson_files = glob.glob("couche/*.geojson")
    
    for file_path in geojson_files:
        # Extract layer name from filename
        layer_name = os.path.basename(file_path).replace('.geojson', '')
        # Normalize name (replace spaces with underscores)
        normalized_name = layer_name.replace(' ', '_')
        layers[normalized_name] = file_path
    
    return layers

def check_polygon_intersections(coordinates: List[Dict[str, float]]) -> Dict[str, str]:
    """Check if polygon intersects with all available GeoJSON layers"""
    if len(coordinates) < 3:
        raise HTTPException(status_code=400, detail="Need at least 3 coordinates to form a polygon")
    
    # Create polygon from coordinates
    try:
        polygon_coords = [(coord["x"], coord["y"]) for coord in coordinates]
        poly = Polygon(polygon_coords)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid coordinates for polygon: {str(e)}")
    
    layers = get_all_geojson_layers()
    results = {}
    
    for layer_name, file_path in layers.items():
        try:
            # Load GeoJSON file
            gdf = gpd.read_file(file_path)
            
            # Check intersection
            intersection_found = gdf["geometry"].apply(
                lambda g: g.intersects(poly) or g.contains(poly) or poly.contains(g)
            ).any()
            
            results[layer_name] = "OUI" if intersection_found else "NON"
            
        except Exception as e:
            print(f"Error processing layer {layer_name}: {str(e)}")
            results[layer_name] = "NON"  # Default to NON if error
    
    return results

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded image to extract coordinates and check intersections with GeoJSON layers
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Extract coordinates from image
        coordinates = extract_coordinates_from_image(image_bytes)
        
        # Check intersections with all layers
        textual_data = check_polygon_intersections(coordinates)
        
        # Return response in requested format
        response = {
            "textualData": textual_data,
            "coordinates": coordinates
        }
        
        return JSONResponse(content=response)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/layers")
async def get_available_layers():
    """Get list of available GeoJSON layers"""
    layers = get_all_geojson_layers()
    return {"layers": list(layers.keys())}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "GeoData Analysis API is running"}

# Test endpoint for local images
@app.post("/analyze-local-image/{image_name}")
async def analyze_local_image(image_name: str):
    """
    Analyze a local image from the images/ directory
    """
    image_path = f"images/{image_name}"
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found in images/ directory")
    
    try:
        # Read image file
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        
        # Extract coordinates from image
        coordinates = extract_coordinates_from_image(image_bytes)
        
        # Check intersections with all layers
        textual_data = check_polygon_intersections(coordinates)
        
        # Return response in requested format
        response = {
            "textualData": textual_data,
            "coordinates": coordinates
        }
        
        return JSONResponse(content=response)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
