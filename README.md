# Laptop Health Prediction

## Project Overview

Laptop Health Prediction is a modern AI-powered diagnostics dashboard that predicts overall laptop health from system performance metrics. It uses a trained machine learning model and presents the result through a glassmorphic Gradio UI with interactive charts, risk analysis, recommendations, prediction history, and downloadable reports.

TODO: Add a short personal/project motivation here.

## Features

- Predicts laptop health score from 0 to 100
- Uses system metrics such as CPU, RAM, Disk I/O, device age, running apps, and crashed apps
- Supports hardware profile inputs for laptop model, processor, and graphics
- Shows health status, risk level, confidence score, alerts, and recommendations
- Includes interactive Plotly charts:
  - Health gauge
  - Resource utilization chart
  - Metric risk chart
  - Health vs risk donut chart
  - System profile radar chart
  - Health timeline
- Stores local prediction history
- Generates downloadable text health reports
- Responsive glassmorphic UI built with Gradio

## Tech Stack

- Python
- Gradio
- scikit-learn
- Pandas
- NumPy
- Plotly
- Joblib

## Dataset

TODO: Add dataset name and source.

Example details to fill:

- Dataset source: TODO: Kaggle / custom dataset / other source
- Number of records: TODO
- Number of features: 10
- Target column: Laptop health score
- Dataset link: TODO

The dataset is used to train the machine learning model that predicts laptop health based on hardware and performance metrics.

## ML Model

TODO: Add exact training details after finalizing the model report.

- Model type: Random Forest Regressor
- Model file: `model.pkl`
- Input features: 10
- Output: Health score between 0 and 100
- Training score / R2 score: TODO
- Test score / validation score: TODO
- Training notebook: TODO

Input features used by the model:

- Device age
- CPU cores
- CPU utilization
- Memory utilization
- Disk I/O utilization
- Running applications count
- Crashed applications count
- Encoded device model
- Encoded processor
- Encoded graphics

## Screenshots

TODO: Add final screenshots here.

| Dashboard | Prediction Result |
| --- | --- |
| TODO: Add dashboard screenshot | TODO: Add result screenshot |

Suggested screenshot paths:

```text
assets/dashboard.png
assets/result.png
assets/charts.png
```

## Demo Link

TODO: Add live deployed demo link.

Example:

```text
https://huggingface.co/spaces/SachinSharma01/laptop-performance-heat-predictor
```

If the project is not deployed yet, run it locally using the installation steps below.

## Installation

Clone the repository:

```bash
git clone TODO: add-your-repository-url
cd TODO: add-your-project-folder-name
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure `model.pkl` is present in the project root.

Run the app:

```bash
python app.py
```

Open the local Gradio URL shown in the terminal:

```text
http://127.0.0.1:7860
```

## Future Work

- Add live system metric collection
- Add PDF report export
- Add user authentication
- Add database-backed prediction history
- Add model retraining notebook
- Add Docker support
- Deploy on Hugging Face Spaces / Render / Railway
- Add more laptop models and hardware categories

## Project Structure

```text
.
|-- app.py                  # Application entry point
|-- ui.py                   # Main Gradio layout and event wiring
|-- prediction.py           # ML model loading and prediction pipeline
|-- charts.py               # Plotly chart builders
|-- components.py           # Reusable Gradio UI components
|-- styles.py               # Result HTML builders
|-- theme.py                # Custom Gradio theme and CSS
|-- utils.py                # Validation, history, reports, notifications
|-- model.pkl               # Trained ML model
|-- requirements.txt        # Python dependencies
`-- prediction_history.json # Local prediction history
```

## Author

**TODO: Your Name**

- GitHub: TODO
- LinkedIn: TODO
- Portfolio: TODO
- Email: TODO

## License

TODO: Add license.

Example:

```text
MIT License
```
