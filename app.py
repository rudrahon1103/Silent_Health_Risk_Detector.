from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
import time
from datetime import datetime

app = Flask(__name__)

# ============================================================
# LOAD MACHINE LEARNING MODELS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

diabetes_model = joblib.load(
    os.path.join(BASE_DIR, "models", "diabetes_model.pkl")
)

pcos_model = joblib.load(
    os.path.join(BASE_DIR, "models", "pcos_logistic_model.pkl")
)

anemia_model = joblib.load(
    os.path.join(BASE_DIR, "models", "anemia_model.pkl")
)

thyroid_model = joblib.load(
    os.path.join(BASE_DIR, "models", "thyroid_model.pkl")
)

stroke_model = joblib.load(
    os.path.join(BASE_DIR, "models", "stroke_model.pkl")
)

# ============================================================
# IOT DEVICE DATA
# ============================================================

latest_sensor_data = {
    "heart_rate": 0,
    "spo2": 0,
    "temperature": 0,

    "heart_rate_status": "UNKNOWN",
    "spo2_status": "UNKNOWN",
    "temperature_status": "UNKNOWN",
    "overall_status": "UNKNOWN",

    "device_status": "Offline",
    "timestamp": None
}

# ============================================================
# LIVE SENSOR HISTORY
# ============================================================

# Stores recent sensor readings for the live graph.
# Maximum 30 readings are kept in memory.

sensor_history = []

MAX_HISTORY = 30

# ============================================================
# IOT CONNECTION TIMEOUT
# ============================================================

IOT_TIMEOUT = 10

last_sensor_update = None

# ============================================================
# SENSOR STATUS THRESHOLDS
# ============================================================

HEART_RATE_MIN = 60
HEART_RATE_MAX = 100

SPO2_MIN = 95
SPO2_MAX = 100

TEMPERATURE_MIN = 36.1
TEMPERATURE_MAX = 37.5

# ============================================================
# SENSOR STATUS FUNCTIONS
# ============================================================

def get_heart_rate_status(value):

    if HEART_RATE_MIN <= value <= HEART_RATE_MAX:
        return "NORMAL"

    return "ABNORMAL"


def get_spo2_status(value):

    if SPO2_MIN <= value <= SPO2_MAX:
        return "NORMAL"

    return "ABNORMAL"


def get_temperature_status(value):

    if TEMPERATURE_MIN <= value <= TEMPERATURE_MAX:
        return "NORMAL"

    return "ABNORMAL"


def get_overall_status(
    heart_rate_status,
    spo2_status,
    temperature_status
):

    if (
        heart_rate_status == "NORMAL"
        and spo2_status == "NORMAL"
        and temperature_status == "NORMAL"
    ):
        return "NORMAL"

    return "ABNORMAL"


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():

    return render_template("about.html")


# ============================================================
# CONTACT
# ============================================================

@app.route("/contact")
def contact():

    return render_template("contact.html")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


# ============================================================
# IOT SENSOR API
# ============================================================

