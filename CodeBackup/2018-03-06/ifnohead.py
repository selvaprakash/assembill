import re
import pandas as pd
from statistics import mode,median
#import xlsxwriter

def if_no_head(csv_file):
    #df=pd.read_csv("D:\Others\BillDog\Pics\CSV\img_enh_clean_20180206024251.csv") # venkat OK
    #df=pd.read_csv("D:\Others\BillDog\CSV\Latta7_jpg_enh_clean_20180208234201.csv") # Latta OK
    #df=pd.read_csv("D:\Others\BillDog\CSV\Thang_enh_clean.csv") #Thang_enh_clean OK
    #df=pd.read_csv("D:\Others\BillDog\Pics\CSV\img_enh_clean_20180129171815.csv") # Amma NOT OK
    df=pd.read_csv(csv_file) # TARGET OK
    #D:\Others\BillDog\Pics\CSV\img_enh_clean_20180214063724.csv
    dec_list=[]
    #print df
    y_coor=[]
    x_coor=[]
    df_new=pd.DataFrame(columns=["Word", "X2", "Y1"])
    df_new1=pd.DataFrame(columns=["Word", "X2", "Y1"])
    df_new2=pd.DataFrame(columns=["Word", 'X1',"X2", "Y1"])
    to_be_dropped=[]
    #print re.match(r"(\d+)\.(\d+)", "22.45")
    #print df
    for i in range(1,len(df)):
        try:
            m=re.search(r"(\d+)\.(\d+)", df.loc[i]['Word'])
            #print m.endpos,df.loc[i]['Word'],df.loc[i]['Y1'],df.loc[i]['X1']
            if m.endpos>3:
                dec_list.append(i)
        except AttributeError:
            1==1
    #print m.endpos
    for i in dec_list:
        y_coor.append( df.loc[i]['Y1'])
        x_coor.append( df.loc[i]['X2'])
        #print df.loc[i]['X1'],df.loc[i]['Y1'],df.loc[i]['X2'],df.loc[i]['Word']
        df_new=df_new.append({'Word':df.loc[i]['Word'],'X2':df.loc[i]['X2'],'Y1':df.loc[i]['Y1']},ignore_index=True)
    #print df_new.groupby(['X2']).min(),df_new.groupby(['X2']).count()
    #print (df_new['Y1']) #,max(df_new['X2'])
    df_new=df_new.reset_index(drop=True)
    #print df_new

    print ('x_coor',max(x_coor))
    print ('y_coor',min(y_coor))

    print (min(df[df['Y1']==min(y_coor)].X1))
    print (max(df[df['Y1']==min(y_coor)].X2))

    #print df[ (df['X1']==max(df[df['Y1']==min(y_coor)].X1)) | (df['Y1']==min(df[df['Y1']==min(y_coor)].Y1))]
    for  i in range(len(df)):
        #print df[ (df['X1']<=max(df[df['Y1']==min(y_coor)].X1)) & (df.loc[i]['Y1'] in y_coor) ]
         if (df.loc[i]['X1']>=min(df[df['Y1']==min(y_coor)].X1)) and (df.loc[i]['Y1'] in y_coor):
             #print df.loc[i]['Word']
             df_new2 = df_new2.append({'Word': df.loc[i]['Word'],'X1': df.loc[i]['X1'], 'X2': df.loc[i]['X2'], 'Y1': df.loc[i]['Y1']}, ignore_index=True)

    #print df[df['X1']==min(df[df['Y1']==min(y_coor)].X1) ]
    #print df_new.set_index('Y1')
    df_new= df_new.set_index('Y1','X2')
    df= df.set_index('Y1','X2')
    #print df_new2

    sorted_df = df_new2.sort_values(by=['Y1','X1'])
    df = sorted_df.reset_index(drop=True)
    #print df
    ncols=df.shape[1]
    word_space=0
    word_space_arr=[]
    counter=0
    for i in range(1, len(df)):
        if df.loc[i]['X1']>df.loc[i - 1]['X2']:
            if re.match('[A-Z]', df.loc[i]['Word']):
                word_space+=((df.loc[i]['X1']) - (df.loc[i - 1]['X2']))
                counter+=1
                print (type(df.loc[i]['Word']),df.loc[i]['Word'],df.loc[i]['X1'],df.loc[i - 1]['X2'],((df.loc[i]['X1']) - (df.loc[i - 1]['X2'])))
                word_space_arr.append(((df.loc[i]['X1']) - (df.loc[i - 1]['X2'])))

    print ('median',median(word_space_arr))
    median_word_space=median(word_space_arr)
    avg_word_space=word_space/counter
    print ('avg_word_space',avg_word_space)

    for i in range(1, len(df)):
        if abs((df.loc[i]['X1']) - (df.loc[i - 1]['X2']))  <= median_word_space or re.match('^[a-zA-Z0-9_]+$',str(df.loc[i]['Word'])) and re.match('^[a-zA-Z0-9_]+$',str(df.loc[i-1]['Word'])):
            #print df.loc[i - 1]['Word'] + ' ' + df.loc[i]['Word']
            df.at[i, 'Word'] = df.loc[i - 1]['Word'] + ' ' + df.loc[i]['Word']
            df.at[i, 'X1'] = df.loc[i - 1]['X1']
            to_be_dropped.append(i - 1)
    df=df.drop(to_be_dropped)
    df=df.reset_index(drop=True)



    count_cols=df.groupby(['Y1']).count()
    min_cols=df.groupby(['Y1']).min()
    max_cols=df.groupby(['Y1']).max()
    #print mode(count_cols['X1'])
    #print mode(min_cols['X1'])
    #print mode(max_cols['X2'])
    df_count= df.groupby(['Y1']).count()
    df_min= df.groupby(['Y1']).min()
    df_max =df.groupby(['Y1']).max()
    df_j1=df_count.join(df_min,lsuffix='_count',rsuffix='_min')
    df_j2=df_j1.join(df_max,rsuffix='_max')
    #print df_j2
    df_final=pd.DataFrame(columns=["Word"])
    df= df.groupby('Y1')['Word'].apply(lambda x: "{%s}" % "\t".join(x))
    #print df
    #print type(df)
    df.replace("{","")
    #print df
    df_final=pd.DataFrame(df)
    #print df_final
    #print df_concat
    df_final['Word'].replace(to_replace=["{",'}'],regex=True,value="",inplace=True)
    #df_final=df_final.apply(lambda x: x.str.replace('{', ''))
    #print df_final
    #print df_final
    #df_final.to_csv("D:\Others\BillDog\CSV\Scrible.csv")
    df_final=df_final['Word'].str[0:-1].str.split('\t', expand=True).astype(str)
    #print df_final
    ncols=df_final.shape[1]


    while len(df_final[df_final[ncols-1]=='None'])>0:
        df_val=df_final[df_final[ncols-1]!='None']
        df_noval=  df_final[df_final[ncols-1]=='None']
        df_noval=df_noval.shift(1,axis=1)
        df_final=pd.concat([df_val,df_noval])
    #print df_final
    #print df_final.reset_index().sort_values(['Y1'])

    #print type(df_final.loc[195][2])
    df_final=df_final.reset_index().sort_values(['Y1'])
    nrows=df_final.shape[0]
    df_final=df_final.reset_index()
    df_final=df_final.drop(['Y1','index'],axis=1)
    #print df_final
    #print ncols, nrows
    nrows_df=df_final.shape[0]
    ncols_df=df_final.shape[1]
    df_to_process=df_final.apply(lambda x: x.str.replace(' ', ''))
    #print 'columns',df_final.dtypes.index
    df_dtype=df_to_process
    #print df_dtype
    for j in range(nrows):
        for i in (range(ncols)):
            if str(df_to_process.loc[j][i])=='nan':
                df_dtype.loc[j][i] = 'NaN'
            elif re.match(r"[+-]?([0-9])", df_to_process.loc[j][i]):
                df_dtype.loc[j][i]='Number'
            elif re.match('^[a-zA-Z0-9_]+$',str(df_to_process.loc[j][i])):
                df_dtype.loc[j][i]='String'

            else:
                df_dtype.loc[j][i]='Other'
    #print df_dtype
    df_mode=[]
    for i in range(ncols):
        df_mode.append( mode(df_dtype[df_dtype[0]!='NaN'][i]))

