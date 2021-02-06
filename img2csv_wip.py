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
proc_img_twit="/home/selvaprakash/BillD/Pics/"
#image_file= arg1
USER_FOLDER = '/home/selvaprakash/BillD/static/users/'
#USER_FOLDER = '/mnt/c/d/BillD/static/users/'

csv_folder= '/BillD/users/admin/CSV'
template_folder = '/BillD/users/image_templates'


def detect_text_uri(path): # User Google API to detect Text in the Image
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    #df = pd.DataFrame(columns= ["Word","X","Y"])
    df = pd.DataFrame(columns= ["Word_Count","Word","X1","Y1","X2","Y2"])
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    print (texts)
    ind=0
    for text, i in zip(texts, range(1, len(texts)+1)):

		# Send the same to Data Frame to be sent for Processing
    	 df=df.append({'Word_Count':i,'Word':(text.description).strip(),'X2':0,'Y2':0,"X1":(text.bounding_poly.vertices[0].x),"Y1":(text.bounding_poly.vertices[0].y)},ignore_index=True)
    	 df=df.append({'Word_Count':i,'Word':(text.description).strip(),'X1':0,'Y1':0,"X2":(text.bounding_poly.vertices[1].x),"Y2":(text.bounding_poly.vertices[1].y)},ignore_index=True)
    	 print ((text.description).encode('utf-8').strip(),format(text.bounding_poly.vertices[0].y))


    print ('y1',df['Y1'],df['X1'])
    print (df)
    print (df.groupby(['Word_Count','Word'])['X1','X2','Y1','Y2'].max())
    df1=df.groupby(['Word_Count','Word'])['X1','X2','Y1','Y2'].max()


    print ('df1', df1)
    print ("Y1", format(text.bounding_poly.vertices[0].y))
    #df1.to_csv('/home/selva/PycharmProjects/BillDog/CSV/df.csv',sep='|')
    return df1.reset_index()

def process_text(df,df_coords,df_fields,user,inp_file):

    #df = pd.DataFrame.from_csv("D:\Others\BillDog\Bill_contents.csv", index_col=None)
    print ('df',df.columns)
    # if df_coords.empty:
    #     df_coords = pd.DataFrame(['Column1',0,0,5000,5000], name = ['Field','Start_X','Start_Y','End_X', 'End_Y'])


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

    # df = df.loc[(df['Y1']).astype(int) > min_y]
    #
    # df = df.loc[(df['Y1']).astype(int) < max_y].reset_index()
    #print df
    df = df[['Word', 'X1', 'Y1', 'X2', 'Y2']]
    df = df.reset_index().drop(labels='index',axis=1)
    # df_c = df[['Word', 'X', 'Y']]
    #print df

    df['X1']=pd.to_numeric(df['X1'])
    df['X2'] = pd.to_numeric(df['X2'])
    int_array={}
    int_df=pd.DataFrame( )
    #print 'df ', df
    # df_c = df.groupby('Y1')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    # print ('df_c', df_c)
    # print 'len',len(df_coords)
    print ('df cords',df_coords)
    for i in range(len(df_coords)):
        #if i == 0:
            df_filter = (df.loc[(df.X1 >= df_coords['Start_X'].iloc[i]) & (df.X2 <= df_coords['End_X'].iloc[i] ) & (df.Y1 >= df_coords['Start_Y'].iloc[i] ) & (df.Y1 <= df_coords['End_Y'].iloc[i] ) ])
            print ('df_filter 0', df_filter)
            int_df1 = (df_filter[['Word','Y1']])
            int_df1 = int_df1.groupby(['Y1'])['Word'].apply(' '.join).reset_index()
            print ('int df grouped', int_df)
            #int_df = int_df.merge(int_df1, how='outer', on="Y1", suffixes=('_l_'+str(i),'_r_'+str(i)))


            new_words = int_df1["Word"]
            print ('New Words', new_words)
            int_df = pd.concat([int_df, new_words], axis=1)

            print ('int df2', int_df)
        #df_c = df_c.groupby('Y')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    #int_df=pd.DataFrame.from_dict(int_array,orient='index')
    #print df_c
    print ('int_array final', int_df)

    int_df = int_df.reset_index()
    int_df_print = int_df.drop(['index'],axis='columns')
    #int_df_print = int_df.drop(['Word_l_0','Y1','index'],axis='columns')
    print ('Current Columns',int_df_print.columns)
    int_df_print.columns = df_coords['Field']

    print ('Printed DF', int_df.reset_index())
    print ('df print',int_df_print)

    pd.DataFrame.to_csv(int_df_print,USER_FOLDER+user+'/CSV/results/'+os.path.basename(inp_file)+'.csv',index = False)

    print('Done! Done! Done!')



