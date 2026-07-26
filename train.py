import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ===========================
# Đọc dữ liệu
# ===========================

df = pd.read_csv("creditcard_processed.csv")

print("Kích thước dữ liệu:")
print(df.shape)

# ===========================
# Tách dữ liệu
# ===========================

X = df.drop("Class", axis=1)

y = df["Class"]

# ===========================
# Chia train test
# ===========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTrain:", X_train.shape)
print("Test :", X_test.shape)

# ===========================
# Chuẩn hóa
# ===========================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

# ===========================
# Logistic Regression
# ===========================

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight="balanced"
)

# ===========================
# Train
# ===========================

model.fit(X_train, y_train)

print("\nTrain thành công!")

# ===========================
# Predict
# ===========================

y_pred = model.predict(X_test)

# ===========================
# Accuracy
# ===========================

print("\nAccuracy")

print(accuracy_score(y_test, y_pred))

# ===========================
# Confusion Matrix
# ===========================

print("\nConfusion Matrix")

print(confusion_matrix(y_test, y_pred))

# ===========================
# Classification Report
# ===========================

print("\nClassification Report")

print(classification_report(y_test, y_pred))

# ===========================
# Lưu model
# ===========================

joblib.dump(model, "models/fraud_model.pkl")

joblib.dump(scaler, "models/scaler.pkl")

print("\nĐã lưu model!")

print("models/fraud_model.pkl")

print("models/scaler.pkl")