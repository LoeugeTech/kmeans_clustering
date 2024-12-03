import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load the saved model
kmeans = joblib.load("model/model.pkl")

# Instantiate the FastAPI app
app = FastAPI(
    title="K-Means Clustering API",
    description="An AP for clustering customer data based on annual income and spending score using K-Means Clustering.",
    version="1.0.0"
)

# Define the input data schema

class CustomerData(BaseModel):
    annual_income: float
    spending_score: float

@app.post(
    "/predict",
    summary="Predict customer cluster",
    description = "Predict whether the customer belongs to cluster 0,1,2,3,4",
    tags=["Prediction"]
)
def predict_cluster(data: CustomerData):
    #Prepare the input for prediction
    input_data = np.array([[data.annual_income, data.spending_score]])
    cluster = kmeans.predict(input_data)[0]

    # Map cluster numbers to letters
    cluster_mapping = {
        0: "Prudent Spenders",
        1: "Generous Spenders",
        2: "Extravagant Spenders",
        3: "Wise Spenders",
        4: "Loose Spenders"
    }
    cluster_label = cluster_mapping.get(cluster, "Unknown Cluster")

    return {"cluster": cluster_label}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)