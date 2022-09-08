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