import pandas as pd

def load_rubric(path):
    df = pd.read_excel(path, header=None)

    # find 'Overall Rubrics'
    start_row = df[df.apply(lambda r: r.astype(str).str.contains("Overall Rubrics", case=False).any(), axis=1)].index
    if len(start_row) == 0:
        raise ValueError("Could not find 'Overall Rubrics' section.")
    start = start_row[0] + 1

    # grab more rows to avoid merged cell issues
    temp = df.iloc[start:start+12, 1:5]   # B–E columns

    # remove fully empty rows
    temp = temp.dropna(how="all")

    # keep rows with criteria + metric + weightage
    temp = temp[temp[1].notna() & temp[3].notna()]

    temp.columns = ["criteria", "metric", "dummy", "weightage"]
    temp = temp.drop(columns=["dummy"])

    temp["weightage"] = pd.to_numeric(temp["weightage"], errors="coerce")
    temp = temp.dropna(subset=["weightage"])

    # normalize
    total = temp["weightage"].sum()
    temp["weight"] = temp["weightage"] / total

    return temp
