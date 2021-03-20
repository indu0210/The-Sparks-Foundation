from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
import pandas as pd
import argparse



#creating argument parser to take image path from command line as input from user
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--img', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['img']


#Reading the image with opencv
img = cv2.imread(img_path)
#resizing image so as to display colors
img = cv2.resize(img, (950, 600))


#declaring global variables
clicked = False
r = g = b = xpos = ypos = 0



#Reading csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)



#function to convert RGB to HEX so as to use them as labels
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))



#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    mini = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=mini):
            mini = d
            cname = csv.loc[i,"color_name"]
    return cname



#function to get x,y coordinates of mouse double click
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)
while(1):
    cv2.imshow("image",img)
    if (clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (650,65), (b,g,r), -1)
        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b)+ ' R='+ str(r) +' G='+ str(g)+' B='+ str(b)
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.7,(255,255,255),2,cv2.LINE_AA)
        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False


    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
