'''
Copyright {2020} Junyu Chen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


import os
import re
import math
import argparse
import numpy as np
import pandas as pd

def initPlate96():
    class plate_96:
        row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        col = list(range(1, 12+1))
        colNum = len(col)
        rowNum = len(row)
        df = pd.DataFrame(np.nan, index=row, columns=col)
    return plate_96

def initPlate384():
    class plate_384:
        row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
        col = list(range(1, 24+1))
        colNum = len(col)
        rowNum = len(row)
        df = pd.DataFrame(np.nan, index=row, columns=col)
    return plate_384


def sourceGen(df):
    df1 = df.groupby("Gene").count().reset_index()
    df1["NeedWell"] = pd.NaT
    df1["NeedVol"] =  pd.NaT
    #volList = list()
    for i in range(len(df1)):
        #volList.append(df1["Order"][i] * 3 * 5) #samples * 3 replicate * 5 uL primer mix
        df1.loc[i, "NeedVol"] =  df1["Index"][i] * 3 * 5
        df1.loc[i, "NeedWell"] = math.ceil(df1["NeedVol"][i]/(MaxVol - MinVol))
    df2 = df1.sort_values(by=["Index"])
    df2 = df2.rename(columns={"Index": "Num"})
    return df2

def sourceDictGen(source_df, plate):
    source_df = source_df.reset_index()
    sourceDict = dict()
    count = 0
    for i in range(len(source_df)):
        for j in range(source_df["NeedWell"][i]):
            sourceDict[source_df["Gene"][i]+"_"+str(j+1)] = str(plate.row[count]) + str(1)
            count += 1
    return sourceDict

def showSourceLoc(sourceDict, plate):
    df = plate.df
    for key in sourceDict:
        #print(sDict[key])
        index = re.findall(r'(\w+?)(\d+)', sourceDict[key])
        df.loc[index[0][0], int(index[0][1])] = key
    return df


def destinationDictGen(plate):
    destinationDict = dict()
    n = 0
    for num in plate.col:
        for letter in plate.row:
            destinationDict[n] = letter + str(num)
            n += 1
    return destinationDict

def s2d(sourceDict, destinationDict, df):
    df3 = pd.DataFrame()
    columns = ["Index", "Gene", "Source", "Destination", "Vol", "Time"]
    df3 = pd.DataFrame(np.nan, index=range(0, len(df) * 3 *2), columns=columns)
    source_df = pd.DataFrame(sourceDict.items(), columns=['ID', 'Loc'])
    source_df["Vol"] = 40
    s = -1
    d = -1
    num = 1
    vol = 0
    for i in range(len(df3)):
        #how many vol used? count for every source well
        if i % 2 == 0:
            d += 1
        if i % 6 == 0:
            s += 1
        df3.loc[i, "Index"] = str(df["Index"][s])
        df3.loc[i, "Gene"] = str(df["Gene"][s])
        #print(i)
        df3.loc[i, "Time"] = 1
        df3.loc[i, "Source"] = sourceDict[df3.loc[i, "Gene"] + "_" + str(math.ceil(df3.loc[df3["Gene"] == df["Gene"][s]]["Time"].sum() / 16))] # num should changed
        df3.loc[i, "Destination"] = destinationDict[d]
        df3.loc[i, "Vol"] = 2500
    return df3

def desOut(df3):
    col = ["Source Well", "Transfer Volume", "Destination Well", "ID", "Gene"]
    df4 = pd.DataFrame(columns=col)
    df4.loc[:, "Source Well"] = df3["Source"]
    df4.loc[:, "Destination Well"] = df3["Destination"]
    df4.loc[:, "Transfer Volume"] = df3["Vol"]
    df4.loc[:, "ID"] = df3["Index"]
    df4.loc[:, "Gene"] = df3["Gene"]
    return df4

def showLoc(sourceDict, plate):
    df = plate.df
    for key in sourceDict:
        #print(sDict[key])
        index = re.findall(r'(\w+?)(\d+)', key)
        df.loc[index[0][0], int(index[0][1])] = sourceDict[key]
    return df


parser = argparse.ArgumentParser(description='Run Ehcc primer mix')
parser.add_argument('-i', '--input', dest='InFile', type=str, required=True,
                    help="the path of the input csv File")
parser.add_argument('-o', '--output', dest='OutDir', type=str, required=True,
                    help="the output path of reads")
parser.add_argument('-b', '--batch', dest='BatchID', type=str, required=True,
                    help="the output path of reads")
args = parser.parse_args()



#init
InFile = os.path.abspath(args.InFile)
OutDir = os.path.abspath(args.OutDir)
BatchID = str(args.BatchID)
MinVol = 20
MaxVol = 60
plate96 = initPlate96()
plate384 = initPlate384()
destinationDict = destinationDictGen(plate96)


source_df = pd.read_csv(InFile)
source_usage = sourceGen(source_df)
source_usage.to_csv(BatchID +  "_source_vol" + ".csv")

sourceDict = sourceDictGen(source_usage, plate384)
sPlate = showSourceLoc(sourceDict, plate384)
sPlate.to_csv(BatchID + "_source_plate" + ".csv")

s2d_df = s2d(sourceDict, destinationDict, source_df)

s2d_df_out = desOut(s2d_df)
s2d_df_out.to_csv(BatchID + "_source2destination_transfer" + ".csv")

s2d_dict = pd.Series(s2d_df_out["Source Well"].values,index=s2d_df_out["Destination Well"]).to_dict()

s2dPlate = showLoc(s2d_dict, plate96)
s2dPlate.to_csv(BatchID + "_source2destination_plate" + ".csv")