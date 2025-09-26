#!/usr/bin/env python3
"""
Script de test pour l'API GeoData Analysis
"""

import requests
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test l'endpoint de santé"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_layers():
    """Test l'endpoint des couches"""
    try:
        response = requests.get(f"{API_BASE_URL}/layers")
        layers = response.json()["layers"]
        print(f"✅ Layers found: {len(layers)} couches")
        for layer in layers:
            print(f"   - {layer}")
        return True
    except Exception as e:
        print(f"❌ Layers test failed: {e}")
        return False

def test_local_image(image_name):
    """Test l'analyse d'une image locale"""
    try:
        response = requests.post(f"{API_BASE_URL}/analyze-local-image/{image_name}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis of {image_name}:")
            print(f"   Coordinates: {len(result['coordinates'])} points")
            print("   Intersections:")
            for layer, status in result['textualData'].items():
                print(f"     {layer}: {status}")
            return True
        else:
            print(f"❌ Analysis of {image_name} failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Analysis of {image_name} failed: {e}")
        return False

def test_upload_image(image_path):
    """Test l'upload et l'analyse d'une image"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/analyze-image", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload analysis of {Path(image_path).name}:")
            print(f"   Coordinates: {len(result['coordinates'])} points")
            print("   Intersections:")
            for layer, status in result['textualData'].items():
                print(f"     {layer}: {status}")
            return True
        else:
            print(f"❌ Upload analysis failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload analysis failed: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Tests de l'API GeoData Analysis")
    print("=" * 50)
    
    # Test de santé
    if not test_health():
        print("❌ L'API n'est pas accessible. Assurez-vous qu'elle est lancée.")
        return
    
    print()
    
    # Test des couches
    test_layers()
    print()
    
    # Test des images locales
    images_dir = Path("images")
    if images_dir.exists():
        image_files = list(images_dir.glob("*"))
        print(f"📁 Testing {len(image_files)} images from images/ directory:")
        
        for image_file in image_files:
            if image_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                print(f"\n🔍 Testing local image: {image_file.name}")
                test_local_image(image_file.name)
                
                print(f"\n📤 Testing upload: {image_file.name}")
                test_upload_image(str(image_file))
    else:
        print("❌ Directory images/ not found")

if __name__ == "__main__":
    main()