import ROOT
import yaml
import argparse
import os
#from pathlib import Path

file_list = '~/new/wwgamma_5f_NLO_com_1310185_101.root'
df=ROOT.RDataFrame("Events",file_list)
column_list=df.GetColumnNames()
branchList = []

for i in range(0,len(column_list)):
    branchList.append(column_list[i])
#print branchList
x='HLT'
point='.'
filtered_list = []
for elem in  branchList :
    if x in elem and point not in elem:
        filtered_list.append(elem)
print(filtered_list)
