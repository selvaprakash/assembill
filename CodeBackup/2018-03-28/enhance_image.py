#!/usr/bin/python2.7

import pandas as pd
import io
import os
import cv2
import imutils
from  find_image_angle  import find_angle

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/selvaprakash/BillD/BillDog-018b2ee1875d.json'
image_path='/home/selvaprakash/BillD/Ch1.jpg'
#csv_file="D:\BillD\Vishnu.csv"
#rotated_img="D:\BillD\Vishnu_rot1a1ted3.jpg"
final_img="/home/selvaprakash/BillD/Ch1_final_otsu.jpg"
res_gray_img="/home/selvaprakash/BillD/Ch1_res_gray.jpg"
img_to_excel="/home/selvaprakash/BillD/Ch1_excel.jpg"

def img_pre_process(image_path, res_gray_img, final_img,img_to_excel):
    img = cv2.imread(image_path, 8)
    h, w = img.shape[:2]
    if h > 1000 or w > 1000:
        img = cv2.resize(img, ( 478,637), interpolation=cv2.INTER_AREA)
    cv2.imwrite(img_to_excel,img)
    gray = cv2.bitwise_not(img)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #ret3,img = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #gray=img
    client = vision.ImageAnnotatorClient()
    cv2.imwrite(res_gray_img,gray)
    with io.open(res_gray_img, 'rb') as image_file:
        content = image_file.read()

    #img=cv2.imread(image_path, 0)
    image = types.Image(content=content)
    df = pd.DataFrame(columns=["Word_Count","Word", "X1", "Y1", 'X2', 'Y2'])
    print (df.columns)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #print('Texts:')
    #print texts
    ind=0

    # Take First Word
    for text,i in zip(texts,range(1,3)):
        if i==1:
            continue
        df=df.append({'Word_Count':i,'Word':(text.description).encode("ascii", "ignore")  ,'X2':0,'Y2':0,"X1":format(text.bounding_poly.vertices[0].x),"Y1":format(text.bounding_poly.vertices[0].y)},ignore_index=True)
        df=df.append({'Word_Count':i,'Word':(text.description).encode("ascii", "ignore"),'X1':0,'Y1':0,"X2":format(text.bounding_poly.vertices[1].x),"Y2":format(text.bounding_poly.vertices[1].y)},ignore_index=True)

    df1= df.groupby(['Word_Count']).max()
    df1=df1.reset_index(drop=True)
    print (df1.loc[0]['Word'], (float(len(df1.loc[0]['Word']))))
    (h,w)=img.shape[:2]
    print (h,w)
    print  ('X2',int(df1.loc[0]['X2']),'X1',int(df1.loc[0]['X1']),'Y1',int(df1.loc[0]['Y1']),'Y2',int(df1.loc[0]['Y2']))
    center = (h // 2 , w //2 )
    print (center)
    angle= (find_angle(df1.loc[0]['X1'],df1.loc[0]['Y1'],df1.loc[0]['X2'],df1.loc[0]['Y2']))
    #M = cv2.getRotationMatrix2D(center, -90, 1.0)
    if angle<>0 : # if imageis horizontal
        rotated = imutils.rotate_bound(gray, -angle)
        print ('Image Rotated ', -angle, ' degree')
        #rotated = cv2.warpAffine(img, M, (h+100, w+100))
        #cv2.imshow('Rotated',rotated)
        #cv2.waitKey(0)
        cv2.imwrite(final_img, rotated)
        #res = cv2.resize(rotated,(478, 637), interpolation = cv2.INTER_CUBIC)
        #gray = cv2.bitwise_not(res)
        #cv2.imwrite(final_img,gray)
        #return final_img
    else:
        print ('No Rotation')
        cv2.imwrite(final_img, gray)
        #return res_gray_img


if __name__=='__main__':
    img_pre_process(image_path,res_gray_img, final_img,img_to_excel)