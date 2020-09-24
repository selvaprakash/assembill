import requests
import json
import base64
import os
import re
import sys
import io
import pandas as pd
import csv
import numpy as np
import cv2

from google.cloud import vision
from google.cloud.vision import types
from google.cloud import storage
#client = storage.Client()
#bucket = client.get_bucket('billdata')
#blob = bucket.get_blob('remote/path/to/file.txt')

#image_file= arg1

csv_folder= '/BillD/users/admin/CSV'
template_folder = '/BillD/users/image_templates'
proc_img="/home/selvaprakash/BillD/Pics/proc.png"




def detect_text_uri(path): # User Google API to detect Text in the Image
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    df = pd.DataFrame(columns= ["Word","X","Y"])
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')
    #print texts
    ind=0
    for text, i in zip(texts, range(1, len(texts))):
		# Send the same to Data Frame to be sent for Processing
    	 df=df.append({'Word_Count':i,'Word':(text.description).encode('utf-8').strip(),'X2':0,'Y2':0,"X1":format(text.bounding_poly.vertices[0].x),"Y1":format(text.bounding_poly.vertices[0].y)},ignore_index=True)
    	 df=df.append({'Word_Count':i,'Word':(text.description).encode('utf-8').strip(),'X1':0,'Y1':0,"X2":format(text.bounding_poly.vertices[1].x),"Y2":format(text.bounding_poly.vertices[1].y)},ignore_index=True)
    df1=df.groupby(['Word_Count','Word']).max()


    print ('df1', df1)
    #df1.to_csv('/home/selva/PycharmProjects/BillDog/CSV/df.csv',sep='|')
    return df1

def process_text(df1,min_x,max_x,min_y,max_y,df_coords,df_fields):

    #df = pd.DataFrame.from_csv("D:\Others\BillDog\Bill_contents.csv", index_col=None)
    df=df1
    #print 'df',df

    ####
    dfy2 = pd.to_numeric(df['Y1'])
    dfy2 = dfy2.to_frame()
    dfy2.sort_values('Y1', inplace=True)
    for i in range(0, len(dfy2)):
        if abs(dfy2.iloc[i, 0] - dfy2.iloc[i - 1, 0]) <= 10:
            dfy2.iloc[i, 0] = dfy2.iloc[i - 1, 0]
            # print df.iloc[i,0]
    #print 'dfy2', dfy2
    df['Y1'] = dfy2['Y1']
    ####

    df = df.loc[(df['Y1']).astype(int) > min_y]

    df = df.loc[(df['Y1']).astype(int) < max_y].reset_index()
    #print df
    df = df[['Word', 'X1', 'Y1', 'X2', 'Y2']]
    df = df.reset_index().drop(labels='index',axis=1)
    # df_c = df[['Word', 'X', 'Y']]
    #print df

    df['X1']=pd.to_numeric(df['X1'])
    df['X2'] = pd.to_numeric(df['X2'])
    int_array={}
    int_df=pd.DataFrame( columns=["Word",  'Y1'])
    #print 'df ', df
    # df_c = df.groupby('Y1')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    # print ('df_c', df_c)
    # print 'len',len(df_coords)
    print ('df cords',df_coords)
    for i in range(len(df_coords)):
        #if i == 0:
            df_filter = (df.loc[(df.X1 >= df_coords['Start_X'].iloc[i]) & (df.X2 <= df_coords['End_X'].iloc[i] )])
            print ('df_filter 0', df_filter)
            int_df1 = (df_filter[['Word','Y1']])
            int_df1 = int_df1.groupby(['Y1'])['Word'].apply(' '.join).reset_index()
            print ('int df grouped', int_df)
            int_df = int_df.merge(int_df1, how='outer', on="Y1", suffixes=('_l_'+str(i),'_r_'+str(i)))

            #int_df = int_df.drop('Word_x', axis='columns')

            print ('int df2', int_df)
        #df_c = df_c.groupby('Y')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    #int_df=pd.DataFrame.from_dict(int_array,orient='index')
    #print df_c
    print ('int_array final', int_df)

    int_df = int_df.reset_index()
    int_df_print = int_df.drop(['Word_l_0','Y1','index'],axis='columns')
    int_df_print.columns = df_coords['Field']

    print ('Printed DF', int_df.reset_index())
    print ('df print',int_df_print)

    pd.DataFrame.to_csv(int_df_print,'/home/selvaprakash/BillD/CSV/img2csv.csv',index = False)

    print('Done! Done! Done!')


def process_image(inp_img):
    inp_img = cv2.imread(inp_img)
    img = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(proc_img,img)


def main(df_coords1,inp_file):
    df = pd.DataFrame( columns=["Word","X","Y"])
    #y_start_end=find_bound_coor('/home/selva/BillDog/ExcelBill.png')

    process_image(inp_file)
    df1=detect_text_uri(proc_img)


    df_coords=pd.read_csv('/home/selvaprakash/BillD/CSV/templates/img_template.csv')
    print ('target ', df_coords[['Field','Start_X','End_X','Start_Y']])

    min_x=df_coords['Start_X'].min()
    min_y = df_coords['Start_Y'].min()
    max_x= df_coords['End_X'].max()
    max_y= df_coords['End_Y'].max()
    print ('min max coords', min_x,max_x,min_y,max_y)
    #df_coords = (df_coords.loc[(df_coords.Field != 'maxxy')])
    process_text(df1,min_x,max_x,min_y,max_y,df_coords[['Field','Start_X','End_X','Start_Y']],df_coords.iloc[:,0])

