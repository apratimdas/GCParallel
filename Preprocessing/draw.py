
from graphics import *
from random import randint
import csv
import sys
import colorsys

grid = []
for i in range(12):
    grid.append([])
    for j in range(12):
        grid[i].append(j)

# print(grid)

gcm=[]

with open(sys.argv[1]) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        gcm.append(row)

print(gcm)

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return [r, g, b]

def main():
    win = GraphWin("My Window", 600, 600)
    squares = []
    i=0
    j=0
    while i < 12:
        j=0
        while j < 12:
            square = Rectangle(Point(j*50,i*50), Point((j+1)*50,(i+1)*50))
            x = gcm[i][j]
            y = -float(x) + 1.0
            rval = int(y / 2 * 255)
            bval = int( (1 - y / 2) * 255)
            # rval = int(y / 2 * 255)
            rgb = colorsys.hsv_to_rgb(((y/2)*255)/360.0, 1.0, 0.7)
            rgbn = [int(x*255) for x in rgb]
            square.setFill(color_rgb(rgbn[0],rgbn[1],rgbn[2]))
            squares.append(square)
            square.draw(win)
            j+=1
        i+=1

    win.getMouse()


main()