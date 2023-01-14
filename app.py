from flask import Flask, jsonify, render_template
import pickle5 as p
import requests
import numpy as np
import pandas as pd
from sklearn import preprocessing


app = Flask(__name__)
modelfile = 'final_prediction'
model = p.load(open(modelfile, 'rb'))
x_test = p.load(open("X_test", 'rb'))

@app.route('/prediction/<client_id>', methods=['GET'])
def prediction(client_id):
    client_id = int(client_id)
    client_feat = x_test.loc[x_test["SK_ID_CURR"] == client_id]
    client_feat = client_feat.drop(columns ="SK_ID_CURR")
    prediction = np.array2string(model.predict(client_feat))
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)
    