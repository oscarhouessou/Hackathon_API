#!/bin/bash

# Script pour configurer et lancer l'API GeoData Analysis

echo "🚀 Configuration de l'environnement GeoData Analysis API"

# Vérifier si python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip3 install -r requirements.txt

# Vérifier la configuration de la clé API
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé. Création d'un exemple..."
    cp .env.example .env
    echo "📝 Veuillez éditer le fichier .env et ajouter votre clé API Groq."
elif ! grep -q "GROQ_API_KEY=" .env || grep -q "your_groq_api_key_here" .env; then
    echo "⚠️  Veuillez configurer votre GROQ_API_KEY dans le fichier .env"
    echo "   Éditez le fichier .env et remplacez 'your_groq_api_key_here' par votre vraie clé."
else
    echo "✅ Configuration .env trouvée!"
fi

echo "✅ Configuration terminée!"
echo ""
echo "🔧 Pour lancer l'API:"
echo "   python3 app.py"
echo ""
echo "📖 Endpoints disponibles:"
echo "   POST /analyze-image - Analyser une image uploadée"
echo "   POST /analyze-local-image/{nom_image} - Analyser une image locale"
echo "   GET /layers - Lister les couches disponibles"
echo "   GET /health - Vérifier l'état de l'API"
echo ""
echo "🌐 L'API sera disponible sur: http://localhost:8000"
echo "📚 Documentation interactive: http://localhost:8000/docs"