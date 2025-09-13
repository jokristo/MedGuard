# Guide de Test des Endpoints MedGuard API

## Prérequis
1. Lancer PostgreSQL avec Docker: `docker-compose up -d`
2. Installer les dépendances: `pip install -r requirements.txt`
3. Appliquer les migrations: `python manage.py migrate`
4. Démarrer le serveur: `python manage.py runserver`

## Endpoints Disponibles

### 1. Patients
- **GET** `/api/patients/` - Liste tous les patients
- **POST** `/api/patients/` - Crée un nouveau patient
- **GET** `/api/patients/{id}/` - Détails d'un patient
- **PUT** `/api/patients/{id}/` - Met à jour un patient
- **DELETE** `/api/patients/{id}/` - Supprime un patient

**Exemple POST:**
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "age": 45,
    "sexe": "M",
    "email": "dupont@email.com"
  }'
```

### 2. Devices
- **GET** `/api/devices/` - Liste tous les devices
- **POST** `/api/devices/` - Crée un nouveau device

**Exemple POST:**
```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": 1,
    "device_id": "ESP32-001",
    "type_capteur": "temperature",
    "status": true
  }'
```

### 3. Mesures
- **GET** `/api/mesures/` - Liste toutes les mesures
- **POST** `/api/mesures/` - Crée une nouvelle mesure

**Exemple POST:**
```bash
curl -X POST http://localhost:8000/api/mesures/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": 1,
    "device": 1,
    "type_donne": "temperature",
    "valeur": 37.2
  }'
```

### 4. Alertes
- **GET** `/api/alerts/` - Liste toutes les alertes
- **POST** `/api/alerts/` - Crée une nouvelle alerte

**Exemple POST:**
```bash
curl -X POST http://localhost:8000/api/alerts/ \
  -H "Content-Type: application/json" \
  -d '{
    "Patient": 1,
    "device": 1,
    "type_alerte": "temperature élevée",
    "valeur": 39.5,
    "niveau": "danger",
    "message": "Température critique détectée"
  }'
```

### 5. Prédiction IA
- **POST** `/api/predict-risk/` - Prédit le risque médical

**Exemple POST:**
```bash
curl -X POST http://localhost:8000/api/predict-risk/ \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 37.5,
    "heart_rate": 85,
    "glucose": 160
  }'
```

## Documentation Interactive
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## Exemple de Workflow Complet

1. Créer un patient
2. Associer un device au patient
3. Envoyer des mesures
4. Vérifier les alertes générées
5. Utiliser la prédiction IA

## Données de Test Recommandées

### Patients
```json
{"nom": "Martin", "age": 35, "sexe": "F", "email": "martin@email.com"}
{"nom": "Durand", "age": 62, "sexe": "M", "email": "durand@email.com"}
```

### Mesures (valeurs normales/anormales)
- Température: 36.5-37.5°C (normale), >38°C (anormale)
- Fréquence cardiaque: 60-100 bpm (normale)
- Glycémie: 70-140 mg/dL (normale), >180 mg/dL (anormale)