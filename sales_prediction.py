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
    return "Welcome to the Sales"
    #return render_template("index.html")

@app.route("/submit", methods=["GET", "POST"])
def submit_form():
    if request.method == "GET":
        return ("I will make the prediction for Insurance Price!, Thanks for visiting the website :)")
        
    else:
        #POST request along with data
        sales_req = request.get_json()

        #define mapping
        mappings = {
            "region": {"R1": 0, "R2": 1, "R3": 2,  "R4": 3},
            "location": {"L1": 0, "L2": 1, "L3": 2,  "L4": 3},
            "store": {"S1": 0, "S2": 1, "S3": 2,  "S4": 3},
            }

        user_inputs = {}
        for key, mapping in mappings.items():
            selected_str = sales_req.get(key, None)
            if selected_str in mapping:
                user_inputs(key) = mapping[selected_str]
            else:
                return jsonify({"error": f"Invalid value for {key}"}), 400


        holiday = sales_req("Holiday")
        if holiday == 1:
            holiday = 0
        else:
            holiday = 1

        
        discount = sales_req("Discount")
        if discount == "Yes":
            discount = 0
        else:
            discount = 1

        
        order = sales_req("#Order")


        input_data = [
            user_inputs["region"], user_inputs["location"], user_inputs["store"], holiday, discount, order 
                      ]
        print("Input Data:", input_data, flush=True)

        try:
            result = model.predict([input_data])
            predicted_price = round(result[0], 2)
        except Exception as e:
            return jsonify({"error": f"Prediction error: {str(e)}"}), 500
        
        
        print("Predicted Results:", result, Flush=True)

        return jsonify({"Predicted Sales Price": predicted_price})    

'''
    if __name__ = "__main__":
        app.run(debug=True)    

        cont = {
            "region" = region,
            "location" = location,
            "store" = store,
            "holiday" = holiday,
            "discount" = discount,
            "order" = order
            }

        return render_template("result.html", **cont) 
'''