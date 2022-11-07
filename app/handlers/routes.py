import this
from flask import Flask, jsonify, request, Response
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    # @app.errorhandler(404) 
    # def invalid_route(e): 
    #     print("here")
    #     return predict()

    @app.route('/predict', methods=['GET'])
    def predict():
        #use entries from the query string here but could also use json
        g1 = request.args.get('G1')
        g2 = request.args.get('G2')
        studytime = request.args.get('studytime')
        failures = request.args.get('failures')
        data = [g1, g2, studytime, failures]
        if not checkValid(data):
            return Response ("Please provide valid input", status=400)
        query_df = pd.DataFrame({
            'G1': pd.Series(g1),
            'G2': pd.Series(g2),
            'studytime': pd.Series(studytime),
            'failures': pd.Series(failures)
        })
        query = pd.get_dummies(query_df)
        # case on prediction: 0 - not qualified; 1 - qualified 
        prediction = clf.predict(query)
        if int(np.ndarray.item(prediction)) == 0: 
            return jsonify(
                {"variablesUsed": "Variables G1, G2, studytime, and failures used to predict.",
                 "returnMsg": "Applicant is unlikely to succeed."}) 
        else:
            return jsonify(
                {"variablesUsed": "Variables G1, G2, studytime, and failures used to predict.",
                 "returnMsg": "Applicant is likely to succeed."})          

    def checkValid(l : list) -> bool:
        if None in l: return False
        if int(l[0]) < 0 or int(l[0]) > 20: return False
        if int(l[1]) < 0 or int(l[1]) > 20: return False
        if int(l[2]) < 0 or int(l[2]) > 4: return False
        if int(l[3]) < 0 or int(l[3]) > 4: return False
        return True
        
# sample input
# http://127.0.0.1:5000/predict?G1=17&G2=19&failures=3&studytime=2


