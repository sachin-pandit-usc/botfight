import os
import sys
import re
from collections import defaultdict
import math
from random import randint

n = 9
edges={}
for i in range (8):
    edges[i] = defaultdict(dict)

values={}
for i in range (8):
    values[i] = defaultdict(dict)

for i in range (8):
    for j in range (8):
        values[i][j] = 0

for i in range (8):
    for j in range (8):
        edges[i][j] = [0,0,0,0]
        #                      [l,t,r,b]


def display_values():
    for i in range(8):
        for j in range(8):
            print values[i][j],
        print ""

def display_edges():
    for i in range(8):
        for j in range(8):
            print edges[i][j],
        print ""
        print "" 

def fill_values(box_x, box_y):
    global values
    values[box_x][box_y] += 1

def fill_edges(box_x, box_y, edge):
    global edges
    if (edge == "left"):
        index = 0
    elif (edge == "top"):
        index = 1
    elif (edge == "right"):
        index = 2
    elif (edge == "bottom"):
        index = 3
    edges[box_x][box_y][index] = 1

def process_opponent_move(opp_move):
    coord = opp_move.split(" ")[2]
    coord1 = int(coord[1])
    coord3 = int(coord[7])
    coord2 = int(coord[3])
    coord4 = int(coord[9])
    print ("Coords:")
    print (coord1, coord2, coord3, coord4)
    fill_board (coord1, coord2, coord3, coord4)

def fill_board (coord1, coord2, coord3, coord4):
    box_x = max(coord3, coord1) - 1
    box_y = max(coord4, coord2) - 1

    if (coord1 == coord3):
        #Horizontal line
        edge = "bottom"
    if (coord2 == coord4):
        #Vertical line
        edge = "right"
    if (box_x >= 0 and box_y >= 0 and box_x < 8 and box_y < 8):
        fill_edges(box_x, box_y, edge)
        fill_values(box_x, box_y)
    print (box_x, box_y, edge)

    if (edge == "bottom"):
        edge = "top"
        box_x+=1
    if (edge == "right"):
        edge = "left"
        box_y+=1
    if (box_x >= 0 and box_y >= 0 and box_x < 8 and box_y < 8):
        fill_edges(box_x, box_y, edge)
        fill_values(box_x, box_y)
    print (box_x, box_y, edge)


def print_move(i,j,edge):
    if (edge == "bottom"):
        xcord = i+1
        ycord = j
        var = "(" + xcord + "," + ycord
        var += "),(" + xcord + "," + (ycord+1) + ")"

    if (edge == "right"):
        xcord = i
        ycord = j+1
        var = "(" + (xcord) + "," + ycord
        var += "),(" + (xcord+1) + "," + (ycord) + ")"

    if (edge == "top"):
        xcord = i
        ycord = j
        var = "(" + xcord + "," + ycord
        var += "),(" + xcord + "," + (ycord+1) + ")"
        
    if (edge == "left"):
        xcord = i
        ycord = j
        var = "(" + (xcord) + "," + ycord
        var += "),(" + (xcord+1) + "," + (ycord) + ")"

def cover_edge (i, j):
    edge = ""
    ran = randint(0,3)
    for k in range(3):
        index = (ran+k)%4
        if (0 == index):
            edge = "left"
        if (1 == index):
            edge = "top"
        if (2 == index):
            edge = "right"
        if (3 == index):
            edge = "bottom"

        if (0 == edges[i][j][index]):
            fill_edges(i,j,edge)
            fill_values(i,j)
            print (i,j,edge)
            print_move (i,j,move)

            if (edge == "bottom"):
                edge = "top"
                i+=1
            if (edge == "right"):
                edge = "left"
                j+=1
            if (edge == "top"):
                edge = "bottom"
                i-=1
            if (edge == "left"):
                edge = "right"
                j-=1
            if (i >= 0 and j >= 0 and i < 8 and j < 8):
                fill_edges(i, j, edge)
                fill_values(i, j)
                print (i,j,edge)
                print_move (i,j,move)
            break

def find_box_and_fill(num):
    global values
    global edges

    for i in range(8):
        for j in range(8):
            if (num == values[i][j]):
                cover_edge(i,j)
                return 1
    return 0

def find_next_move():
    print ("dummy move")
    ret = find_box_and_fill (3)
    if (1 == ret):
        return

    ret = find_box_and_fill (0)
    if (1 == ret):
        return

    ret = find_box_and_fill (1)
    if (1 == ret):
        return

    ret = find_box_and_fill (2)
    if (1 == ret):
        return

def read_opponent_move():
    opponent_move = raw_input()
    process_opponent_move(opponent_move)

def switch_on_command():
    while True:
        user_input = raw_input ()

        if user_input == "START 1":
            find_next_move()
        elif user_input == "START 2":
            read_opponent_move()
        elif user_input == "YOUR MOVE":
            find_next_move()
        elif re.match ('OPPONENT MOVE', user_input):
            process_opponent_move(user_input)
        elif user_input == "STOP":
            sys.exit()
        else:
            print ("Invalid input")
            sys.exit(1)
        display_edges()
        display_values()

switch_on_command()
