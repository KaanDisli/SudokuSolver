import requests
import sys

import random
from threading import Thread
import os
from bs4 import BeautifulSoup
from PIL import Image
import io
import pytesseract
import PIL.Image
import cv2

import time

def int(str):
    return (ord(str) - 48)


def str(int):
    return chr(int + 48)




li =[[0,8,0,0,0,0,2,0,0],
     [0,0,0,0,8,4,0,9,0],
     [0,0,6,3,2,0,0,1,0],
     [0,9,7,0,0,0,0,8,0],
     [8,0,0,9,0,3,0,0,2],
     [0,1,0,0,0,0,9,5,0],
     [0,7,0,0,4,5,8,0,0],
     [0,3,0,7,1,0,0,0,0],
     [0,0,8,0,0,0,0,4,0]]

numset = [1,2,3,4,5,6,7,8,9]
l2 =[[0,0,0,0,0,0,0,0,0],
     [4,3,0,0,0,9,7,0,0],
     [0,0,0,0,5,0,0,2,0],
     [0,0,0,0,1,5,0,7,0],
     [0,8,5,6,0,2,4,0,0],
     [0,0,2,0,9,0,0,0,0],
     [1,5,0,8,6,0,0,0,0],
     [2,0,8,0,4,0,0,6,0],
     [0,4,6,0,0,0,0,1,0]]


l4 =[[0,0,6,0,4,0,0,9,7],
     [0,4,0,7,3,0,0,1,0],
     [0,1,7,0,9,2,0,3,0],
     [6,0,0,0,7,0,0,8,0],
     [1,0,5,0,6,0,9,0,3],
     [0,2,0,0,1,0,0,0,6],
     [0,5,0,9,8,0,1,6,0],
     [0,9,0,0,5,6,0,7,0],
     [8,6,0,0,2,0,3,0,0]]
def intersection(list1,list2,list3):
    l = []
    for ele in list1:
        if ele in list2 and ele in list3:
            l.append(ele)
    return l

def list_diff(my_list1, my_list2):
    out = []
    for ele in my_list1:
        if ele not in my_list2:
            out.append(ele)
    return out
def che_row(game,row,col):
    newset = []
    for x in range (9):

         newset.append(game[row][x])
    return list_diff(numset,newset)


def che_col(game,row,col):
    newset = []
    for x in range (9):

         newset.append(game[x][col])
    return list_diff(numset,newset)


def che_box(game,row,col):
    ilk3 = [0,1,2]
    orta3= [3,4,5]
    son3 = [6,7,8]
    var1 = []
    var2 = []
    hepsi = [ilk3,orta3,son3]
    newset = []
    for x in hepsi:
        for h in x:
            if row == h:
                var1 = x
            if col == h:
                var2 = x
    for x in var1:
        for y in var2:
            newset.append(game[x][y])
    return list_diff(numset,newset)

def values(game,row,column):
    newset = []
    val1 = che_box(game, row, column)
    val2 = che_col(game, row, column)
    val3 = che_row(game, row, column)
    newset = intersection(val1,val2,val3)
    return newset


def primarysolver(game):
    newset = []

    for x in range (9):
        for y in range (9):

            if game[x][y] == 0 and len(values(game,x,y)) ==1 :
                game[x][y] = values(game,x,y)[0]


                primarysolver(game)

    return game

l3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 3, 1, 2, 8, 9, 7, 5, 6], [0, 0, 0, 0, 5, 0, 0, 2, 0], [0, 0, 0, 0, 1, 5, 0, 7, 0], [0, 8, 5, 6, 0, 2, 4, 0, 0], [0, 0, 2, 0, 9, 0, 0, 0, 0], [1, 5, 0, 8, 6, 0, 0, 0, 0], [2, 0, 8, 0, 4, 0, 0, 6, 0], [0, 4, 6, 0, 0, 0, 0, 1, 0]]
def box_solver(game):
    ilk3 = [0, 1, 2]
    orta3 = [3, 4, 5]
    son3 = [6, 7, 8]
    var1 = []
    var2 = []

    hepsi = [ilk3, orta3, son3]

    for row in range(9):
        for col in range(9):
            if game[row][col] == 0:
                newset = []
                val = values(game, row, col)
                for x in hepsi:
                    for h in x:
                        if row == h:
                            var1 = x
                        if col == h:
                            var2 = x
                for a in var1:
                    for b in var2:
                        if game[a][b] == 0:
                            if a != row or b!= col:
                                newset.append(values(game,a,b))
                for z in newset:

                    val = list_diff(val,z)
                if len(val) == 1:
                    game[row][col] = val[0]
                    box_solver(game)

    return game

def row_solver(game):

    for row in range (9):
        for col in range (9):
                if game[row][col] == 0:
                    newset = []
                    val = values(game, row, col)
                    for x in range (9):

                            if x!= col and game[row][x] == 0:
                                newset.append(values(game,row,x))

                    for z in newset:

                            val = list_diff(val, z)

                    if len(val) == 1:
                                game[row][col] = val[0]
                                row_solver(game)
    return game




def column_solver(game):
    for row in range (9):
        for col in range (9):
                if game[row][col] == 0:
                    newset = []
                    val = values(game, row, col)
                    for x in range (9):

                            if x!= row and game[x][col] == 0:
                                newset.append(values(game,x,col))

                    for z in newset:

                            val = list_diff(val, z)

                    if len(val) == 1:
                                game[row][col] = val[0]
                                column_solver(game)
    return game
def check_game(game):
    for x in range (9):
        for y in range (9):
            if game[x][y] == 0:
                return "empty"
    return "full"
def main_solver(game):
    primarysolver(game)
    box_solver(game)
    row_solver(game)
    column_solver(game)

    for x in range(9):
        print(game[x])



start = time.time()

main_solver(li)
print(time.time()-start)