@app.route("/api/sensor-data", methods=["GET", "POST"])
def sensor_data():

    global latest_sensor_data
    global last_sensor_update
    global sensor_history

    # ========================================================
    # RECEIVE SENSOR DATA
    # ========================================================

    if request.method == "POST":

        try:

            data = request.get_json()

            if not data:

                return jsonify({
                    "status": "error",
                    "message": "No sensor data received"
                }), 400

            # ------------------------------------------------
            # GET SENSOR VALUES
            # ------------------------------------------------

            heart_rate = float(
                data.get("heart_rate", 0)
            )

            spo2 = float(
                data.get("spo2", 0)
            )

            temperature = float(
                data.get("temperature", 0)
            )

            # ------------------------------------------------
            # VALIDATE SENSOR VALUES
            # ------------------------------------------------

            if heart_rate < 0:
                raise ValueError("Invalid heart rate")

            if spo2 < 0:
                raise ValueError("Invalid SpO2")

            if temperature < 0:
                raise ValueError("Invalid temperature")

            # ------------------------------------------------
            # DETERMINE SENSOR STATUS
            # ------------------------------------------------

            heart_rate_status = get_heart_rate_status(
                heart_rate
            )

            spo2_status = get_spo2_status(
                spo2
            )

            temperature_status = get_temperature_status(
                temperature
            )

            overall_status = get_overall_status(
                heart_rate_status,
                spo2_status,
                temperature_status
            )

            # ------------------------------------------------
            # CURRENT TIME
            # ------------------------------------------------

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            # ------------------------------------------------
            # UPDATE LATEST SENSOR DATA
            # ------------------------------------------------

            latest_sensor_data = {

                "heart_rate": heart_rate,

                "spo2": spo2,

                "temperature": temperature,

                "heart_rate_status": heart_rate_status,

                "spo2_status": spo2_status,

                "temperature_status": temperature_status,

                "overall_status": overall_status,

                "device_status": "Online",

                "timestamp": current_time
            }

            # =================================================
            # ADD READING TO SENSOR HISTORY
            # =================================================

            sensor_history.append({

                "time": current_time,

                "heart_rate": heart_rate,

                "spo2": spo2,

                "temperature": temperature

            })

            # =================================================
            # KEEP ONLY LAST 30 READINGS
            # =================================================

            if len(sensor_history) > MAX_HISTORY:

                sensor_history.pop(0)

            # ------------------------------------------------
            # SAVE LAST RECEIVED TIME
            # ------------------------------------------------

            last_sensor_update = time.time()

            # ------------------------------------------------
            # RESPONSE
            # ------------------------------------------------

            return jsonify({

                "status": "success",

                "message": "Sensor data received",

                "data": latest_sensor_data

            })

        except Exception as e:

            return jsonify({

                "status": "error",

                "message": str(e)

            }), 400

    # ========================================================
    # SEND LATEST SENSOR DATA
    # ========================================================

    if last_sensor_update is None:

        latest_sensor_data["device_status"] = "Offline"

        latest_sensor_data["overall_status"] = "UNKNOWN"

    else:

        elapsed_time = (
            time.time() - last_sensor_update
        )

        if elapsed_time <= IOT_TIMEOUT:

            latest_sensor_data["device_status"] = "Online"

        else:

            latest_sensor_data["device_status"] = "Offline"

    return jsonify(latest_sensor_data)


# ============================================================
# SENSOR HISTORY API
# ============================================================

# IMPORTANT:
# This function is intentionally named get_sensor_history()
# instead of sensor_history().
#
# sensor_history is our LIST.
# Previously, naming this function sensor_history caused
# the function to replace the list and .append() failed.

@app.route("/api/sensor-history", methods=["GET"])
def get_sensor_history():

    return jsonify({

        "status": "success",

        "history": sensor_history

    })


# ============================================================
# CLEAR SENSOR HISTORY
# ============================================================

@app.route("/api/clear-sensor-history", methods=["POST"])
def clear_sensor_history():

    global sensor_history

    sensor_history.clear()

    return jsonify({

        "status": "success",

        "message": "Sensor history cleared"

    })


# ============================================================
# DISEASE PAGES
# ============================================================

@app.route("/pcos")
def pcos():

    return render_template("pcos.html")


@app.route("/anemia")
def anemia():

    return render_template("anemia.html")


@app.route("/diabetes")
def diabetes():

    return render_template("diabetes.html")


@app.route("/thyroid")
def thyroid():

    return render_template("thyroid.html")


@app.route("/stroke")
def stroke():

    return render_template("stroke.html")


# ============================================================
# DIABETES PREDICTION
# ============================================================

@app.route("/predict_diabetes", methods=["POST"])
def predict_diabetes():

    try:

        features = np.array([[

            float(request.form["pregnancies"]),
            float(request.form["glucose"]),
            float(request.form["bloodpressure"]),
            float(request.form["skinthickness"]),
            float(request.form["insulin"]),
            float(request.form["bmi"]),
            float(request.form["dpf"]),
            float(request.form["age"])

        ]])

        prediction = diabetes_model.predict(features)

        if prediction[0] == 1:

            result = "⚠️ High Risk of Diabetes Detected"

        else:

            result = "✅ Low Risk of Diabetes"

        return render_template(
            "diabetes.html",
            prediction_text=result
        )

    except Exception as e:

        return render_template(
            "diabetes.html",
            prediction_text=f"Error: {e}"
        )


