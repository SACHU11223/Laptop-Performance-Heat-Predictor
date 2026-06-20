"""ML model inference for laptop health prediction."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
model = None


FEATURE_NAMES = [
    "device_Age",
    "cores",
    "CPU_Utilization",
    "Memory Utilization",
    "diskIO Utilization",
    "Running_Apps_Count",
    "Crashed_Apps_Count",
    "device_Model_Encoded",
    "processor_Encoded",
    "graphics_Encoded",
]


DEVICE_MODEL_MAP = {
    "Dell Inspiron": 0,
    "HP Pavilion": 1,
    "Lenovo IdeaPad": 2,
    "Asus VivoBook": 3,
    "Acer Aspire": 4,
    "MacBook Air": 5,
    "MacBook Pro": 6,
    "Dell XPS": 7,
    "HP EliteBook": 8,
    "Lenovo ThinkPad": 9,
    "Other": 10,
}

PROCESSOR_MAP = {
    "Intel Core i3": 0,
    "Intel Core i5": 1,
    "Intel Core i7": 2,
    "Intel Core i9": 3,
    "AMD Ryzen 3": 4,
    "AMD Ryzen 5": 5,
    "AMD Ryzen 7": 6,
    "AMD Ryzen 9": 7,
    "Apple M1": 8,
    "Apple M2": 9,
    "Other": 10,
}

GRAPHICS_MAP = {
    "Intel UHD Graphics": 0,
    "Intel Iris Xe": 1,
    "NVIDIA GTX 1650": 2,
    "NVIDIA RTX 3050": 3,
    "NVIDIA RTX 3060": 4,
    "AMD Radeon RX 550": 5,
    "AMD Radeon RX 580": 6,
    "Apple M1 GPU": 7,
    "Apple M2 GPU": 8,
    "Other": 9,
}


def load_model() -> bool:
    """Load the local model.pkl file once."""
    global model
    if model is not None:
        return True
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
        return True
    except FileNotFoundError:
        print(f"Model not found at {MODEL_PATH}")
        return False
    except Exception as exc:
        print(f"Error loading model: {exc}")
        return False


def interpret_health_score(score: float) -> dict:
    score = max(0.0, min(100.0, float(score)))

    if score >= 85:
        return {
            "health_score": round(score, 1),
            "health_status": "Excellent",
            "risk_level": "Low",
            "risk_percent": round(100 - score, 1),
            "confidence": round(85 + (score - 85) * 0.5, 1),
            "color": "#4ade80",
            "recommendations": [
                "System is performing very well.",
                "Keep regular cleanup and update routines active.",
                "Monitor temperatures during heavy workloads.",
            ],
            "alerts": [],
        }
    if score >= 70:
        return {
            "health_score": round(score, 1),
            "health_status": "Good",
            "risk_level": "Low-Medium",
            "risk_percent": round(100 - score, 1),
            "confidence": round(75 + (score - 70) * 0.6, 1),
            "color": "#86efac",
            "recommendations": [
                "Close unused background apps.",
                "Run disk cleanup weekly.",
                "Keep OS and drivers updated.",
            ],
            "alerts": ["Minor performance dip detected."],
        }
    if score >= 50:
        return {
            "health_score": round(score, 1),
            "health_status": "Fair",
            "risk_level": "Medium",
            "risk_percent": round(100 - score, 1),
            "confidence": round(65 + (score - 50) * 0.5, 1),
            "color": "#facc15",
            "recommendations": [
                "Restart the laptop to clear memory pressure.",
                "Close heavy apps and browser tabs.",
                "Run antivirus and temporary-file cleanup.",
                "Consider a RAM upgrade if this pattern repeats.",
            ],
            "alerts": ["Elevated utilization detected.", "Maintenance is recommended."],
        }
    if score >= 30:
        return {
            "health_score": round(score, 1),
            "health_status": "Poor",
            "risk_level": "High",
            "risk_percent": round(100 - score, 1),
            "confidence": round(60 + (score - 30) * 0.25, 1),
            "color": "#fb923c",
            "recommendations": [
                "Restart immediately and stop non-critical apps.",
                "Free disk space and remove unused software.",
                "Check for malware and overheating.",
                "Run hardware diagnostics if the score remains low.",
            ],
            "alerts": ["High system stress.", "Failure risk is elevated."],
        }
    return {
        "health_score": round(score, 1),
        "health_status": "Critical",
        "risk_level": "Critical",
        "risk_percent": round(100 - score, 1),
        "confidence": round(55 + score * 0.17, 1),
        "color": "#fb7185",
        "recommendations": [
            "Back up important data now.",
            "Shut down non-critical processes.",
            "Check storage, thermals, battery, and memory.",
            "Take the laptop to a technician if the issue persists.",
        ],
        "alerts": ["Critical failure risk.", "Immediate action required."],
    }


def predict_health(
    device_age: float,
    cores: int,
    cpu_utilization: float,
    memory_utilization: float,
    disk_io_utilization: float,
    running_apps: int,
    crashed_apps: int,
    device_model: str = "Other",
    processor: str = "Other",
    graphics: str = "Other",
) -> dict:
    if not load_model():
        return {"error": "Model could not be loaded. Ensure model.pkl is present.", "health_score": 0}

    features = pd.DataFrame(
        [
            [
                device_age,
                cores,
                cpu_utilization,
                memory_utilization,
                disk_io_utilization,
                running_apps,
                crashed_apps,
                DEVICE_MODEL_MAP.get(device_model, DEVICE_MODEL_MAP["Other"]),
                PROCESSOR_MAP.get(processor, PROCESSOR_MAP["Other"]),
                GRAPHICS_MAP.get(graphics, GRAPHICS_MAP["Other"]),
            ]
        ],
        columns=FEATURE_NAMES,
    )

    try:
        raw_score = model.predict(features)[0]
    except Exception as exc:
        return {"error": f"Prediction failed: {exc}", "health_score": 0, "health_status": "Error"}

    result = interpret_health_score(raw_score)
    result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result["input_summary"] = {
        "Device Age": f"{device_age} years",
        "CPU Cores": int(cores),
        "CPU Usage": f"{cpu_utilization}%",
        "RAM Usage": f"{memory_utilization}%",
        "Disk I/O": f"{disk_io_utilization}%",
        "Running Apps": int(running_apps),
        "Crashed Apps": int(crashed_apps),
        "Device Model": device_model,
        "Processor": processor,
        "Graphics": graphics,
    }
    return result


def quick_predict(cpu: float, ram: float, disk: float) -> dict:
    return predict_health(2.0, 4, cpu, ram, disk, max(1, int(cpu / 10)), 0)


def get_model_info() -> dict:
    if not load_model():
        return {"error": "Model not loaded"}
    return {
        "model_type": type(model).__name__,
        "n_estimators": getattr(model, "n_estimators", "N/A"),
        "n_features": getattr(model, "n_features_in_", len(FEATURE_NAMES)),
        "feature_names": FEATURE_NAMES,
        "model_file": str(MODEL_PATH),
        "file_size_kb": round(os.path.getsize(MODEL_PATH) / 1024, 1) if MODEL_PATH.exists() else "N/A",
    }


load_model()
