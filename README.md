# GeoData Analysis API

API FastAPI pour analyser des images de levé topographique et vérifier les intersections avec les couches géographiques.

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Une clé API Groq (pour l'extraction des coordonnées depuis les images)

### Installation

1. **Cloner et naviguer vers le projet**
```bash
cd "/Users/mac/Documents/Projet Python/hackathon"
```

2. **Configurer l'environnement**
```bash
# Rendre le script de setup exécutable
chmod +x setup.sh

# Lancer le script de configuration
./setup.sh
```

3. **Configurer la clé API Groq**
```bash
export GROQ_API_KEY='votre_clé_api_groq_ici'
```

### Lancement de l'API

```bash
python3 app.py
```

L'API sera accessible sur : http://localhost:8000
Documentation interactive : http://localhost:8000/docs

## 📖 Endpoints

### POST /analyze-image
Analyse une image uploadée pour extraire les coordonnées et vérifier les intersections.

**Paramètres :**
- `file` : Image à analyser (PNG, JPG, JPEG)

### POST /analyze-local-image/{image_name}
Analyse une image depuis le dossier `images/`.

**Paramètres :**
- `image_name` : Nom du fichier image dans le dossier `images/`

### GET /layers
Retourne la liste des couches GeoJSON disponibles.

### GET /health
Vérifie l'état de l'API.

## 📊 Format de Réponse

```json
{
    "textualData": {
        "aif": "NON",
        "air_proteges": "NON", 
        "dpl": "NON",
        "dpm": "NON",
        "enregistrement_individuel": "OUI",
        "litige": "NON",
        "parcelles": "OUI",
        "restriction": "OUI",
        "tf_demembres": "NON",
        "tf_en_cours": "NON",
        "tf_etat": "NON",
        "titre_reconstitue": "NON",
        "zone_inondable": "NON"
    },
    "coordinates": [
        { "x": 321562.2, "y": 1135517.34 },
        { "x": 321590.39, "y": 1135506.9 },
        { "x": 321587.21, "y": 1135487.05 },
        { "x": 321559.04, "y": 1135497.6 }
    ]
}
```

## 🧪 Tests

Pour tester l'API avec les images locales :

```bash
# Lancer l'API dans un terminal
python3 app.py

# Dans un autre terminal, lancer les tests
python3 test_api.py
```

## 📁 Structure du Projet

```
.
├── app.py                 # API FastAPI principale
├── requirements.txt       # Dépendances Python
├── setup.sh              # Script de configuration
├── test_api.py           # Script de test
├── README.md             # Documentation
├── couche/               # Couches GeoJSON (à télécharger séparément)
│   ├── *.qmd             # Métadonnées des couches
│   └── *.geojson         # Données géographiques (non incluses)
└── images/               # Images de test
    ├── leve12.png
    ├── leve13.png
    ├── leve18.png
    └── leve2.jpg
```

## ⚠️ Fichiers GeoJSON Requis

Les fichiers GeoJSON sont trop volumineux pour GitHub (jusqu'à 2.4MB). 
Vous devez les ajouter manuellement dans le dossier `couche/` :

- `aif.geojson`
- `air_proteges.geojson` 
- `dpl.geojson`
- `dpm.geojson`
- `enregistrement_individuel.geojson`
- `litige.geojson`
- `parcelles.geojson`
- `restriction.geojson`
- `tf_demembres.geojson`
- `tf_en_cours.geojson`
- `tf_etat.geojson`
- `titre_reconstitue.geojson`
- `zone_inondable.geojson`

**Sans ces fichiers, l'API retournera "NON" pour toutes les couches.**

## 🔧 Utilisation avec curl

### Analyser une image locale
```bash
curl -X POST "http://localhost:8000/analyze-local-image/leve18.png"
```

### Uploader et analyser une image
```bash
curl -X POST "http://localhost:8000/analyze-image" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@images/leve18.png"
```

### Lister les couches disponibles
```bash
curl -X GET "http://localhost:8000/layers"
```

## 🛠️ Fonctionnalités

- **Extraction automatique de coordonnées** depuis les images via Groq Vision API
- **Vérification d'intersections** avec toutes les couches GeoJSON automatiquement
- **API REST complète** avec documentation Swagger
- **Support de plusieurs formats d'images** (PNG, JPG, JPEG)
- **Gestion d'erreurs robuste**
- **Tests automatisés**

## ⚠️ Notes Importantes

- Assurez-vous que la variable d'environnement `GROQ_API_KEY` est définie
- Les images doivent contenir un tableau "COORDONNEES" visible
- L'API utilise le modèle `llama-3.2-90b-vision-preview` de Groq
- Les coordonnées sont extraites du tableau en haut à gauche des images