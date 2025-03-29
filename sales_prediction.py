import joblib
import numpy as np
import pandas as pd
#import sklearn
import pickle
from flask import Flask, render_template, request, jsonify

with open("Predict_Sales_Cost_MLmodel_LR.pickle", "rb") as f:
    model = pickle.load(f)



#Apply Encoders_start here


#Load Encoders
with open("encoders.pkl", "rb") as f:
     encoders = pickle.load(f)

# Validate encoders
if not isinstance(encoders, dict):
    raise ValueError("Encoders file is not loaded correctly!")


store_encoder = encoders.get("store_enc", None)
location_encoder = encoders.get("location_enc", None)
region_encoder = encoders.get("region_enc", None)


print("Encoders loaded:", encoders.keys())  # Check what was loaded
print("LabelEncoder Classes (Unique Categories):", store_encoder.classes_)  # Check unique categories
print("LabelEncoder Classes (Unique Categories):", location_encoder.classes_)  # Check unique categories
print("LabelEncoder Classes (Unique Categories):", region_encoder.classes_)  # Check unique categories



# Load the scaler
scaler = joblib.load("scaler.pkl")



app = Flask(__name__)
#API endpoint

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_form():
        #POST request along with data
        sales_req = request.form #Force ensure json parsing
        print("🚀 Received Form Data:", dict(sales_req), flush=True)
        
        # Encode store_category
        store = sales_req.get("store_enc", "").strip()
        if store is None or store not in store_encoder.classes_:
            return jsonify({"error": "Invalid or missing 'store_enc'"}), 400
        encoded_store = store_encoder.transform([store])[0]
        
        
        # Encode location_category
        location = sales_req.get("location_enc", "").strip()
        if location is None or location not in location_encoder.classes_:
            return jsonify({"error": "Invalid or missing 'location_enc'"}), 400
        encoded_location = location_encoder.transform([location])[0]
        
        # Encode location_category
        region = sales_req.get("region_enc", "").strip()
        if region is None or region not in region_encoder.classes_:
            return jsonify({"error": "Invalid or missing 'region_enc'"}), 400
        encoded_region = region_encoder.transform([region])[0]
        
        print(f"Store: '{store}', Location: '{location}', Region: '{region}'", flush=True)  # Debugging print
        
        


        # Check if values are valid
        if store not in store_encoder.classes_:
            print(f"Invalid store_enc: {store}. Expected one of {list(store_encoder.classes_)}", flush=True)
            return jsonify({"error": f"Invalid 'store_enc': {store}. Expected: {list(store_encoder.classes_)}"}), 400

        if location not in location_encoder.classes_:
            print(f"Invalid location_enc: {location}. Expected one of {list(location_encoder.classes_)}", flush=True)
            return jsonify({"error": f"Invalid 'location_enc': {location}. Expected: {list(location_encoder.classes_)}"}), 400

        if region not in region_encoder.classes_:
            print(f"Invalid region_enc: {region}. Expected one of {list(region_encoder.classes_)}", flush=True)
            return jsonify({"error": f"Invalid 'region_enc': {region}. Expected: {list(region_encoder.classes_)}"}), 400



        Holiday = int(sales_req.get("Holiday", 0))
        Discount = 1 if sales_req.get("Discount") == "Yes" else 0
        Order = int(sales_req.get("Order", 0))


        
        
        # Prepare input data for the model
        input_data = [
            encoded_store, 
            encoded_location, 
            encoded_region,  
            Holiday, 
            Discount, 
            Order]
            
       

        print("Input Data:", input_data, flush=True)


        # preprocessed data
        features_scaled = scaler.transform([input_data]) # Convert list to 2D array

        #Make Prediction
        predictions = model.predict(features_scaled) #Extract single value
        
        #check the shape before indexing
        if predictions.ndim == 1:
            result = predictions[0]  # If 1D array
        else:
            result = predictions[0][0]  # If 2D array
 
        
        #return render_template("result.html", **cont)

        # Pass actual and predicted values to template
        return render_template("result.html",
                            Region_Code=region,
                            Location_Type=location,
                            Store_Type=store,
                            Holiday=Holiday,
                            Discount=Discount,
                            Order=Order,
                            result=round(result, 0))

            
        


if __name__ == "__main__":
    app.run(debug=True)    
    
       