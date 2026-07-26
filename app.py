from flask import Flask, render_template, request
import pandas as pd
import joblib
import os


# ==========================
# Khởi tạo Flask
# ==========================

app = Flask(__name__)


# ==========================
# Folder upload
# ==========================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# ==========================
# Load Model + Scaler
# ==========================

model = joblib.load(
    "models/fraud_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)



# ==========================
# Trang chủ
# ==========================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



# ==========================
# Predict
# ==========================

@app.route(
    "/predict",
    methods=["POST"]
)

def predict():


    # ----------------------
    # Kiểm tra file
    # ----------------------

    if "file" not in request.files:

        return render_template(
            "index.html",
            error="Please choose a CSV file."
        )


    file = request.files["file"]


    if file.filename == "":

        return render_template(
            "index.html",
            error="No file selected."
        )



    # ----------------------
    # Lưu file
    # ----------------------

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)



    # ----------------------
    # Đọc CSV
    # ----------------------

    try:

        df = pd.read_csv(filepath)


    except Exception as e:


        return render_template(
            "index.html",
            error=f"Cannot read CSV file: {e}"
        )



    # ----------------------
    # Các cột bắt buộc
    # ----------------------

    required_columns = [

        "Time",

        "V1","V2","V3","V4","V5",
        "V6","V7","V8","V9","V10",

        "V11","V12","V13","V14","V15",

        "V16","V17","V18","V19","V20",

        "V21","V22","V23","V24","V25",

        "V26","V27","V28",

        "Amount"

    ]



    missing = [

        col

        for col in required_columns

        if col not in df.columns

    ]



    if missing:


        return render_template(

            "index.html",

            error=f"Missing columns: {missing}"

        )



    # ----------------------
    # Chuẩn bị dữ liệu
    # ----------------------

    X = df[required_columns].copy()



    # ----------------------
    # Scale dữ liệu
    # ----------------------

    X_scaled = scaler.transform(
        X
    )



    # ----------------------
    # Predict
    # ----------------------

    probability = model.predict_proba(
        X_scaled
    )


    prediction = (probability[:,1] >= 0.4).astype(int)



    # ----------------------
    # Thêm kết quả
    # ----------------------

    df["Prediction"] = prediction



    df["Prediction"] = df["Prediction"].map(

        {

            0: "Normal",

            1: "Fraud"

        }

    )



    df["Risk Score (%)"] = (

        probability[:,1] * 100

    ).round(2)



    # ----------------------
    # Dashboard
    # ----------------------

    total = len(df)


    fraud = (

        df["Prediction"] == "Fraud"

    ).sum()


    normal = (

        df["Prediction"] == "Normal"

    ).sum()



    # Hiển thị 100 dòng đầu

    table = df.head(100).to_html(

        classes="table table-striped",

        index=False

    )



    return render_template(

        "index.html",

        total=total,

        fraud=fraud,

        normal=normal,

        table=table

    )



# ==========================
# Run local
# ==========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )