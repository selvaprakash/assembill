#!/usr/bin/python3.6

import pandas as pd
import os
from detect_text import detect_text
from enhance_image import img_pre_process
from cleanup_text_file import cleanup_text_file
from find_key_words import find_key_words
from find_item_end import find_item_end
from draw_split_lines import draw_split_lines
from arrange_items import arrange_items
from to_excel import to_excel
import datetime
from ifnohead import if_no_head
from sendemail import sendmail
from topdf import topdf
#import xlsxwriter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/selvaprakash/BillD/BillDog-018b2ee1875d.json'
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/mnt/c/d/BillD/BillDog-018b2ee1875d.json'
src_image='/home/selvaprakash/BillD/BigBill.jpg' #IMG_20180314_135618731.jpg #IMG_20180603_143723969.jpg
csv_path = '/home/selvaprakash/BillD/CSV/'
excel_path='/home/selvaprakash/BillD/Excel/'


def main(src_image,emailid):

    src_path = src_image.rsplit('/', 1)[0]
    src_file = src_image.rsplit('/', 1)[1]
    src_file_name=src_file.rsplit('.', 1)[0]
    # print src_path,src_file_name
    t=datetime.datetime.now()
    print (t)
    resi_image=src_path+'/'+src_file_name+'_res_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    final_image=src_path+src_file_name+'_final_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    #print (enh_image)

    csv_file=csv_path+src_file+'_final_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    new_csv_file=csv_path+src_file+'_final_clean_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    img_to_excel=src_path+'/'+src_file+'_excel_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    lined_img=src_path+'/'+src_file+'_line_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    #print csv_file
    print ('Final Image', final_image)
    #print lined_img

    img_pre_process(src_image,resi_image,final_image,img_to_excel)
    detect_text(final_image,csv_file)
    cleanup_text_file(csv_file,new_csv_file)
    print ('Start find_key_words')
    df_head= find_key_words(new_csv_file)
    #df_head=df_head.reset_index(drop=True)
    if df_head is None:
        #detect_text(final_image,csv_file)
        #cleanup_text_file(csv_file,new_csv_file)
        print ('Start Find Item End')
        end_Y=find_item_end(new_csv_file,0)

        print ('start if_no_head')
        if end_Y is None:
            df_final=if_no_head(new_csv_file,1000)

        else:
            df_final=if_no_head(new_csv_file,end_Y)
            ncols=df_final.shape[1]
            df_final.columns = [i for i in range(ncols)]
        print ('end_Y',end_Y)
    else:
        start_Y =df_head['Y1'].max()
        print(start_Y)
        print ('start find_item_end')

        end_Y=find_item_end(new_csv_file,start_Y)
        if end_Y is None:
            end_Y=1000
        print (end_Y)
        print ('start draw_split_lines')
        df_lines=draw_split_lines(new_csv_file,df_head,final_image,lined_img,end_Y)
        df=pd.read_csv(new_csv_file,sep='|')
        df = df.loc[(df["Y1"] > start_Y) & (df["Y1"] <end_Y)]
        df=df.reset_index(drop=True)
        df_items=df[['Word','X1','Y1','X2','Y2']]
        df_items=df_items.reset_index(drop=True)
        print ('start arrange_items')
        print (df_items)
        df_final=arrange_items(df_items,df_head,df_lines)
        print (df_final)
    #print 'df_items',df_items
    #print df_items
    csv_file=csv_path+src_file_name+'_csv_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    print (df_final)
    df_final.to_csv(csv_file,sep='|')
    topdf(csv_file)
    #print src_path+'\\'+src_file_name+'_csv_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    excel_file=excel_path+src_file_name+t.strftime('%Y%m%d%H%M%S')+'.xlsx'

    print ('start to_excel')

    to_excel(df_final,img_to_excel,excel_file)

    sendmail('assembill.contact@gmail.com',emailid,src_file_name+t.strftime('%Y%m%d%H%M%S')+'.xlsx')

    return excel_file

    #('F2',src_image)
if __name__=='__main__':
    emailid='assembill.contact@gmail.com'
    main(src_image,emailid)