# Silent Health AI – Intelligent Multi-Disease Risk Screening System

Silent Health AI is an AI-powered health risk screening platform that combines **Machine Learning** and a **virtual IoT health-monitoring system** to provide preliminary risk assessments for multiple health conditions.

The system currently supports risk screening for **PCOS, Anemia, Diabetes, Thyroid Disease, and Stroke**, along with live monitoring of simulated **heart rate, SpO₂, and body temperature**.

> **Disclaimer:** Silent Health AI is an educational and research project. Its results are risk-screening estimates and are not medical diagnoses.

---

## 🚀 Key Features

* 🤖 **5 Machine Learning disease-risk models**
* 🌸 PCOS risk screening
* 🩸 Anemia risk screening
* 🧪 Diabetes risk screening
* 🦋 Thyroid disease risk screening
* 🧠 Stroke risk screening
* ❤️ Live heart-rate monitoring
* 🫁 Live SpO₂ monitoring
* 🌡️ Live temperature monitoring
* 📊 Real-time sensor history graph
* 🔌 Virtual IoT sensor simulator
* 🌐 Flask-based web application
* 📱 Responsive web dashboard
* 💾 Saved ML models using Joblib
* 📈 Risk probability display for PCOS
* 🔄 REST API for IoT sensor communication

---

## 🧠 Machine Learning Models

The platform uses trained machine learning models stored as `.pkl` files.

| Health Condition | Model                           |
| ---------------- | ------------------------------- |
| PCOS             | Logistic Regression             |
| Anemia           | Trained ML Classification Model |
| Diabetes         | Trained ML Classification Model |
| Thyroid Disease  | Trained ML Classification Model |
| Stroke           | Trained ML Classification Model |

The models were developed using Python-based data preprocessing, exploratory data analysis, model training, evaluation, and model serialization.

---

## 🔬 Health Conditions

### PCOS

The PCOS module evaluates multiple clinical, hormonal, lifestyle, and reproductive health parameters to estimate PCOS risk.

### Anemia

The anemia module uses blood-related parameters including:

* Hemoglobin
* MCH
* MCHC
* MCV
* Gender

### Diabetes

The diabetes module evaluates parameters such as:

* Pregnancies
* Glucose
* Blood Pressure
* Skin Thickness
* Insulin
* BMI
* Diabetes Pedigree Function
* Age

### Thyroid Disease

The thyroid module evaluates thyroid-related laboratory values together with demographic and risk-related factors.

### Stroke

The stroke module evaluates demographic, medical, lifestyle, and cardiovascular risk factors.

---

## 📡 IoT Health Monitoring

Silent Health AI includes a **virtual IoT device simulator**.

The simulator sends sensor readings to the Flask backend through a REST API.

### Monitored Parameters

| Parameter   | Unit |
| ----------- | ---- |
| Heart Rate  | BPM  |
| SpO₂        | %    |
| Temperature | °C   |

The backend evaluates each reading against predefined reference ranges and determines:

* Sensor status
* Overall health status
* Device connectivity status
* Timestamp
* Recent sensor history

The dashboard displays the readings and visualizes the latest sensor history using **Chart.js**.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────────┐
                    │      Web Dashboard       │
                    │       HTML / CSS / JS    │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       Flask Backend      │
                    │        Python API        │
                    └───────┬─────────┬────────┘
                            │         │
                ┌───────────┘         └────────────┐
                ▼                                  ▼
      ┌───────────────────┐              ┌──────────────────┐
      │  ML Prediction    │              │   IoT REST API   │
      │     Modules       │              │                  │
      └─────────┬─────────┘              └────────┬─────────┘
                │                                  │
                ▼                                  ▼
      ┌───────────────────┐              ┌──────────────────┐
      │  Saved .pkl Models │              │ IoT Simulator    │
      └───────────────────┘              │ Heart Rate       │
                                         │ SpO₂             │
                                         │ Temperature      │
                                         └──────────────────┘
```

---

## 📁 Project Structure

```text
Silent_Health_Risk_Detector/
│
├── app.py
├── iot_simulator.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── datasets/
│   ├── anemia.csv
│   ├── diabetes.csv
│   ├── healthcare-dataset-stroke-data.csv
│   ├── thyroid_cancer_risk_data.csv
│   ├── PCOS_data_without_infertility.xlsx
│   └── ...
│
├── models/
│   ├── anemia_model.pkl
│   ├── diabetes_model.pkl
│   ├── pcos_logistic_model.pkl
│   ├── pcos_model.pkl
│   ├── stroke_model.pkl
│   └── thyroid_model.pkl
│
├── notebooks/
│   ├── EDA_Silent_Health_Risk_Detector.ipynb
│   ├── PCOS_Model.ipynb
│   ├── Anemia_Model.ipynb
│   ├── Diabetes_Model.ipynb
│   ├── Thyroid_Model.ipynb
│   └── Stroke_Model.ipynb
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── index.html
    ├── about.html
    ├── contact.html
    ├── dashboard.html
    ├── pcos.html
    ├── anemia.html
    ├── diabetes.html
    ├── thyroid.html
    └── stroke.html
```

---

## 🛠️ Technologies Used

### Programming

* Python
* HTML5
* CSS3
* JavaScript

### Machine Learning

* NumPy
* Pandas
* Scikit-learn
* Joblib

### Web Development

* Flask
* Jinja2
* REST API

### Visualization

* Chart.js
* Matplotlib

### Development Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rudrahon1103/Silent_Health_Risk_Detector..git
```

### 2. Open the project folder

```bash
cd Silent_Health_Risk_Detector.
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser.

---

## 📡 Running the IoT Simulator

Keep the Flask application running.

Open another terminal and run:

```bash
python iot_simulator.py
```

The virtual device will send health sensor readings to:

```text
/api/sensor-data
```

The dashboard retrieves the readings and displays them in real time.

---

## 🔄 Application Workflow

```text
User
  │
  ▼
Web Dashboard
  │
  ├── Disease Selection
  │       │
  │       ▼
  │   Health Parameters
  │       │
  │       ▼
  │   ML Model
  │       │
  │       ▼
  │   Risk Screening Result
  │
  └── IoT Monitoring
          │
          ▼
    Virtual Sensor
          │
          ▼
      Flask API
          │
          ▼
    Sensor Processing
          │
          ▼
    Live Dashboard
```

---

## 🎯 Project Objective

The primary objective of Silent Health AI is to demonstrate how **machine learning and IoT-based monitoring concepts can be combined into a single health technology platform**.

The project focuses on:

* Early risk screening
* Multi-disease assessment
* Health parameter monitoring
* AI-assisted decision support
* Real-time sensor visualization
* Integration of ML models with a web application

---

## 🔮 Future Enhancements

Possible future improvements include:

* Integration with real wearable sensors
* Real-time heart-rate and SpO₂ hardware
* Blood-pressure sensor integration
* Mobile application
* User authentication
* Personal health history
* Database integration
* Improved model validation
* Model explainability
* Personalized health alerts
* Cloud deployment
* Secure health-data management

---

## ⚠️ Disclaimer

Silent Health AI is developed for **educational, academic, and research purposes**.

The predictions generated by the system are machine-learning-based risk estimates and should **not be considered medical diagnoses or professional medical advice**.

Users should consult qualified healthcare professionals for medical evaluation and treatment decisions.

---

## 👨‍💻 Project

**Silent Health AI – Intelligent Multi-Disease Risk Screening System**

Built using **Python, Machine Learning, Flask, JavaScript, and IoT simulation**.