# ============================================================
# PCOS PREDICTION
# ============================================================

@app.route("/predict_pcos", methods=["POST"])
def predict_pcos():

    try:

        pcos_features = {

            " Age (yrs)": float(request.form["age"]),
            "Weight (Kg)": float(request.form["weight"]),
            "Height(Cm) ": float(request.form["height"]),
            "BMI": float(request.form["bmi"]),
            "Blood Group": float(request.form["bloodgroup"]),
            "Pulse rate(bpm) ": float(request.form["pulse"]),
            "RR (breaths/min)": float(request.form["rr"]),
            "Hb(g/dl)": float(request.form["hb"]),
            "Cycle(R/I)": float(request.form["cycle"]),
            "Cycle length(days)": float(request.form["cycle_length"]),
            "Marraige Status (Yrs)": float(request.form["marriage"]),
            "Pregnant(Y/N)": float(request.form["pregnant"]),
            "No. of aborptions": float(request.form["abortions"]),
            "  I   beta-HCG(mIU/mL)": float(request.form["beta_hcg1"]),
            "II    beta-HCG(mIU/mL)": float(request.form["beta_hcg2"]),
            "FSH(mIU/mL)": float(request.form["fsh"]),
            "LH(mIU/mL)": float(request.form["lh"]),
            "FSH/LH": float(request.form["fsh_lh"]),
            "Hip(inch)": float(request.form["hip"]),
            "Waist(inch)": float(request.form["waist"]),
            "Waist:Hip Ratio": float(request.form["waist_hip"]),
            "TSH (mIU/L)": float(request.form["tsh"]),
            "AMH(ng/mL)": float(request.form["amh"]),
            "PRL(ng/mL)": float(request.form["prl"]),
            "Vit D3 (ng/mL)": float(request.form["vit_d3"]),
            "PRG(ng/mL)": float(request.form["prg"]),
            "RBS(mg/dl)": float(request.form["rbs"]),
            "Weight gain(Y/N)": float(request.form["weight_gain"]),
            "hair growth(Y/N)": float(request.form["hair_growth"]),
            "Skin darkening (Y/N)": float(request.form["skin_darkening"]),
            "Hair loss(Y/N)": float(request.form["hair_loss"]),
            "Pimples(Y/N)": float(request.form["pimples"]),
            "Fast food (Y/N)": float(request.form["fast_food"]),
            "Reg.Exercise(Y/N)": float(request.form["exercise"]),
            "BP _Systolic (mmHg)": float(request.form["bp_sys"]),
            "BP _Diastolic (mmHg)": float(request.form["bp_dia"]),
            "Follicle No. (L)": float(request.form["follicle_l"]),
            "Follicle No. (R)": float(request.form["follicle_r"]),
            "Avg. F size (L) (mm)": float(request.form["f_size_l"]),
            "Avg. F size (R) (mm)": float(request.form["f_size_r"]),
            "Endometrium (mm)": float(request.form["endometrium"])

        }

        feature_order = list(
            pcos_model.feature_names_in_
        )

        final_values = []

        for feature in feature_order:

            if feature == "Sl. No":

                final_values.append(0)

            elif feature in pcos_features:

                final_values.append(
                    pcos_features[feature]
                )

            else:

                raise ValueError(
                    f"Model expects feature '{feature}', "
                    f"but it was not provided."
                )

        features = pd.DataFrame(
            [final_values],
            columns=feature_order
        )

        prediction = pcos_model.predict(
            features
        )

        risk_probability = None

        if hasattr(
            pcos_model,
            "predict_proba"
        ):

            probabilities = (
                pcos_model.predict_proba(features)
            )

            if 1 in pcos_model.classes_:

                class_index = list(
                    pcos_model.classes_
                ).index(1)

                risk_probability = round(
                    probabilities[0][class_index] * 100,
                    2
                )

        if prediction[0] == 1:

            result = "⚠️ High Risk of PCOS Detected"

        else:

            result = "✅ Low Risk of PCOS"

        return render_template(
            "pcos.html",
            prediction_text=result,
            risk_probability=risk_probability
        )

    except Exception as e:

        return render_template(
            "pcos.html",
            prediction_text=f"Error: {e}",
            risk_probability=None
        )


