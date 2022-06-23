#!usr/local/bin/python3

from matplotlib import pyplot
from openpyxl import load_workbook

wb = load_workbook('data_analysis_lab.xlsx')
sheet = wb['Data']


def getvalue(x):
    return x.value


years = list(map(getvalue, sheet['A'][1:]))
temp1 = list(map(getvalue, sheet['B'][1:]))
temp2 = list(map(getvalue, sheet['C'][1:]))
act = list(map(getvalue, sheet['D'][1:]))

pyplot.plot(years, temp2, label="Temp")
pyplot.plot(years, act, label="Sun Activity")
pyplot.xlabel('Years')
pyplot.title("Correlation")
pyplot.show()
