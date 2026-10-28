#!/usr/bin/env python3
"""CSV analysis with pandas: shape, dtypes, nulls, numeric summary, top values. Usage: csv_analysis.py file.csv [group_col]"""
import sys, json, pandas as pd
def analyze(path, group=None):
    df=pd.read_csv(path)
    out={"file":path,"rows":len(df),"cols":list(df.columns),"dtypes":{c:str(t) for c,t in df.dtypes.items()},
         "nulls":{c:int(v) for c,v in df.isna().sum().items() if v},
         "numeric_summary":df.describe(include="number").round(3).to_dict() if df.select_dtypes("number").shape[1] else {}}
    if group and group in df.columns:
        num=df.select_dtypes("number").columns.tolist()
        if num: out["groupby"]=df.groupby(group)[num].mean(numeric_only=True).round(3).to_dict()
    return out
if __name__=="__main__": print(json.dumps(analyze(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None),indent=2,default=str))
