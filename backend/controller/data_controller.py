from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # To add model logic to get data from database and transform data.
    data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
    df = pd.DataFrame(data)
    df_json = df.to_json(orient="records")
    return jsonify(df_json)
