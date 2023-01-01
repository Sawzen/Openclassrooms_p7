from flask import Flask, jsonify, render_template
import pickle as p
import requests
import numpy as np
import pandas as pd

app = Flask(__name__)
modelfile = 'final_prediction.pickle'
model = p.load(open(modelfile, 'rb'))
x_test = p.load(open("X_test", 'rb'))
x_test_scale = p.load(open("X_test_scale", 'rb'))

@app.route('/dashboard/', methods=['GET'])
def dashboard():
    return render_template("dashboard.html")

@app.route('/prediction/<client_id>', methods=['GET'])
def prediction(client_id):
    data = requests.get_json(x_test_scale)
    prediction = np.array2string(model.predict(data))
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    