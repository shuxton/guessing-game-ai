import pandas as pd
class DataHandler():
    def __init__(self):
        pass

    def read_dataset(self,filename):
        df = pd.read_csv(filename)
        return df


