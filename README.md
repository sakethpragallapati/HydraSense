# HydraSense — AI-Powered Smart Hydration Predictor

![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react)
![Python](https://img.shields.io/badge/ML-Python-3776AB?logo=python)
![Flask](https://img.shields.io/badge/API-Flask-000000?logo=flask)
![Docker](https://img.shields.io/badge/DevOps-Docker-2496ED?logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?logo=vercel&logoColor=white)](https://hydrasense.vercel.app/)
[![Hugging Face](https://img.shields.io/badge/ML%20Service-Hugging%20Face-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/)

HydraSense is an end-to-end Machine Learning web application that predicts personalized hydration levels. It evaluates physiological metrics (age, weight, gender, daily water intake) alongside environmental factors (weather and activity level) to deliver smart hydration insights.

**Live Demo:** [https://hydrasense.vercel.app/](https://hydrasense.vercel.app/)

---

## Features

- **Personalized Hydration Prediction**: Uses a balanced ensemble machine learning model trained on 30,000 health records.
- **Auto Weather Detection**: Detects local weather conditions (temperature category) via browser geolocation and OpenWeatherMap API.
- **Zero False-Negative Optimization**: Partition-based ensemble design specifically handles class imbalance to ensure poor hydration conditions are reliably detected.
- **Automated CI/CD & Continuous Training (CT)**: Automated model retraining, Docker builds, and deployments on GitHub push events.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js, Lucide Icons, Axios, Vercel |
| **ML & API Service** | Python 3.11, Flask, Flask-CORS, Hugging Face Spaces |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, XGBoost, LightGBM |
| **DevOps & CI/CD** | Docker, Docker Hub, GitHub Actions |

---

## Architecture

```
[ User Browser / React Frontend (Vercel) ]
                  │
                  │  POST /predict (JSON)
                  ▼
[ ML Inference Service (Flask on Hugging Face Spaces) ]
                  │
        Balanced Ensemble LinearSVC
       (4x Models + Soft Margin Averaging)
```

- **Frontend (React)**: Hosted on Vercel. Gathers user metrics and calls the prediction endpoint.
- **ML Service (Flask)**: Hosted in a Docker container on Hugging Face Spaces. Serves preprocessing pipelines and model predictions.
- **Local Gateway (Node.js/Express)**: Included for local multi-container development via Docker Compose.

---

## Model Evaluation Benchmark

Models evaluated on the 6,000-sample test set:

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Balanced Ensemble LinearSVC** | **98.85%** | **98.85%** | **98.85%** | **0.9886** | **0.9912** | **Production Model (0 False Negatives)** |
| LinearSVC (Single) | 99.85% | 99.85% | 99.85% | 0.9985 | 0.9963 | Unbalanced baseline |
| XGBoost | 99.85% | 99.85% | 99.85% | 0.9985 | 0.9972 | Gradient boosted trees |
| Decision Tree | 99.77% | 99.77% | 99.77% | 0.9977 | 0.9964 | Single tree baseline |
| LightGBM | 99.75% | 99.75% | 99.75% | 0.9975 | 0.9963 | Tree ensemble |
| Logistic Regression | 99.73% | 99.73% | 99.73% | 0.9973 | 0.9937 | Linear baseline |
| Gradient Boosting | 99.10% | 99.10% | 99.10% | 0.9910 | 0.9842 | Ensemble baseline |
| Random Forest | 98.52% | 98.51% | 98.52% | 0.9851 | 0.9747 | Ensemble baseline |
| K-Nearest Neighbors | 97.07% | 97.05% | 97.07% | 0.9705 | 0.9502 | Distance-based baseline |
| Gaussian Naive Bayes | 82.82% | 89.45% | 82.82% | 0.8425 | 0.8726 | Probabilistic baseline |

> **Imbalance Handling**: The dataset contains an 80% Good / 20% Poor ratio. To prevent majority bias, the production model partitions the majority samples into 4 balanced 1:1 sub-models and aggregates predictions via decision margin averaging, completely eliminating false negatives on poor hydration.

---

## Project Structure

```bash
HydraSense/
├── .github/workflows/       # GitHub Actions CI/CD workflows
├── artifacts/               # Saved model (.pkl) & preprocessors
├── backend/                 # Node.js gateway (optional proxy)
├── frontend/                # React.js application
├── ml-services/             # Flask ML inference service
├── notebook/                # Exploratory Data Analysis & training notebooks
├── src/                     # Core ML package
│   ├── components/          # Ingestion, Transformation, Model Trainer
│   ├── pipeline/            # Training & Prediction pipelines
│   ├── exception.py         # Custom exception handling
│   ├── logger.py            # Logging setup
│   └── utils.py             # Common utilities (pickle save/load)
├── docker-compose.yml       # Local container orchestration
└── requirements.txt         # Python dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose *(optional)*
- OpenWeatherMap API Key *(free tier)*

### 1. Clone the Repository

```bash
git clone https://github.com/sakethpragallapati/Hydration-Levels-Prediction.git
cd Hydration-Levels-Prediction
```

### 2. Run with Docker Compose (Recommended)

Create `frontend/.env`:
```env
REACT_APP_WEATHER_API_KEY=your_openweather_api_key
REACT_APP_BACKEND_URL=http://localhost:5000
```

Start all services:
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- ML Service: `http://localhost:7000`

---

### 3. Manual Local Setup

**ML Service**:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python src/pipeline/train_pipeline.py
python ml-services/app.py
```

**Frontend**:
```bash
cd frontend
npm install
npm start
```

---

## Environment Variables

| Variable | Scope | Description |
| :--- | :--- | :--- |
| `REACT_APP_WEATHER_API_KEY` | Frontend | OpenWeatherMap API key for location-based weather |
| `REACT_APP_BACKEND_URL` | Frontend | URL of the prediction API service |
| `FLASK_API_URL` | Backend | URL of the Python ML Service (if using Node gateway) |

---

## Author

**Pragallapati Saketh**  
- LinkedIn: [https://www.linkedin.com/in/pragallapati-saketh-143384290/](https://www.linkedin.com/in/pragallapati-saketh-143384290/)  
- GitHub: [https://github.com/sakethpragallapati](https://github.com/sakethpragallapati)
