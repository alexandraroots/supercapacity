from helpers import *
import pickle
import pandas as pd


class Model:
    def __init__(self):
        self.model = pickle.load(open("data/xgb_fp.pkl", "rb"))

    def get_borders(self):
        return 'Не ебу'

    def preproc(self, input):
        descriptors = []
        for i in [4, 6, 7]:
            descriptors.extend(morgan_fingerprint(mol_name_to_smiles(input[i])))
        preproc_tmp = [input[0], input[1], input[2], input[3], input[5], input[8], input[9]]
        preproc_tmp = dict(zip(['temperature_1', 'time_1', 'temperature_2', 'time_2',
                                'm_salt_2', 'volume_solvent', 'density'], preproc_tmp))
        for i, d in enumerate(descriptors):
            preproc_tmp[str(i)] = d
        return pd.DataFrame(preproc_tmp, index=[0])

    def predict(self, input):
        return self.model.predict(self.preproc(input))


if __name__ == "__main__":
    tmp = [100, 2, 350, 4, 'urea', 2, 'Nickel(II) nitrate hexahydrate', 'Nickel(II) nitrate hexahydrate', 20, 10]
    model = Model()
    print(model.predict(tmp))
