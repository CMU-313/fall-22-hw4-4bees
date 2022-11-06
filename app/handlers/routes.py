import this
from flask import Flask, jsonify, request
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


    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        G1 = request.args.get('G1')
        G2 = request.args.get('G2')
        failures = request.args.get('failures')
        studytime = request.args.get('studytime')
        data = [[G1], [G2], [failures], [studytime]]
        query_df = pd.DataFrame({
            'G1': pd.Series(G1),
            'G2': pd.Series(G2),
            'failures': pd.Series(failures),
            'studytime': pd.Series(studytime)
        })
        # query = pd.get_dummies(query_df)
        prediction = clf.predict(query_df)
        print(prediction)
        return jsonify(np.ndarray.item(prediction))

# sample input
# http://127.0.0.1:5000/predict?G1=17&G2=19&failures=3&studytime=2