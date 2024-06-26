import catboost as cb
import pandas as pd
import joblib
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

def query_ml_model(age_range, tourist_volume, is_one_way, is_citizen):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "predict_cable_car_prices.json")
    scaler_path = os.path.join(current_dir, "tourist_volume_scaler.pkl")
    booster = cb.CatBoostRegressor()
    booster.load_model(model_path)
    tourist_volume_scaler = joblib.load(scaler_path)
    one_way_duration = 12.5
    one_way_distance = 1.65
    round_duration = 25
    round_distance = 3.3
    tourist_volume = tourist_volume_scaler.transform(np.array(tourist_volume).reshape(-1, 1)).flatten()[0]
    one_way_dataframe =  pd.DataFrame({"duration": [one_way_duration], "distance": [one_way_distance], "snow": [0],
                            "is_nature":[0], "type_of_trip": [1], "is_citizen": [is_citizen], "age_range": [age_range],
                            "tourist_volume_of_cable_car": [tourist_volume]})
    round_dataframe =  pd.DataFrame({"duration": [round_duration], "distance": [round_distance], "snow": [0],
                            "is_nature":[0], "type_of_trip": [0], "is_citizen": [is_citizen], "age_range": [age_range],
                            "tourist_volume_of_cable_car": [tourist_volume]})
    
    if (is_one_way == 1):
        price = booster.predict(one_way_dataframe)[0]
    else:
        price = booster.predict(round_dataframe)[0]
    if (price < 1):
        return 1
    return round(price, 2)
    