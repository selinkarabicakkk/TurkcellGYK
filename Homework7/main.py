from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import datetime as dt

app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


df = pd.read_excel("Online Retail.xlsx")
df.dropna(inplace=True)
df = df[df['Country'] == 'United Kingdom']
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']


analysis_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (analysis_date - x.max()).days,
    "InvoiceNo": "nunique",
    "TotalPrice": "sum"
})
rfm.columns = ["Recency","Frequency","Monetary"]


rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1], duplicates='drop')
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)


X = rfm[["Recency","Frequency","Monetary"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=5, random_state=42)
rfm["Cluster"] = kmeans.fit_predict(X_scaled)

class RFM(BaseModel):
    Recency: float
    Frequency: float
    Monetary: float

@app.post("/predict")
def predict_cluster(input: RFM):
 

    raw = [[input.Recency, input.Frequency, input.Monetary]]
    scaled = scaler.transform(raw)
    cluster = kmeans.predict(scaled)[0]
    return {"cluster": int(cluster)}

@app.get("/")
def read_root():
    return {"message": "RFM Cluster Prediction API — send POST to /predict with Recency, Frequency, Monetary."}
