# Instructions pour les fichiers GeoJSON

## Problème
Les fichiers GeoJSON sont trop volumineux pour être hébergés directement sur GitHub (limite de 100MB par repo et 25MB par fichier).

## Solution
Les fichiers GeoJSON doivent être ajoutés manuellement dans le dossier `couche/`.

## Fichiers requis
- `couche/aif.geojson`
- `couche/air_proteges.geojson` (2.4MB)
- `couche/dpl.geojson`
- `couche/dpm.geojson`
- `couche/enregistrement_individuel.geojson`
- `couche/litige.geojson`
- `couche/parcelles.geojson`
- `couche/restriction.geojson`
- `couche/tf_demembres.geojson`
- `couche/tf_en_cours.geojson`
- `couche/tf_etat.geojson`
- `couche/titre_reconstitue.geojson`
- `couche/zone_inondable.geojson`

## Alternatives pour l'hébergement
1. **Git LFS** (Large File Storage) - Recommandé pour la production
2. **Drive/Dropbox** - Partage de fichiers externe
3. **Serveur de données** - Hébergement dédié pour les données géographiques
4. **Compression** - Réduire la taille des fichiers

## Impact sur l'API
Sans ces fichiers, l'API fonctionnera mais retournera toujours "NON" pour toutes les couches géographiques dans `textualData`.

Les coordonnées seront toujours extraites correctement des images.