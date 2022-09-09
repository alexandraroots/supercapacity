import pandas as pd
from ml import simulated_annealing
# from ml import simulated_annealing.
import numpy as np
from ml.income_classifier.model import Model

BORDERS_PLOT = {
    "Temperature_1": [80, 200],
    "Time_1": [1, 24],
    # "Velo": [1, 10],
    "Temperature_2": [200, 500],
    "Time_2": [1, 5],
    "Volume_solvent": [10, 500],
    "Density": [1, 70],
    "Mass_Reagent_2": [1, 10000]
    # "": ,
}
ORDER_INDEX = {"Temperature_1": 0, "Time_1": 1, "Temperature_2": 2,
               "Time_2": 3, "Mass_Reagent_2": 4, "Volume_solvent": 5, "Density": 6}


class Dummy:
    def __init__(self):
        path_to_artifacts = "../../research/"
        # self.values_fill_missing =  joblib.load(path_to_artifacts + "train_mode.joblib")
        # self.encoders = joblib.load(path_to_artifacts + "encoders.joblib")
        # self.model = joblib.load(path_to_artifacts + "random_forest.joblib")
        # self.model = lambda x: np.random.randint(900, 1200)
        # print("Init")
        self.model = Model()

    def preprocessing(self, input_data):  # we will get data in expected format here
        # x = {'Temperature_1': [120, 160], 'Time_1': 12, 'Velocity': 2, 'Temperature_2': [350, 500], 'Time_2': 2,
        #      'Base': 'Urea',
        #      'Measure_1': 'mmol', 'Mass_Base': 100, 'Reagent_1': 'Ni(NO3)2-6H2O', 'Measure_2': 'mmol',
        #      'Mass_Reagent_1': 100,
        #      'Reagent_2': 'Co(NO3)2-6H2O', 'Measure_3': 'mmol', 'Mass_Reagent_2': 100, 'Volume_solvent': 70,
        #      'Density': 70}

        order_params = ["Temperature_1", "Time_1", "Temperature_2",
                        "Time_2",
                        "Base", "Mass_Reagent_2", "Reagent_1",
                        "Reagent_2", "Volume_solvent", "Density"]
        print(input_data)
        up_borders = []
        low_borders = []
        params = dict()
        for key in order_params:
            val = input_data[key]
            if type(val) is str:
                params[key] = val
                continue
            if type(val) is int:
                # print("HERE")
                low_borders.append(BORDERS_PLOT[key][0])
                up_borders.append(val)
                # print("HERE_1")

            else:
                low_borders.append(val[0])
                up_borders.append(val[1])
        # print(borders)
        print(params)
        simulated_annealing.function_call.params = params
        borders = np.array([low_borders, up_borders])
        print(borders)
        return borders, params
        # return/ input_data

    def predict(self, input_data):
        # return self.model.predict_proba(input_data)
        # print("start")
        res = self.model.predict(input_data)
        # print("End")
        return res
        # return 768

    def model_rename(self, input_data):
        input_data = [input_data["Temperature_1"], input_data["Time_1"], input_data["Temperature_2"],
                      input_data["Time_2"], input_data["Mass_Reagent_2"], input_data["Volume_solvent"],
                      input_data["Density"], input_data["Base"], input_data["Reagent_1"], input_data["Reagent_2"]]
        return input_data

    def model_rename_predict(self, input_data):
        input_data = [input_data["Temperature_1"][0], input_data["Time_1"], input_data["Temperature_2"][0],
                      input_data["Time_2"], input_data["Mass_Reagent_2"], input_data["Volume_solvent"],
                      input_data["Density"], input_data["Base"], input_data["Reagent_1"], input_data["Reagent_2"]]
        return input_data

    def optimization(self, input_data):
        simulated_annealing.function_call.model = self.model
        start = np.mean(input_data, axis=0)
        print(start)

        pos, steps = simulated_annealing.optimize(simulated_annealing.function_call, start, input_data)
        print("result", pos)
        return pos, simulated_annealing.function_call(pos)

    def postprocessing(self, output_data, target):
        params = ["Temperature_1", "Time_1", "Temperature_2",
                  "Time_2", "Mass_Reagent_2", "Volume_solvent", "Density"]
        # if input_data > 0.5:
        #     label = ">no succ"
        if target == "predict":
            label = "prediction"
            response = {"capacity": output_data[0],
                        "label": label, "status": "OK"}
            # return
        else:
            label = "optimization"
            response = {"parameters": {key: val for key, val in zip(params, output_data[0])},
                        "capacity": output_data[1],
                        "label": label, "status": "OK"}

        return response

    def plot_creator(self, response, input_data):
        # print("Here")

        axis = input_data["Axis_x"]

        # print(axis)
        dotes = 10
        if input_data["target"] == "predict":
            step = (BORDERS_PLOT[axis][1] - BORDERS_PLOT[axis][0]) / dotes
            response["ax_x"] = [BORDERS_PLOT[axis][0] + i * step for i in range(dotes + 1)]
            data = self.model_rename_predict(input_data)

        # response["ax_x"] = [i for i in range(50)]
        else:
            # print("here input:", input_data)
            if type(input_data[axis]) is int:
                step = (BORDERS_PLOT[axis][0] - input_data[axis])/dotes
                response["ax_x"] = [input_data[axis] + i * step for i in range(dotes + 1)]

            else:
                step = (input_data[axis][1] - input_data[axis][0]) / dotes
                response["ax_x"] = [input_data[axis][0] + i * step for i in range(dotes + 1)]
            #
            # print("Here response", response)
            data = self.model_rename(response["parameters"] | {"Base": simulated_annealing.function_call.params["Base"],
                                                               "Reagent_1": simulated_annealing.function_call.params[
                                                                   "Reagent_1"],
                                                               "Reagent_2": simulated_annealing.function_call.params[
                                                                   "Reagent_2"]})
            # print("data acc")
        result = []
        # print("Here_2")

        for x in response["ax_x"]:
            # print("Here_3")

            data[ORDER_INDEX[axis]] = x
            # print("Here_4")
            # print(data)
            # print(self.model.predict(data))
            result.append(self.model.predict(data)[0])
            # print("Here_5")

        response["ax_y"] = result
        # print("the end")
        return response

    def compute_prediction(self, input_data):
        try:
            target = input_data["target"]
            if target == "predict":
                reworked_data = self.model_rename_predict(input_data)
                prediction = self.predict(reworked_data)

            else:
                # print("begin")
                borders, params = self.preprocessing(input_data)
                # prediction = self.predict(input_data)[0]  # only one sample
                # prediction = self.predict(input_data)  # only one sample
                prediction = self.optimization(borders)  # only one sample
            prediction = self.postprocessing(prediction, target)

            # prediction["ax_x"] = [i for i in range(50)]
            prediction = self.plot_creator(prediction, input_data)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
