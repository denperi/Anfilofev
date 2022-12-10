import pandas as pd
from concurrent import futures


def begin_processes(args):
    vac_name = args[0]
    year = args[1]

    data1 = pd.read_csv(f'chunks\\chunk_{year}.csv')
    data1.loc[:, 'salary'] = data1.loc[:, ['salary_from', 'salary_to']].mean(axis=1)
    data_vac = data1[data1["name"].str.contains(vac_name)]
    salary_year = {year: []}
    vacancy_year = {year: 0}
    vacancy_salary = {year: []}
    vac_count = {year: 0}
    salary_year[year] = int(data1['salary'].mean())
    vacancy_year[year] = len(data1)
    vacancy_salary[year] = int(data_vac['salary'].mean())
    vac_count[year] = len(data_vac)
    return [salary_year, vacancy_year, vacancy_salary, vac_count]


if __name__ == "__main__":

    class InputData:
        def __init__(self):
            self.name_file = input("Введите название файла: ")
            self.name_vacancy = input("Введите название профессии: ")


    class CreateCSV:
        def __init__(self, name_file):
            self.data = pd.read_csv(name_file)
            self.data["years"] = self.data["published_at"].apply(lambda date: int(date[:4]))
            self.all_years = list(self.data["years"].unique())
            for year in self.all_years:
                data = self.data[self.data["years"] == year]
                data.iloc[:, :6].to_csv(f"chunks\\chunk_{year}.csv", index=False)


    def dict_sorted(dict):
        output_dict = {}
        sort_dict = sorted(dict)
        for key in sort_dict:
            output_dict[key] = dict[key]
        return output_dict


    def dict_sorted_area(dict):
        sorted_tuples = sorted(dict.items(), key=lambda elem: elem[1], reverse=True)[:10]
        sorted_dict = {k: v for k, v in sorted_tuples}
        return sorted_dict


    input = InputData()
    file_name, vac = input.name_file, input.name_vacancy
    create_csv = CreateCSV(file_name)
    data = create_csv.data
    years = create_csv.all_years

    data["published_at"] = data["published_at"].apply(lambda date: int(date[:4]))
    data['salary'] = data.loc[:, ['salary_from', 'salary_to']].mean(axis=1)

    vacancies = len(data)
    data["count"] = data.groupby("area_name")['area_name'].transform("count")
    data3 = data[data['count'] >= 0.01 * vacancies]
    city_list = list(data3["area_name"].unique())

    sals_year = {}
    vacs_year = {}
    vacancy_salary = {}
    vac_count = {}
    sal_area = {}
    vac_area = {}

    for city in city_list:
        dataframe_s = data3[data3['area_name'] == city]
        sal_area[city] = int(dataframe_s['salary'].mean())
        vac_area[city] = round(len(dataframe_s) / len(data), 4)

    process_exe = futures.ProcessPoolExecutor()
    for year in years:
        args = (vac, year)
        list = process_exe.submit(begin_processes, args).result()
        sals_year.update(list[0])
        vacs_year.update(list[1])
        vacancy_salary.update(list[2])
        vac_count.update(list[3])

    print("Динамика уровня зарплат по годам:", dict_sorted(sals_year))
    print("Динамика количества вакансий по годам:", dict_sorted(vacs_year))
    print("Динамика уровня зарплат по годам для выбранной профессии:", dict_sorted(vacancy_salary))
    print("Динамика количества вакансий по годам для выбранной профессии:", dict_sorted(vac_count))
    print("Уровень зарплат по городам (в порядке убывания):", dict_sorted_area(sal_area))
    print("Доля вакансий по городам (в порядке убывания):", dict_sorted_area(vac_area))