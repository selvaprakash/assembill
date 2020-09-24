#!/usr/bin/python2.7

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
#import xlsxwriter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/selvaprakash/BillD/BillDog-018b2ee1875d.json'
src_image='/home/selvaprakash/BillD/Costco.jpg'
csv_path = '/home/selvaprakash/BillD/CSV/'
excel_path='/home/selvaprakash/BillD/Excel/'


def main(src_image):

    src_path = src_image.rsplit('/', 1)[0]
    src_file = src_image.rsplit('/', 1)[1]
    src_file_name=src_file.rsplit('.', 1)[0]
    # print src_path,src_file_name
    t=datetime.datetime.now()
    print (t)
    resi_image=src_path+'/'+src_file_name+'_res_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    final_image=src_path+'/'+src_file_name+'_final_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    #print (enh_image)
    csv_file=csv_path+src_file+'_final_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    new_csv_file=csv_path+src_file+'_final_clean_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    img_to_excel=src_path+'/'+src_file+'_excel_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    lined_img=src_path+'/'+src_file+'_line_'+t.strftime('%Y%m%d%H%M%S')+'.jpg'
    #print csv_file
    #print new_csv_file
    #print lined_img

    img_pre_process(src_image,resi_image,final_image,img_to_excel)
    detect_text(final_image,csv_file)
    cleanup_text_file(csv_file,new_csv_file)

    df_head= find_key_words(new_csv_file)
    #df_head=df_head.reset_index(drop=True)
    if df_head is None:
        #detect_text(final_image,csv_file)
        #cleanup_text_file(csv_file,new_csv_file)
        end_Y=find_item_end(new_csv_file,0)
        print ('end_Y',end_Y)
        print ('start if_no_head')
        df_final=if_no_head(new_csv_file,end_Y)
        ncols=df_final.shape[1]
        df_final.columns = [i for i in range(ncols)]
    else:
        start_Y =df_head['Y1'].max()
        print(start_Y)
        print ('start find_item_end')
        end_Y=find_item_end(new_csv_file,start_Y)
        print (end_Y)
        print ('start draw_split_lines')
        df_lines=draw_split_lines(new_csv_file,df_head,final_image,lined_img,end_Y)
        df=pd.read_csv(new_csv_file)
        df = df.loc[(df["Y1"] > start_Y) & (df["Y1"] <end_Y)]
        df=df.reset_index(drop=True)
        df_items=df[['Word','X1','Y1','X2','Y2']]
        df_items=df_items.reset_index(drop=True)
        print ('start arrange_items')
        print df_items
        df_final=arrange_items(df_items,df_head,df_lines)
        print df_final
    #print 'df_items',df_items
    #print df_items
    csv_file=csv_path+src_file_name+'_csv_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    print (df_final)
    df_final.to_csv(csv_file)
    #print src_path+'\\'+src_file_name+'_csv_'+t.strftime('%Y%m%d%H%M%S')+'.csv'
    excel_file=excel_path+src_file_name+t.strftime('%Y%m%d%H%M%S')+'.xlsx'

    print ('start to_excel')

    to_excel(df_final,img_to_excel,excel_file)

    return excel_file

    #('F2',src_image)
if __name__=='__main__':
    main(src_image)