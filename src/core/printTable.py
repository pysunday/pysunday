# coding: utf-8
from prettytable import PrettyTable

def printTable(titleArr=[], align='', isPrint=True):
    '''
    用于表格打印
        titleArr为表格头
        align为对齐方式
        isPrint为是否打印
    '''
    table = PrettyTable(titleArr)
    if align:
        for title in titleArr:
            table.align[title] = align
    def log(rowArr=[], alone=False):
        if alone: rowArr = [rowArr]
        for row in rowArr:
            table.add_row(row)
        if isPrint: print(table)
        return table
    return log
