from ml.income_classifier.helpers import *
import pickle
import pandas as pd


class Model:
    def __init__(self):
        self.model = pickle.load(open("ml/income_classifier/xgb_fp.pkl", "rb"))

    def get_borders(self):
        return 'Не ебу'

    def preproc(self, input):
        # print(input)
        descriptors = []
        for i in input[7:]:
            descriptors.extend(morgan_fingerprint(mol_name_to_smiles(i)))
        preproc_tmp = input[:7]
        preproc_tmp = dict(zip(['temperature_1', 'time_1', 'temperature_2', 'time_2',
                                'm_salt_2', 'volume_solvent', 'density'], preproc_tmp))
        for i, d in enumerate(descriptors):
            preproc_tmp[str(i)] = d
        # print("finish_model")

        return pd.DataFrame(preproc_tmp, index=[0])

    def predict(self, input):
        data = self.preproc(input)
        # print("model data", data)
        res = self.model.predict(data)
        # print(res)
        return res


if __name__ == "__main__":
    tmp = [100, 2, 350, 4, 2, 20, 10, 'urea', 'Nickel(II) nitrate hexahydrate', 'Nickel(II) nitrate hexahydrate']
    model = Model()
    print(model.predict(tmp))
