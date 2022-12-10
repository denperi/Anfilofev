import pandas as pd

filename = "vacancies_by_year.csv"
data1 = pd.read_csv(filename)
date = lambda date: int(date[:4])
data1["years"] = data1["published_at"].apply(date)
years_unique = list(data1["years"].unique())

for year in years_unique:
    data2 = data1[data1["years"] == year]
    data2.iloc[:, :6].to_csv(f"chunks\\chunk_{year}.csv", index=False)