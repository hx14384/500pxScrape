#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

This program offers basical util.
Author: JeffXu
Last edited: Feb 2019
"""

import openpyxl

def ensureXlSuffix(path):
    array = path.split('.')
    if len(array) > 1:
        suffix = array[len(array) - 1]    
        if suffix != "xlsx":
            if path[len(path) - 1] == '.':
                return path + "xlsx"
            else:
                return path + ".xlsx"
        else:
            return path
    else:
        if len(path) == 0:
            return path
        else:
            return path + ".xlsx"

def writerow2xl(ws, rowIndex, rowArray):
    #write one row to xls
    for i in range(len(rowArray)):
        colIndex = i + 1
        ws.cell(row=rowIndex, column=colIndex).value = rowArray[i]
