import xgboost as xgb
import pandas as pd

booster = xgb.Booster()
booster.load_model()

def query_ml_model(age_range, tourist_volume, is_one_way, is_citizen):
    one_way_duration = 12.5
    one_way_distance = 1.65
    round_duration = 25
    round_distance = 3.3
    one_way_dataframe =  pd.DataFrame({"duration": [one_way_duration], "distance": [one_way_distance], "snow": [0],
                            "is_nature":[0], "type_of_trip": [1], "is_citizen": [is_citizen], "age_range": [age_range],
                            "tourist_volume_of_cable_car": [tourist_volume]})
    round_dataframe =  pd.DataFrame({"duration": [round_duration], "distance": [round_distance], "snow": [0],
                            "is_nature":[0], "type_of_trip": [0], "is_citizen": [is_citizen], "age_range": [age_range],
                            "tourist_volume_of_cable_car": [tourist_volume]})
    if (is_one_way == 1):
        return booster.predict(one_way_dataframe)
    else:
        return booster.predict(round_dataframe)
    