# ============================================================
# ANEMIA PREDICTION
# ============================================================

@app.route("/predict_anemia", methods=["POST"])
def predict_anemia():

    try:

        features = np.array([[

            float(request.form["gender"]),
            float(request.form["hemoglobin"]),
            float(request.form["mch"]),
            float(request.form["mchc"]),
            float(request.form["mcv"])

        ]])

        prediction = anemia_model.predict(features)

        if prediction[0] == 1:

            result = "⚠️ High Risk of Anemia Detected"

        else:

            result = "✅ Low Risk of Anemia"

        return render_template(
            "anemia.html",
            prediction_text=result
        )

    except Exception as e:

        return render_template(
            "anemia.html",
            prediction_text=f"Error: {e}"
        )


# ============================================================
# THYROID PREDICTION
# ============================================================

@app.route("/predict_thyroid", methods=["POST"])
def predict_thyroid():

    try:

        age = float(request.form["age"])
        tsh = float(request.form["tsh"])
        t3 = float(request.form["t3"])
        t4 = float(request.form["t4"])
        nodule = float(request.form["nodule"])
        gender = float(request.form["gender"])

        country_india = float(
            request.form["country_india"]
        )

        ethnicity_asian = float(
            request.form["ethnicity_asian"]
        )

        family_history = float(
            request.form["family_history"]
        )

        radiation = float(
            request.form["radiation"]
        )

        iodine = float(
            request.form["iodine"]
        )

        smoking = float(
            request.form["smoking"]
        )

        obesity = float(
            request.form["obesity"]
        )

        diabetes = float(
            request.form["diabetes"]
        )

        cancer_low = float(
            request.form["cancer_low"]
        )

        cancer_medium = float(
            request.form["cancer_medium"]
        )

        features = np.array([[

            age,
            tsh,
            t3,
            t4,
            nodule,
            gender,

            0, 0, 1, 0, 0, 0, 0, 0, 0,

            ethnicity_asian,
            0, 0, 0,

            family_history,
            radiation,
            iodine,
            smoking,
            obesity,
            diabetes,
            cancer_low,
            cancer_medium

        ]])

        prediction = thyroid_model.predict(
            features
        )

        if prediction[0] == 1:

            result = (
                "⚠️ High Risk of Thyroid Disease Detected"
            )

        else:

            result = (
                "✅ Low Risk of Thyroid Disease"
            )

        return render_template(
            "thyroid.html",
            prediction_text=result
        )

    except Exception as e:

        return render_template(
            "thyroid.html",
            prediction_text=f"Error: {e}"
        )


# ============================================================
# STROKE PREDICTION
# ============================================================

@app.route("/predict_stroke", methods=["POST"])
def predict_stroke():

    try:

        age = float(request.form["age"])

        hypertension = float(
            request.form["hypertension"]
        )

        heart = float(
            request.form["heart_disease"]
        )

        glucose = float(
            request.form["glucose"]
        )

        bmi = float(
            request.form["bmi"]
        )

        gender_male = float(
            request.form["gender_male"]
        )

        gender_other = float(
            request.form["gender_other"]
        )

        married = float(
            request.form["married"]
        )

        never_worked = float(
            request.form["never_worked"]
        )

        private = float(
            request.form["private"]
        )

        self_employed = float(
            request.form["self_employed"]
        )

        children = float(
            request.form["children"]
        )

        urban = float(
            request.form["urban"]
        )

        former_smoked = float(
            request.form["former_smoked"]
        )

        never_smoked = float(
            request.form["never_smoked"]
        )

        smokes = float(
            request.form["smokes"]
        )

        features = np.array([[

            age,
            hypertension,
            heart,
            glucose,
            bmi,
            gender_male,
            gender_other,
            married,
            never_worked,
            private,
            self_employed,
            children,
            urban,
            former_smoked,
            never_smoked,
            smokes

        ]])

        prediction = stroke_model.predict(
            features
        )

        if prediction[0] == 1:

            result = "⚠️ High Risk of Stroke Detected"

        else:

            result = "✅ Low Risk of Stroke"

        return render_template(
            "stroke.html",
            prediction_text=result
        )

    except Exception as e:

        return render_template(
            "stroke.html",
            prediction_text=f"Error: {e}"
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)