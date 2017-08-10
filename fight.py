import os
import sys
import re
from collections import defaultdict
import math
from random import randint

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
    f.write("In fill_values() 42:"+str(box_x)+str(box_y)+"\n")
    f.flush()
    values[box_x][box_y] += 1

def fill_edges(box_x, box_y, edge):
    global edges
    f.write("In 48\n");
    if (edge == "left"):
        index = 0
    elif (edge == "top"):
        index = 1
    elif (edge == "right"):
        index = 2
    elif (edge == "bottom"):
        index = 3
    f.write("In fill_edges() 54:"+str(box_x)+str(box_y)+edge+str(index)+"\n")
    f.flush()
    edges[box_x][box_y][index] = 1

def process_opponent_move(opp_move):
    f.write(opp_move+'\n')
    f.flush()
    coord = opp_move.split(" ")[1]
    coord1 = int(coord[1])
    coord3 = int(coord[7])
    coord2 = int(coord[3])
    coord4 = int(coord[9])
    #print ("Coords:")
    #print (coord1, coord2, coord3, coord4)
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

    print var
    f.write(var+'\n')
    f.flush()
    sys.stdout.flush()

def cover_edge (i, j):
    edge = ""
    ran = randint(0,3)
    f.write("In cover_edge() 135\n")
    f.flush()

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
        f.write("In cover_edge() 146:"+str(i)+str(j)+str(index)+edge+"\n")
        f.flush()

        if (0 == edges[i][j][index]):
            fill_edges(i,j,edge)
            fill_values(i,j)
            #print (i,j,edge)
            print_move (i,j,edge)
            f.write("In cover_edge() 154:"+str(i)+str(j)+"\n")
            f.flush()

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
            f.write("In cover_edge() 161:"+str(i)+str(j)+edge+"\n")
            f.flush()
            if (i >= 0 and j >= 0 and i <= n-1 and j <= n-1):
                f.write("In cover_edge() 163:"+str(i)+str(j)+edge+"\n")
                f.flush()
                fill_edges(i, j, edge)
                fill_values(i, j)
                #print (i,j,edge)
            break

def find_box_and_fill(num):
    global values
    global edges

    for i in range(n):
        for j in range(n):
            if (num == values[i][j]):
                f.write("Cover edge 172:"+str(i)+str(j)+"\n")
                f.flush()
                cover_edge(i,j)
                return 1
    return 0

def find_next_move():
    global f
    f.write("Here 3\n")
    ret = find_box_and_fill (3)
    if (1 == ret):
        return

    f.write("Here 0\n")
    ret = find_box_and_fill (0)
    if (1 == ret):
        return

    f.write("Here 1\n")
    ret = find_box_and_fill (1)
    if (1 == ret):
        return

    f.write("Here 2\n")
    ret = find_box_and_fill (2)
    if (1 == ret):
        return

def read_opponent_move():
    global f
    opponent_move = raw_input()
    process_opponent_move(opponent_move)

def switch_on_command():
    our_move=0;
    their_move=0;
    while True:
        user_input = raw_input ()

        if user_input == "START 1":
            find_next_move()
        elif user_input == "START 2":
            read_opponent_move()
        elif user_input == "YOUR_MOVE":
            find_next_move()
            our_move+=1
        elif re.match ('OPPONENT_MOVE', user_input):
            process_opponent_move(user_input)
            their_move+=1
        elif user_input == "STOP":
            f.write(str(our_move)+"\n"+str(their_move)+"\n")
            f.write("Stopping")
            f.flush()
            sys.exit()
        else:
            print ("Invalid input")
            sys.exit(1)
        #display_edges()
        #display_values()

filename = sys.argv[1]
f = open(filename, 'w')
switch_on_command()
