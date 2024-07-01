import pandas as pd

if __name__ == "__main__":
    df = pd.read_json("https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json")
    df.to_csv("data/province.csv", index=False)
