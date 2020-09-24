#!/usr/bin/python2.7

import cv2
import numpy as np
import  pandas as pd
import math
from find_key_words import find_key_words
from find_item_end import find_item_end

csv_file="/home/selvaprakash/BillD/CSV/Latta_enh_clean.csv"
lined_img='/home/selvaprakash/BillD/Latta_Lined.jpg'
orig_imgage='/home/selvaprakash/BillD/Latta.jpg'
def_line_spacing=12
start_Y=221
end_Y=391

head_words = ['Item','ltem','Name','Item Name','ltem Name','Product','Prod','Qty','Oty','Quantity','0uantity','Value','Amount','Desc','Particulars','MRP','Rate']
tab_threshold=10
def_line_spacing=15


def draw_split_lines(csv_file,df_head,orig_image,lined_img,end_Y):
    line_y=[]
    print ('df_head',df_head)
    df=pd.read_csv(csv_file,sep='|')
    df=df[['Word','X1','Y1','X2','Y2']]
    #df=df.reset_index()
    #print df
    start_Y=df_head["Y1"].max()
    df = df.loc[(df["Y1"] > start_Y) & (df["Y1"] < end_Y)]
    df = df.reset_index(drop=True)
    print ('df_items',df)
    for j in range(1,len(df_head)):
        for i in range(0, len(df)):
            if ((df.loc[i]['X2']) >= (df_head.loc[j-1]['X2']) and (df.loc[i]['X2'])<(df_head.loc[j]['X1'])):
                line_y.append([j-1, df.loc[i]['X2']])
                #print 'Line ', j-1,(df.loc[i]['Word']), (df.loc[i]['X1']), (df.loc[i]['X2']), (df_head.loc[j - 1]['X2']), (
                #df_head.loc[j]['X1'])
            elif  ((df.loc[i]['X1']) >= (df_head.loc[j]['X1']) and (df.loc[i]['X1'])<=(df_head.loc[j]['X2'])):
                line_y.append([j, df.loc[i]['X2']])
                #print 'Line X1',j,(df.loc[i]['Word']), (df.loc[i]['X1']), (df.loc[i]['X2']), (df_head.loc[j - 1]['X2']), (
                #df_head.loc[j]['X1'])
            elif ((df.loc[i]['X2']) >= (df_head.loc[j]['X1']) and (df.loc[i]['X1']) <= (df_head.loc[j]['X2'])) :
                line_y.append([j, df.loc[i]['X2']])
                #print 'Line X2',j,(df.loc[i]['Word']),(df.loc[i]['X1']),(df.loc[i]['X2']),(df_head.loc[j-1]['X2']),(df_head.loc[j]['X1'])
            elif j==1 and (df.loc[i]['X2']) <= (df_head.loc[j-1]['X2']):
                line_y.append([j-1, df.loc[i]['X2']])
            else:
               #print (df.loc[i]['Word']),(df.loc[i]['X1']),(df.loc[i]['X2']),(df_head.loc[j-1]['X2']),(df_head.loc[j]['X1'])
                continue
    print ('line_y',line_y)
    df_lines = pd.DataFrame(data=line_y, columns=['Col_Position','Line_X'])
    df_lines=df_lines.sort_values(by=['Col_Position'])
    #print df_lines
    df_lines= df_lines.groupby(by='Col_Position').max()
    df_lines=df_lines.reset_index(drop=True)
    line_img=cv2.imread(orig_image)
    for i in range(len(df_lines)):

        cv2.line(line_img,(df_lines.loc[i]["Line_X"], start_Y), (df_lines.loc[i]["Line_X"], end_Y), (0, 0, 0), 1)
        print (df_lines.loc[i]["Line_X"],start_Y,end_Y)
    cv2.imwrite(lined_img, line_img)
    print ('df_lines',df_lines)
    return df_lines
def main():
    df_head=find_key_words(csv_file)
    #df_head=df_head.reset_index(drop=True)
    print ('df_head',df_head)
    lined_img='/home/selvaprakash/BillD/Latta_Lined.jpg'
    draw_split_lines(csv_file,df_head.reset_index(drop=True),orig_imgage,lined_img,391)

if __name__=='__main__':
    main()