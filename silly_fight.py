import os
import sys
import re
from collections import defaultdict
import math
from random import randint

var = ""
namma_boxes=0
global_count=0
n = 9
edges={}
for i in range (n):
    edges[i] = defaultdict(dict)

values={}
for i in range (n):
    values[i] = defaultdict(dict)

for i in range (n):
    for j in range (n):
        values[i][j] = 0

for i in range (n):
    for j in range (n):
        edges[i][j] = [0,0,0,0]
        #                      [l,t,r,b]


def display_values():
    for i in range(n):
        for j in range(n):
            print values[i][j],
        print ""

def display_edges():
    for i in range(n):
        for j in range(n):
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
    global f
    global global_count

    coord = opp_move.split(" ")[1]
    coord1 = int(coord[1])
    coord3 = int(coord[7])
    coord2 = int(coord[3])
    coord4 = int(coord[9])
    global_count +=1
    f.write("Player 1 Moved :("+str(coord1)+","+str(coord2)+"),("+str(coord3)+","+str(coord4)+")\n")
    f.flush()
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
    if (box_x >= 0 and box_y >= 0 and box_x <= n-1 and box_y <= n-1):
        fill_edges(box_x, box_y, edge)
        fill_values(box_x, box_y)
    #print (box_x, box_y, edge)

    if (edge == "bottom"):
        edge = "top"
        box_x+=1
    if (edge == "right"):
        edge = "left"
        box_y+=1
    if (box_x >= 0 and box_y >= 0 and box_x <= n-1 and box_y <= n-1):
        fill_edges(box_x, box_y, edge)
        fill_values(box_x, box_y)
    #print (box_x, box_y, edge)


def print_move(i,j,edge):
    global f
    global var
    if (edge == "bottom"):
        xcord = i+1
        ycord = j

        var = "(" + str(xcord) + "," + str(ycord)
        var += "),(" + str(xcord) + "," + str(ycord+1) + ")"

    if (edge == "right"):
        xcord = i
        ycord = j+1
        var = "(" + str(xcord) + "," + str(ycord)
        var += "),(" + str(xcord+1) + "," + str(ycord) + ")"

    if (edge == "top"):
        xcord = i
        ycord = j
        var = "(" + str(xcord) + "," + str(ycord)
        var += "),(" + str(xcord) + "," + str(ycord+1) + ")"
        
    if (edge == "left"):
        xcord = i
        ycord = j
        var = "(" + str(xcord) + "," + str(ycord)
        var += "),(" + str(xcord+1) + "," + str(ycord) + ")"

def cover_edge (i, j):
    edge = ""
    ran = randint(0,3)

    for k in range(4):
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
            #print (i,j,edge)
            print_move (i,j,edge)

            if (edge == "bottom"):
                edge = "top"
                i+=1
            elif (edge == "right"):
                edge = "left"
                j+=1
            elif (edge == "top"):
                edge = "bottom"
                i-=1
            elif (edge == "left"):
                edge = "right"
                j-=1
            if (i >= 0 and j >= 0 and i <= n-1 and j <= n-1):
                fill_edges(i, j, edge)
                fill_values(i, j)
                #print (i,j,edge)
            return 1

def find_box_and_fill(num):
    global values
    global edges

    for i in range(n):
        for j in range(n):
            if (num == values[i][j]):
                ret = cover_edge(i,j)
                if (ret == 1):
                    return 1

    return 0

def find_next_move():
    global f
    global var
    global namma_boxes
    global global_count

    ret = find_box_and_fill (3)
    if (1 == ret):
        f.write("Got box!\n")
        namma_boxes+=1
        f.write("Player 2 Moved :"+var+'\n')
        f.flush()
        print var
        sys.stdout.flush()
        return

    ret = find_box_and_fill (0)
    if (1 == ret):
        f.write("Player 2 Moved :"+var+'\n')
        f.flush()
        print var
        sys.stdout.flush()
        return

    ret = find_box_and_fill (1)
    if (1 == ret):
        f.write("Player 2 Moved :"+var+'\n')
        f.flush()
        print var
        sys.stdout.flush()
        return

    ret = find_box_and_fill (2)
    if (1 == ret):
        f.write("Player 2 Moved :"+var+'\n')
        f.flush()
        print var
        sys.stdout.flush()
        return

def read_opponent_move():
    global f
    opponent_move = raw_input()
    process_opponent_move(opponent_move)

def switch_on_command():
    global namma_boxes
    global f
    global global_count

    while True:
        user_input = raw_input ()
        #f.write(user_input+" "+str(global_count)+"\n")
        #f.flush()
        if user_input == "START 1":
            f.write("We are playing first\n")
            f.flush()
        elif user_input == "START 2":
            f.write("We are playing second\n")
            f.flush()
            read_opponent_move()
        elif user_input == "YOUR_MOVE":
            find_next_move()
        elif re.match ('OPPONENT_MOVE', user_input):
            process_opponent_move(user_input)
        elif user_input == "STOP":
            f.write("we got: "+str(namma_boxes)+"\n")
            f.write("Stopping\n")
            f.flush()
            sys.exit()
        #display_edges()
        #display_values()

filename = sys.argv[1]
f = open(filename, 'w')
switch_on_command()
