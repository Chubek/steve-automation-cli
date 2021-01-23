from pandas.core.algorithms import mode
from record import Record
from cluster import cluster
import pandas as pd
import ntpath
import os
import functools
import operator
from os.path import abspath
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataParser:

    def __init__(self, file_path, num_clusters):
        self.filepath = abspath(file_path)
        self.df = pd.read_excel(self.filepath)
        self.folder, _ = self.__path_leaf(self.filepath)
        self.num_clusters = num_clusters

    def operate(self, mode):
        print(f"Mode {mode} selected.")
        res = self.__separate_and_cluster()
        return {
            '1': self.__route_day,
            '2': self.__route_day_stopcluster,
            '3': self.__label_one_file,
            '4': self.__all
        }[mode](res)

    def __path_leaf(self, path):
        head, tail = ntpath.split(path)
        return head, tail.split(".")[-2]

    def __route_day(self, res):
        print("Writing file for Route-Day...")

        for r in res:
            print(f"Writing {r['route']}_{r['day']}.xlsx")
            self.__write_excel(r["df"], f"{r['route']}_{r['day'].replace(' ', '_')}_{hash(str(datetime.now()))}")


    def __route_day_stopcluster(self, res):
        print("Writing file for Route-Day-StopCluster...")

        for r in res:          
            for label, group in r["df"].groupby("Label"):
                print(f"Writing label {r['route']}_{r['day']}_{label}.xlsx")
                self.__write_excel(group, f"{r['route']}_{r['day'].replace(' ', '_')}_{label}_{hash(str(datetime.now()))}")

    def __label_one_file(self, res):
        print("Writing into one file...")

        dfs = [r["df"] for r in res]

        self.__write_excel(pd.concat(dfs), f"ALL_{hash(str(datetime.now()))}")

    def __all(self, res):
        self.__route_day(res)
        self.__route_day_stopcluster(res)
        self.__label_one_file(res)

    def __cluster_records(self, records):
        recs = [Record(address, city, province, zipcode, delivery_day).return_val() for address, city, province, zipcode, delivery_day in records]

        labels = cluster(recs, int(self.num_clusters))

        return labels

    def __write_excel(self, df, name):
        try:
            df.to_excel(os.path.join(self.folder, f"{name}.xlsx"))
            print(f"{name}.xlsx saved...")
        except:
            print(f"Error saving file {name}.xlsx... Perhaps a file with the same name exists?")

    def __separate_and_cluster(self):
        print("Starting Separate Data Based on Day and Route...")
        
        routes = ['RT43', 'RT46', 'RT47', 'RT48', 'RT50', 'RT51', 'RT52', 'RT53']
        days = ['DAY 1', 'DAY 2', 'DAY 3', 'DAY 4', 'DAY 5']

        df_comp = [[{"df": self.df[(self.df['Route'] == route) &\
             ((self.df['Week 1'] == day) | (self.df['Week 2'] == day)\
                  | (self.df['Week 3'] == day) | (self.df['Week 4'] == day))],\
                       "day": day, "route": route} for day in days]\
                            for route in routes]
        df_list = functools.reduce(operator.iconcat, df_comp, [])
        df_list = [df for df in df_list if df["df"].shape[0] > int(self.num_clusters)]

        print(f"Seperated into {len(df_list)} dataframes...")
        

        dfs_main = []

        for i, dic in enumerate(df_list):
            print(f"Dataframe {i + 1}")
        
            recs = dic["df"].loc[:, ["Address", "City", "Province", "Postal Code", "Delivery Day"]]

            labels = self.__cluster_records([item for _, item in recs.iterrows()])
 
            dic["df"].loc[:, "Label"] = [f"L{l}_{dic['route']}_{dic['day'].replace(' ', '_')}" for l in labels]

            dfs_main.append({"route": dic['route'], "day": dic['day'], "df": dic["df"].iloc[:, :]})        

            print(f"Clustered into {len(labels)} labels.")



        return dfs_main
    


