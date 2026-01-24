# HydraSense - AI-Powered Smart Hydration Predictor

![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react)
![Node.js](https://img.shields.io/badge/Backend-Node.js-339933?logo=nodedotjs)
![Python](https://img.shields.io/badge/ML-Python-3776AB?logo=python)
![Docker](https://img.shields.io/badge/DevOps-Docker-2496ED?logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions)
[![Frontend](https://img.shields.io/badge/Frontend-Vercel-000000?logo=vercel&logoColor=white)](https://vercel.com/)
[![Backend & ML](https://img.shields.io/badge/Backend%20%26%20ML-Hugging%20Face-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/)

HydraSense is an end-to-end Machine Learning web application that predicts optimal hydration levels. Unlike generic water trackers, it leverages supervised learning models to analyze physiological attributes (age, weight, gender) along with real-time environmental conditions (weather) to deliver accurate hydration recommendations.

The application is built using a microservices architecture and fully containerized with Docker. A complete CI/CD pipeline powered by GitHub Actions automates model training, Docker image builds, and image publishing to Docker Hub, followed by continuous deployment to production. The final production models, LinearSVC and XGBoost, both achieved 99.85% accuracy on the test dataset.

## Live Demo

Deployed URL: [https://hydrasense.vercel.app/](https://hydrasense.vercel.app/)

## Architecture

The project follows a 3-tier microservices architecture:

1. **Frontend (React.js)** - Deployed on **Vercel**
   - Responsive user interface for data input
   - Automatic weather detection using browser geolocation and OpenWeatherMap API

2. **Backend Gateway (Node.js / Express)** - Deployed on **Hugging Face Spaces** (Docker)
   - Acts as a secure reverse proxy
   - Handles request validation, CORS, and routing
   - Forwards inference requests to the ML service

3. **ML Service (Python / Flask)** - Deployed on **Hugging Face Spaces** (Docker)
   - Loads the trained model (model.pkl) and preprocessing pipeline (preprocessor.pkl)
   - Exposes a REST API endpoint (/predictData) for predictions

## Directory Structure

The project uses a monorepo structure:

```bash
HydraSense/
├── .github/workflows/   # CI/CD pipeline using GitHub Actions
├── artifacts/           # Saved models (.pkl) and processed datasets
├── backend/             # Node.js middleware service
├── frontend/            # React application
├── ml-services/         # Flask-based ML inference service
├── notebook/            # EDA and model training notebooks
├── src/                 # Core ML pipeline logic
├── docker-compose.yml   # Local multi-container orchestration
└── README.md
```

## Machine Learning Pipeline

### Dataset

Daily Water Intake and Hydration Patterns Dataset  
https://www.kaggle.com/datasets/sonalshinde123/daily-water-intake-and-hydration-patterns-dataset

Total records: 30,000

### Models Evaluated

All major classification algorithms were trained and evaluated using the same preprocessing pipeline. Below are the complete evaluation results on the test dataset.

| Model                     | Accuracy | Notes / Status              |
|---------------------------|----------|-----------------------------|
| Logistic Regression       | 99.73%   | Strong baseline             |
| K-Nearest Neighbors       | 97.06%   | Performance drops with scale|
| LinearSVC                 | 99.85%   | Selected for production     |
| Gaussian Naive Bayes      | 82.81%   | Underfitting observed       |
| Decision Tree             | 99.75%   | Slight overfitting risk     |
| Random Forest             | 98.60%   | Good but heavier model      |
| Gradient Boosting         | 99.10%   | Stable performance          |
| XGBoost                   | 99.85%   | Selected for production     |
| LightGBM                  | 99.75%   | Comparable to tree models   |

### Confusion Matrix Summary

- LinearSVC:
  - True Negatives: 4788
  - False Positives: 0
  - False Negatives: 9
  - True Positives: 1203

- XGBoost:
  - True Negatives: 4785
  - False Positives: 3
  - False Negatives: 6
  - True Positives: 1206

These models showed the best balance between accuracy, generalization, and inference speed.

### Pipeline Stages (src/)

1. Data Ingestion
   - Loads raw dataset
   - Splits data into training and testing sets

2. Data Transformation
   - Numerical features scaled using StandardScaler
   - Categorical features encoded using OneHotEncoder

3. Model Training
   - Trains multiple classification algorithms
   - Evaluates models using accuracy and confusion matrix
   - Persists the best-performing model and preprocessor to artifacts/

## Installation and Local Setup

### Prerequisites

- Docker and Docker Compose
- Node.js v18 or higher
- Python v3.11.9 or higher
- OpenWeatherMap API key

### Method 1: Docker (Recommended)

This method launches all three services automatically.

Clone the repository:

git clone https://github.com/sakethpragallapati/Hydration-Levels-Prediction.git  
cd HydraSense

Create a .env file inside frontend/:

REACT_APP_WEATHER_API_KEY=your_openweather_api_key  
REACT_APP_BACKEND_URL=http://localhost:5000

Run Docker Compose:

docker-compose up --build

Access services locally:

Frontend: http://localhost:3000  
Backend: http://localhost:5000  
ML Service: http://localhost:7000

## DevOps and CI/CD

The project uses a robust GitHub Actions pipeline for automated CI/CD with Continuous Training (CT).

**Workflow (`main.yml`):**
1.  **Trigger:** Push or pull request to the `master` branch.
2.  **Build & Test Job:**
    * Checks out code.
    * Executes the ML training pipeline (`src/pipeline/train_pipeline.py`) to generate fresh artifacts.
    * Builds Docker images for Backend and ML services and pushes them to Docker Hub.
3.  **Deploy ML to Hugging Face Job:**
    * **Continuous Training (CT):** Re-runs the training pipeline on a fresh runner to ensure the latest model artifacts are generated right before deployment.
    * Configures the Hugging Face Space repos.
    * Force-pushes the application code and the newly generated `artifacts/` folder to the Hugging Face ML Space.
4.  **Deploy Backend to Hugging Face Job:**
    * Configures the Hugging Face Space repo.
    * Force-pushes the backend code to the Hugging Face Backend Space.
5.  **Frontend Deployment:** Vercel automatically detects changes to the `frontend/` directory on GitHub and deploys the updated React app.
   
## Environment Variables

| Variable | Service | Description | Example Value |
| :--- | :--- | :--- | :--- |
| `REACT_APP_WEATHER_API_KEY` | Frontend | OpenWeatherMap API key | `your_api_key` |
| `REACT_APP_BACKEND_URL` | Frontend (Vercel) | URL of the Node.js Backend Space | `https://sasrplays-hydrasense-backend.hf.space` |
| `FLASK_API_URL` | Backend (HF Space) | URL of the Python ML Space | `https://sasrplays-hydrasense-ml.hf.space` |

## Author

Pragallapati Saketh  
LinkedIn: https://www.linkedin.com/in/pragallapati-saketh-143384290/  
GitHub: https://github.com/sakethpragallapati
