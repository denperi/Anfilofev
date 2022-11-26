import numpy as np
import matplotlib.pyplot as plt

def text_to_str(data):
    if data is None:
        return ""
    data = str(data)
    return data

#salary_D = {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510, 2014: 50658, 2015: 52696, 2016: 62675, 2017: 60935, 2018: 58335, 2019: 69467, 2020: 73431, 2021: 82690, 2022: 91795}
#number_D = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954, 2014: 66837, 2015: 70039, 2016: 75145, 2017: 82823, 2018: 131701, 2019: 115086, 2020: 102243, 2021: 57623, 2022: 18294}
#salary_vac_D = {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960, 2013: 58804, 2014: 62384, 2015: 62322, 2016: 66817, 2017: 72460, 2018: 76879, 2019: 85300, 2020: 89791, 2021: 100987, 2022: 116651}
#number_vac_D = {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990, 2014: 5492, 2015: 5375, 2016: 7219, 2017: 8105, 2018: 10062, 2019: 9016, 2020: 7113, 2021: 3466, 2022: 1115}
#city_salary_D = {'Москва': 76970, 'Санкт-Петербург': 65286, 'Новосибирск': 62254, 'Екатеринбург': 60962, 'Казань': 52580, 'Краснодар': 51644, 'Челябинск': 51265, 'Самара': 50994, 'Пермь': 48089, 'Нижний Новгород': 47662}
#city_int_D = {'Москва': 0.3246, 'Санкт-Петербург': 0.1197, 'Новосибирск': 0.0271, 'Казань': 0.0237, 'Нижний Новгород': 0.0232, 'Ростов-на-Дону': 0.0209, 'Екатеринбург': 0.0207, 'Краснодар': 0.0185, 'Самара': 0.0143, 'Воронеж': 0.0141}

salary_D = {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510, 2014: 50658}
number_D = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954, 2014: 66837}
salary_vac_D = {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960, 2013: 58804, 2014: 62384}
number_vac_D = {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990, 2014: 5492}
city_salary_D = {'Москва': 57354, 'Санкт-Петербург': 46291, 'Новосибирск': 41580, 'Екатеринбург': 41091, 'Казань': 37587, 'Самара': 34091, 'Нижний Новгород': 33637, 'Ярославль': 32744, 'Краснодар': 32542, 'Воронеж': 29725}
city_int_D = {'Москва': 0.4581, 'Санкт-Петербург': 0.1415, 'Нижний Новгород': 0.0269, 'Казань': 0.0266, 'Ростов-на-Дону': 0.0234, 'Новосибирск': 0.0202, 'Екатеринбург': 0.0143, 'Воронеж': 0.014, 'Самара': 0.0133, 'Краснодар': 0.0131}

fig,data = plt.subplots(2, 2)
k2 = salary_vac_D.keys()
x_cord = np.arange(len(salary_D.keys()))
value = city_salary_D
sticks = list(value.keys())
sticks = [label.replace(' ', '\n').replace('-','-\n') for label in sticks]
values = list(value.values())
other = 1 - sum((list(city_int_D.values())))
other_D = {'Другие': other}
other_D.update(city_int_D)
city_int_D = other_D
label = list(city_int_D.keys())
size = list(city_int_D.values())

#1
data[0, 0].bar(x_cord-0.4/2, salary_D.values(), width=0.4, label = 'средняя з/п')
data[0, 0].bar(x_cord+0.4/2, salary_vac_D.values(), width=0.4, label = 'з/п программист')
data[0, 0].set_xticks(x_cord, salary_D.keys())
data[0, 0].set_xticklabels(salary_D.keys(), rotation='vertical', va='top', ha='center')
data[0, 0].set_title('Уровень зарплат по годам')
data[0, 0].grid(True, axis = 'y')
data[0, 0].tick_params(axis='both', labelsize=8)
data[0, 0].legend(fontsize = 8)
#2
data[0, 1].bar(x_cord-0.4/2, number_D.values(), width=0.4, label = 'Количество вакансий')
data[0, 1].bar(x_cord+0.4/2, number_vac_D.values(), width=0.4, label = 'Количество вакансий\nпрограммист')
data[0, 1].set_xticks(x_cord, number_D.keys())
data[0, 1].set_xticklabels(number_D.keys(), rotation='vertical', va='top', ha='center')
data[0, 1].set_title('Количество вакансий по годам')
data[0, 1].grid(True, axis = 'y')
data[0, 1].tick_params(axis='both', labelsize=8)
data[0, 1].legend(fontsize = 8)
#3
data[1, 0].set_title("Уровень зарплат по городам")
data[1, 0].invert_yaxis()
data[1, 0].tick_params(axis='both', labelsize=8)
data[1, 0].set_yticklabels(sticks, fontsize = 6, va='center', ha='right')
data[1, 0].barh(sticks, values)
data[1, 0].grid(True, axis = 'x')
#4
data[1, 1].pie(size, labels=label, textprops={'fontsize': 6})
data[1, 1].axis('scaled')
data[1, 1].set_title("Доля вакансий по городам")

plt.tight_layout()
plt.savefig('graph.png', dpi = 1200)
plt.show()

print("Динамика уровня зарплат по годам: " + text_to_str(salary_D))
print("Динамика количества вакансий по годам: " + text_to_str(number_D))
print("Динамика уровня зарплат по годам для выбранной профессии: " + text_to_str(salary_vac_D))
print("Динамика количества вакансий по годам для выбранной профессии: " + text_to_str(number_vac_D))
print("Уровень зарплат по городам (в порядке убывания): " + text_to_str(city_salary_D))
print("Доля вакансий по городам (в порядке убывания): " + text_to_str(city_int_D))