def process_text_bulk(df,df_coords,df_fields,user,inp_file):

    #df = pd.DataFrame.from_csv("D:\Others\BillDog\Bill_contents.csv", index_col=None)
    print ('df',df.columns)
    # if df_coords.empty:
    #     df_coords = pd.DataFrame(['Column1',0,0,5000,5000], name = ['Field','Start_X','Start_Y','End_X', 'End_Y'])


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

    # df = df.loc[(df['Y1']).astype(int) > min_y]
    #
    # df = df.loc[(df['Y1']).astype(int) < max_y].reset_index()
    #print df
    df = df[['Word', 'X1', 'Y1', 'X2', 'Y2']]
    df = df.reset_index().drop(labels='index',axis=1)
    # df_c = df[['Word', 'X', 'Y']]
    #print df

    df['X1']=pd.to_numeric(df['X1'])
    df['X2'] = pd.to_numeric(df['X2'])
    int_array={}
    int_df=pd.DataFrame( )
    #print 'df ', df
    # df_c = df.groupby('Y1')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    # print ('df_c', df_c)
    # print 'len',len(df_coords)
    print ('df cords',df_coords)
    for i in range(len(df_coords)):
        #if i == 0:
            df_filter = (df.loc[(df.X1 >= df_coords['Start_X'].iloc[i]) & (df.X2 <= df_coords['End_X'].iloc[i] ) & (df.Y1 >= df_coords['Start_Y'].iloc[i] ) & (df.Y1 <= df_coords['End_Y'].iloc[i] ) ])
            print ('df_filter 0', df_filter)
            int_df1 = (df_filter[['Word','Y1']])
            int_df1 = int_df1.groupby(['Y1'])['Word'].apply(' '.join).reset_index()
            print ('int df grouped', int_df)
            #int_df = int_df.merge(int_df1, how='outer', on="Y1", suffixes=('_l_'+str(i),'_r_'+str(i)))


            new_words = int_df1["Word"]
            print ('New Words', new_words)
            int_df = pd.concat([int_df, new_words], axis=1)

            print ('int df2', int_df)
        #df_c = df_c.groupby('Y')['Word'].apply(lambda x: "{%s}" % ' '.join(x))
    #int_df=pd.DataFrame.from_dict(int_array,orient='index')
    #print df_c
    print ('int_array final', int_df)

    int_df = int_df.reset_index()
    int_df_print = int_df.drop(['index'],axis='columns')
    #int_df_print = int_df.drop(['Word_l_0','Y1','index'],axis='columns')
    print ('Current Columns',int_df_print.columns)


    print ('Printed DF', int_df.reset_index())
    print ('df printed',int_df_print)
    int_df_print.columns = df_coords['Field']
    return (int_df_print)


def process_image(inp_img,user):
    inp_img = cv2.imread(inp_img)
    img = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)

    proc_img = USER_FOLDER+user+'/images/processed/proc.png'

    cv2.imwrite(proc_img,img)
    return proc_img

def main(inp_file,user,template_file):
    df = pd.DataFrame( columns=["Word","X","Y"])
    #y_start_end=find_bound_coor('/home/selva/BillDog/ExcelBill.png')
    print ('inp_file',inp_file)
    proc_img = process_image(inp_file,user)
    df1=detect_text_uri(proc_img)

    #df.to_csv(pd.DataFrame.to_csv(df, USER_FOLDER + user + '/' + 'CSV/templates/' + template_name + '.csv'))
    df_coords=pd.read_csv(template_file)
    print ('target ', df_coords[['Field','Start_X','End_X','Start_Y']])

    # min_x=df_coords['Start_X'].min()
    # min_y = df_coords['Start_Y'].min()
    # max_x= df_coords['End_X'].max()
    # max_y= df_coords['End_Y'].max()
    # print ('min max coords', min_x,max_x,min_y,max_y)
    #df_coords = (df_coords.loc[(df_coords.Field != 'maxxy')])
    print ('df1',df1)
    process_text(df1,df_coords[['Field','Start_X','End_X','Start_Y','End_Y']],df_coords.iloc[:,0],user,inp_file)


