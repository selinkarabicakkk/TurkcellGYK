import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "insurance.csv")

print(f"CSV dosyası yolu: {csv_path}")
print(f"Dosya mevcut mu: {os.path.exists(csv_path)}")

try:
    df = pd.read_csv(csv_path)
    print(f"CSV dosyası başarıyla okundu. Boyut: {df.shape}")
except Exception as e:
    print(f"Hata: {e}")
   
    try:
       
        csv_path_alt = os.path.join(os.path.dirname(current_dir), "Homework5", "insurance.csv")
        print(f"Alternatif yol deneniyor: {csv_path_alt}")
        print(f"Alternatif yol mevcut mu: {os.path.exists(csv_path_alt)}")
        df = pd.read_csv(csv_path_alt)
        print(f"CSV dosyası alternatif yoldan okundu. Boyut: {df.shape}")
    except Exception as e2:
        print(f"Alternatif yol hatası: {e2}")
        raise


print("\nVeri seti bilgileri:")
print(df.info())
print("\nEksik veriler:")
print(df.isnull().sum())


missing_cols = df.columns[df.isnull().any()]
for col in missing_cols:
    if df[col].dtype == "object":
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].mean())

print("\nEksik veriler doldurulduktan sonra:")
print(df.isnull().sum())

df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)
print("\nKategorik değişkenler dönüştürüldükten sonra sütunlar:")
print(df.columns.tolist())

df["bmi_smoker"] = df["bmi"] * df["smoker_yes"]
df["age_smoker"] = df["age"] * df["smoker_yes"]

X = df.drop("charges", axis=1)
y = df["charges"]

print(f"\nX şekli: {X.shape}, y şekli: {y.shape}")

try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=24)
    print(f"\nVeri bölündü: X_train: {X_train.shape}, X_test: {X_test.shape}, y_train: {y_train.shape}, y_test: {y_test.shape}")
except Exception as e:
    print(f"Veri bölme hatası: {e}")
    raise

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nLinear Regression modeli eğitiliyor...")
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)

print("Decision Tree modeli eğitiliyor...")
dt = DecisionTreeRegressor(random_state=24)
dt.fit(X_train_scaled, y_train)
y_pred_dt = dt.predict(X_test_scaled)

print("Random Forest modeli eğitiliyor...")
rf = RandomForestRegressor(random_state=24)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)

models = {
    'Linear Regression': lr,
    'Decision Tree': dt,
    'Random Forest': rf
}

metrics = {}
for name, model in models.items():
    y_pred = model.predict(X_test_scaled)
    metrics[name] = {
        'MSE': mean_squared_error(y_test, y_pred),
        'MAE': mean_absolute_error(y_test, y_pred),
        'R2': r2_score(y_test, y_pred)
    }

for name, model in models.items():
    model_path = os.path.join(current_dir, f'{name.lower().replace(" ", "_")}_model.pkl')
    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)
    print(f"{name} modeli kaydedildi: {model_path}")

scaler_path = os.path.join(current_dir, 'scaler.pkl')
with open(scaler_path, 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)
print(f"Scaler kaydedildi: {scaler_path}")

columns_path = os.path.join(current_dir, 'columns.pkl')
with open(columns_path, 'wb') as columns_file:
    pickle.dump(X.columns.tolist(), columns_file)
print(f"Sütun isimleri kaydedildi: {columns_path}")

metrics_path = os.path.join(current_dir, 'metrics.pkl')
with open(metrics_path, 'wb') as metrics_file:
    pickle.dump(metrics, metrics_file)
print(f"Metrikler kaydedildi: {metrics_path}")

print("\nModeller, scaler, sütun isimleri ve metrikler başarıyla kaydedildi!")
print("\nModel Performans Metrikleri:")
for name, metric in metrics.items():
    print(f"\n{name}:")
    print(f"  MSE:  {metric['MSE']:.2f}")
    print(f"  MAE:  {metric['MAE']:.2f}")
    print(f"  R2:   {metric['R2']:.4f}") 