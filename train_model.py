import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1️⃣ Load Dataset
dataset_path = "cybersecurity_dataset.csv"  # Ensure the dataset is present
try:
    data = pd.read_csv(dataset_path)
except FileNotFoundError:
    print(f"❌ Error: Dataset file '{dataset_path}' not found!")
    exit()

# 2️⃣ Feature Engineering
X = data.drop(columns=["attack_type", "source_ip"])  # Drop non-numeric column
y = data["attack_type"]  # Labels

# 3️⃣ Encode Labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# 4️⃣ Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️⃣ Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6️⃣ Save the Model & Label Encoder
model_filename = "cybersecurity_model.pkl"
encoder_filename = "label_encoder.pkl"

joblib.dump(model, model_filename)
joblib.dump(label_encoder, encoder_filename)

print(f"✅ Model training completed and saved as {model_filename}")
print(f"✅ Label encoder saved as {encoder_filename}")
