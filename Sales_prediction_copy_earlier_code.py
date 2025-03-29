import numpy as np
import pandas as pd
import sklearn
import pickle
from flask import Flask, render_template, request, jsonify

with open("Predict_Sales_Cost_MLmodel_LR.pickle", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
#API endpoint

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/submit", methods=["GET", "POST"])
def submit_form():
    if request.method == "GET":
        return "I will make the prediction for Sales Price!, Thanks for visiting the website :)"        

    else:
        #POST request along with data#+
        sales_req = request.get_json(force=True) #Force ensure json parsing

        #define mapping#-
        # define mapping#+
        mappings = {
            "Region_Code": {"R1": 0, "R2": 1, "R3": 2,  "R4": 3},
            "Location_Type": {"L1": 0, "L2": 1, "L3": 2,  "L4": 3, "L5":4},
            "Store_Type": {"S1": 0, "S2": 1, "S3": 2,  "S4": 3},
            }
        

        user_inputs = {}
        for key, mapping in mappings.items():
            if key in sales_req and sales_req[key] in mapping:
                user_inputs[key] = mapping[sales_req[key]]
            else:
                return jsonify({"error": f"Invalid value for {key}"}), 400


        Region_Code = user_inputs["Region_Code"] 
        Location_Type = user_inputs["Location_Type"] 
        Store_Type = user_inputs["Store_Type"]
        
        Holiday = 0 if sales_req.get("Holiday") == 1 else 1
        Discount = 0 if sales_req.get("Discount") == "Yes" else 1
        Order = sales_req.get("Order", 0)

        
        # Prepare input data for the model
        input_data = [
            [Region_Code, 
            Location_Type, 
            Store_Type, 
            Holiday, 
            Discount, 
            Order]
            ]
       

        print("Input Data:", input_data, flush=True)

        #Make Prediction
        result = model.predict(input_data)[0] #Extract single value
        
        print("Predicted Results:", result, flush=True)

        #Return JSON response
        #return jsonify({"Predicted Sales Price": round(result,0)})
        
        cont = {
            "Region_Code": Region_Code,
            "Location_Type": Location_Type,
            "Store_Type": Store_Type,
            "Holiday": Holiday,
            "Discount": Discount,
            "Order": Order
            #"prediction": result[0]
            }
        
        return render_template("result.html", **cont)



if __name__ == "__main__":
    app.run(debug=True)    