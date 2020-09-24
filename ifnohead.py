#!/usr/bin/python2.7

import re
import pandas as pd
from statistics import mode,median,StatisticsError
#import xlsxwriter
def_word_spacing=20

def if_no_head(csv_file,end_Y):


    df=pd.read_csv(csv_file,sep='|') # TARGET OK
    #print (df)
    df=df.loc[df['Y1']<end_Y]
    #print 'first #print ifnohead'
    #print (df)
    #D:\Others\BillDog\Pics\CSV\img_enh_clean_20180214063724.csv
    dec_list=[]
    ##print df
    y_coor=[]
    x_coor=[]
    df_new=pd.DataFrame(columns=["Word", "X2", "Y1"])
    df_new1=pd.DataFrame(columns=["Word", "X2", "Y1"])
    df_new2=pd.DataFrame(columns=["Word", 'X1',"X2", "Y1"])
    to_be_dropped=[]
    ##print re.match(r"(\d+)\.(\d+)", "22.45")
    ##print df
    for i in range(1,len(df)):
        try:
            m=re.search(r"(\d+)\.(\d+)", str(df.loc[i]['Word']))
            ##print m.endpos,df.loc[i]['Word'],df.loc[i]['Y1'],df.loc[i]['X1']
            if m.endpos>3:
                dec_list.append(i)
        except AttributeError:
            1==1
    ##print m.endpos
    for i in dec_list:
        y_coor.append( df.loc[i]['Y1'])
        x_coor.append( df.loc[i]['X2'])
        ##print df.loc[i]['X1'],df.loc[i]['Y1'],df.loc[i]['X2'],df.loc[i]['Word']
        df_new=df_new.append({'Word':df.loc[i]['Word'],'X2':df.loc[i]['X2'],'Y1':df.loc[i]['Y1']},ignore_index=True)
    ##print df_new.groupby(['X2']).min(),df_new.groupby(['X2']).count()
    ##print (df_new['Y1']) #,max(df_new['X2'])
    df_new=df_new.reset_index(drop=True)
    ##print df_new
    ##print (y_coor)
    #print ('x_coor',max(x_coor))
    #print ('y_coor',min(y_coor))

    #print (min(df[df['Y1']==min(y_coor)].X1))
    #print (max(df[df['Y1']==min(y_coor)].X2))

    ##print df[ (df['X1']==max(df[df['Y1']==min(y_coor)].X1)) | (df['Y1']==min(df[df['Y1']==min(y_coor)].Y1))]
    for  i in range(len(df)):
        ##print df[ (df['X1']<=max(df[df['Y1']==min(y_coor)].X1)) & (df.loc[i]['Y1'] in y_coor) ]
         if (df.loc[i]['X1']>=min(df[df['Y1']==min(y_coor)].X1)) and (df.loc[i]['Y1'] in y_coor ):
             ##print df.loc[i]['Word']
             df_new2 = df_new2.append({'Word': df.loc[i]['Word'],'X1': df.loc[i]['X1'], 'X2': df.loc[i]['X2'], 'Y1': df.loc[i]['Y1']}, ignore_index=True)

    ##print df[df['X1']==min(df[df['Y1']==min(y_coor)].X1) ]
    ##print df_new.set_index('Y1')
    df_new= df_new.set_index('Y1','X2')
    df= df.set_index('Y1','X2')
    ##print df_new2

    sorted_df = df_new2.sort_values(by=['Y1','X1'])
    df = sorted_df.reset_index(drop=True)
    #print (df)
    j=0
    tex=''
    col1=pd.DataFrame(columns=['Word'])
    to_del=[]
    for i in range(1,len(df)):
        text=''
        if df.loc[i]['X1'] - df.loc[i-1]['X2']<def_word_spacing and df.loc[i]['Y1'] == df.loc[i-1]['Y1'] :
            df.loc[i]['Word'] = ' '+ str(df.loc[i]['Word'])
            #text=text+' '+ str(df.loc[i-1]['Word']) + ' ' + str(df.loc[i]['Word'])
            #to_del.append(i)
        elif df.loc[i]['Y1'] == df.loc[i-1]['Y1']:
            df.loc[i]['Word'] ='|'+ str(df.loc[i]['Word'])
            ##print str(df.loc[i-1]['Word']) + ',' + str(df.loc[i]['Word'])
            #text=text+''+str(df.loc[i-1]['Word']) + ',' + str(df.loc[i]['Word'])
            #to_del.append(i)

        else:
            continue

    #print df
    #print 'df', df.groupby('Y1')['Word'].apply(lambda x: x.sum())
    df= df.groupby('Y1')['Word'].apply(lambda x: x.sum()).reset_index(drop=True)
    #print 'df', df
        #col1 = col1.append({'Word':text},ignore_index=True)
    df1=pd.DataFrame()
    #print   df.str.split('|', expand=True)
    df_final = df.str.split('|', expand=True)
    ncols=df_final.shape[1]

    while len(df_final[df_final[ncols-1].isnull()])>0:
        #print  'No Val',  df_final[df_final[ncols-1].isnull()]
        df_noval=df_final[df_final[ncols-1].isnull()]
        #print 'Val',  df_final[df_final[ncols-1].notnull()]
        df_val=df_final[df_final[ncols-1].notnull()]
        df_noval =    df_noval.shift(1,axis=1)
        df_final =    pd.concat([df_val,df_noval])

    #print 'df_final',df_final
    return df_final
def main():
    #csv_file="/home/selvaprakash/BillD/CSV/CVS.jpg_enh_clean_20180309193352.csv"
    #csv_file="/home/selvaprakash/BillD/CSV/IMG-20180308-WA0003.jpg_enh_clean_20180308054712.csv"
    #csv_file="/home/selvaprakash/BillD/CSV/Vishnu2.jpg_enh_clean_20180309215834.csv"
    csv_file="/home/selvaprakash/BillD/CSV/BigBill_part1.png_final_clean_20180724034958.csv"
    if_no_head(csv_file,1000)

if __name__=='__main__':
    main()
