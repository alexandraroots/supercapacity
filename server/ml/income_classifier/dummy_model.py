import pandas as pd
from ml import simulated_annealing
# from ml import simulated_annealing.
import numpy as np


class Dummy:
    def __init__(self):
        path_to_artifacts = "../../research/"
        # self.values_fill_missing =  joblib.load(path_to_artifacts + "train_mode.joblib")
        # self.encoders = joblib.load(path_to_artifacts + "encoders.joblib")
        # self.model = joblib.load(path_to_artifacts + "random_forest.joblib")
        self.model = lambda x: 12

    def preprocessing(self, input_data):  # we will get data in expected format here
        # x = {'Temperature_1': [120, 160], 'Time_1': 12, 'Velocity': 2, 'Temperature_2': [350, 500], 'Time_2': 2,
        #      'Base': 'Urea',
        #      'Measure_1': 'mmol', 'Mass_Base': 100, 'Reagent_1': 'Ni(NO3)2-6H2O', 'Measure_2': 'mmol',
        #      'Mass_Reagent_1': 100,
        #      'Reagent_2': 'Co(NO3)2-6H2O', 'Measure_3': 'mmol', 'Mass_Reagent_2': 100, 'Volume_solvent': 70,
        #      'Density': 70}
        print(input_data)
        up_borders = []
        low_borders = []
        params = dict()
        for key, val in input_data.items():
            if type(val) is str:
                params[key] = val
                continue
            if type(val) is int:
                low_borders.append(0)
                up_borders.append(val)
            else:
                low_borders.append(val[0])
                up_borders.append(val[1])
        # print(borders)
        print(params)
        borders = np.array([low_borders, up_borders])
        print(borders)
        return borders, params
        # return/ input_data

    def predict(self, input_data):
        # return self.model.predict_proba(input_data)
        return 42

    def optimization(self, input_data):
        simulated_annealing.function_call.model = self.model
        start = np.mean(input_data, axis=0)
        print(start)

        pos, steps = simulated_annealing.optimize(simulated_annealing.function_call, start, input_data)
        print("result", pos)
        return pos, simulated_annealing.function_call(pos)

    def postprocessing(self, input_data):
        params = ["Temperature_1", "Time_1", "Velocity", "Temperature_2", "Time_2", "Mass_Base", "Mass_Reagent_1",
                  "Mass_Reagent_2",
                  "Volume_solvent", "Density"]
        label = "optimization"
        # if input_data > 0.5:
        #     label = ">no succ"
        return {"parameters": {key: val for key, val in zip(params, input_data[0])}, "capacity": input_data[1],
                "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            borders, params = self.preprocessing(input_data)
            # prediction = self.predict(input_data)[0]  # only one sample
            # prediction = self.predict(input_data)  # only one sample
            prediction = self.optimization(borders)  # only one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