#    print df_to_process

    for i in range(1,ncols):
        if df_mode[i]=='String' and  df_mode[i-1]=='String':
            #if str(df_final[i-1])<>'nan' and (str(df_final[i])<>'nan'):
             df_final[i]=df_final[i-1].astype(str)+' '+df_final[i].astype(str)
             df_final = df_final.drop(i - 1, axis=1)
             df_final.replace(to_replace=['nan'], regex=True, value="", inplace=True)

    print (df_final)
    return df_final
    '''
            elif re.match('^[a-zA-Z0-9_]+$',str(df_to_process.loc[j][i])) and re.match('^[a-zA-Z0-9_]+$',str(df_to_process.loc[j][i-1])) and str(df_to_process.loc[j][i])<>'nan':

                 print (df_final.loc[j][i]), (df_final.loc[j][i-1])
                 for x in reversed(range(i)):
                     if x == 0:
                         break
                     else:
                        df_final.at[j,x]= str(df_final.loc[j][x-1])+' '+str(df_final.loc[j][x])
                        #df_final.at[j,x - 1]=''
                 print 'd',df_final.loc[j][i]
            else:
                print (df_final.loc[j][i]), (df_final.loc[j][i - 1]),re.match('^[a-zA-Z0-9_]+$',str(df_final.loc[j][i])),re.match('^[a-zA-Z0-9_]+$',str(df_final.loc[j][i-1]))
                continue
    '''

    #print df_final

def main():
    csv_file="/home/selvaprakash/BillD/CSV/Target.jpg_enh_clean_20180225185601.csv"
    if_no_head(csv_file)

if __name__=='__main__':
    main()
