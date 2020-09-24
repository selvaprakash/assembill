#!/usr/bin/python2.7

import pandas as pd
import io
import os
import cv2

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/selvaprakash/BillD/BillDog-018b2ee1875d.json'
image_path='/home/selvaprakash/BillD/Vishnu_enh_20180311181420.jpg'
csv_file="/home/selvaprakash/BillD/CSV/Vishnu_enh2.csv"
rotated_img='/home/selvaprakash/BillD/Vishnu_enh_rotated.jpg'


def detect_text(path,csv_file):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    img=cv2.imread(path, 0)
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
    #print (float(len(df1.loc[0]['Word'])))
    (h,w)=img.shape
    print h,w
    center = (w // 2, h // 2)
    print center
    M = cv2.getRotationMatrix2D(center, -90, 1.0)
    if float(len(df1.loc[0]['Word']))/( int(df1.loc[0]['X2'])-int(df1.loc[0]['X1'])) <3: # if imageis horizontal
        cv2.getRotationMatrix2D(center, -90, 1.0)
        rotated = cv2.warpAffine(img, M, (h, w))
        cv2.imwrite(rotated_img, rotated)
        print ('Image Rotated')
        return rotated
    else:
        print ('Image Original')
        return image_path

if __name__=='__main__':
    detect_text(image_path,csv_file)