def main_bulk(imglist,user,template_file):

    df = pd.DataFrame( columns=["Word","X","Y"])
    final_df =pd.DataFrame()


    #df.to_csv(pd.DataFrame.to_csv(df, USER_FOLDER + user + '/' + 'CSV/templates/' + template_name + '.csv'))
    df_coords=pd.read_csv(template_file)
    print ('target ', df_coords[['Field','Start_X','End_X','Start_Y']])



    for img in imglist:
        print ('inp_file',img)
        proc_img = process_image(img,user)
        df1=detect_text_uri(proc_img)

        ret_df = process_text_bulk(df1,df_coords[['Field','Start_X','End_X','Start_Y','End_Y']],df_coords.iloc[:,0],user,img)
        final_df = final_df.append (ret_df)
    # final_df = final_df.reset_index()
    # final_df.columns = df_coords['Field']
    print ('Final DF',final_df)
    return final_df


def detect_text_api(path): # User Google API to detect Text in the Image
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    #df = pd.DataFrame(columns= ["Word","X","Y"])
    #df = pd.DataFrame(columns= ["Word_Count","Word","X1","Y1","X2","Y2"])
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    print (texts[0])
    return(texts[0].description)


def process_image_twit(inp_img):
    proc_img = inp_img+'_twitproc.png'
    inp_img_obj = cv2.imread(inp_img)
    #filename = os.path.basename(inp_img)
    img = cv2.cvtColor(inp_img_obj, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(proc_img,img)
    return (proc_img)

def main_api(df_coords,inp_file):
    df = pd.DataFrame( columns=["Word","X","Y"])
    #y_start_end=find_bound_coor('/home/selva/BillDog/ExcelBill.png')
    print ('inp_file',inp_file)
    proc_img = process_image(inp_file,'apiuser')
    df1=detect_text_uri(proc_img)

    #df.to_csv(pd.DataFrame.to_csv(df, USER_FOLDER + user + '/' + 'CSV/templates/' + template_name + '.csv'))
    #df_coords=pd.read_csv(template_file)
    print ('target ', df_coords[['Field','Start_X','End_X','Start_Y']])

    # min_x=df_coords['Start_X'].min()
    # min_y = df_coords['Start_Y'].min()
    # max_x= df_coords['End_X'].max()
    # max_y= df_coords['End_Y'].max()
    # print ('min max coords', min_x,max_x,min_y,max_y)
    #df_coords = (df_coords.loc[(df_coords.Field != 'maxxy')])
    print ('df1',df1)
    process_text(df1,df_coords[['Field','Start_X','End_X','Start_Y','End_Y']],df_coords.iloc[:,0],'apiuser',inp_file)

def main_twit_api(inp_file):
    #df = pd.DataFrame( columns=["Word","X","Y"])
    #y_start_end=find_bound_coor('/home/selva/BillDog/ExcelBill.png')

    #proc_img = process_image_twit(inp_file)
    #print(proc_img)
    df1=detect_text_api(inp_file)
    return df1


    #df_coords=pd.read_csv('/home/selvaprakash/BillD/CSV/templates/img_template.csv')
    # print ('target ', df_coords1[['Field','Start_X','End_X','Start_Y']])

    # min_x=df_coords['Start_X'].min()
    # min_y = df_coords['Start_Y'].min()
    # max_x= df_coords['End_X'].max()
    # max_y= df_coords['End_Y'].max()
    # print ('min max coords', min_x,max_x,min_y,max_y)
    #df_coords = (df_coords.loc[(df_coords.Field != 'maxxy')])
    #process_text(df1,min_x,max_x,min_y,max_y,df_coords1[['Field','Start_X','End_X','Start_Y','End_Y']],df_coords.iloc[:,0])
