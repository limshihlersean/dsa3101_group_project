from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    # To add model logic to get data from database and transform data.
    #data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
    file_path = '../data/bundled_discount.csv'
    data = pd.read_csv(file_path)

    df = pd.DataFrame(data)
    df_json = df.to_json(orient="records")
    return jsonify(df_json)

@app.route('/api/data', methods=['POST'])
def post_data():
    # Here you would process the data and perhaps return a response
    file_path = '../data/bundled_discount.csv'
    data = pd.read_csv(file_path)
    columns_order = data.columns.tolist()
    new_data = request.json

    # Extract data in the correct order
    new_row = [new_data[col] for col in columns_order]

    # Convert the list to a comma-separated string
    new_row_str = ','.join(map(str, new_row))

    with open(file_path, 'a') as file:
        file.write(new_row_str + '\n')

    return jsonify({'status': 'success', 'received_data': new_row_str})

    print("Appending new row:", new_row_str)
    with open(file_path, 'a') as file:
        file.write(new_row_str + '\n')
    print("New row appended")


'''@app.route('/api/data', methods=['PATCH'])  # Changed from POST to PATCH for semantic correctness
def patch_data():
    data = request.json
    item_id = data.get('item_id')  # Assume that the item_id is part of the incoming JSON data

    if item_id in data_store:
        new_value = data.get('value')
        data_store[item_id] = new_value
        return jsonify({'status': 'success', 'updated_data': {item_id: new_value}})
    else:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404'''


