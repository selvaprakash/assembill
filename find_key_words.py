import pandas as pd
import math
from statistics import mode, StatisticsError

image_path='/home/selvaprakash/BillD/Pics/Venkat_enh_20180221200719.jpg'
csv_file="/home/selvaprakash/BillD/CSV/Ch1.jpg_final_clean_20180319094528.csv"
head_words = ['Item','ltem','Name','Item Name','ltem Name','Due Date','Premium','Product','Product Name','Prod','Qty','Oty','Quantity','0uantity','Value','Amount','Desc','Description','Particulars','MRP','Rate']
tab_threshold=15
def_line_spacing=15
joined_words=['Item','Name','Desc']

def find_key_words(path):
    df1 = pd.read_csv(path,sep='|')
    df1=df1.reset_index(drop=True)
    print (df1)
    #print df1.columns.values.tolist()
    multi_word_head = []
    head_y_val=[]
    head_word_count=0
    head_search_count = 0
    head_cols=[]
    head_cols_df=pd.DataFrame()
    df_head=pd.DataFrame(columns= ["Word","Y"])
    for i in range(1, len(df1)):
        if type(df1.loc[i]["Word"]) is str:
            if df1.loc[i]["Word"].upper() in [x.upper() for x in head_words]:
                head_y_val.append(df1.loc[i]['Y1'])
                print (head_y_val,df1.loc[i]["Word"])
    if len(head_y_val)>1:
        try:
            head_loc_y= mode(head_y_val)
        except StatisticsError:
            head_loc_y= max(head_y_val)
    else:
        print ("No Heading")
        return
    #print 'Header Location ', math.ceil(df_head['Y1'].sum() / head_word_count)
    head_cols_df = df1.loc[df1['Y1']==head_loc_y]
    print ('head_cols_df',head_cols_df)

    #print head_cols_df.reset_index(drop=True)
    df_head1= head_cols_df.reset_index(drop=True)
    for i   in range(1,len(df_head1)):
        #print 'Diff',df_head1.loc[i]['X1'], df_head1.loc[i-1]['X1'] , (df_head1.loc[i]['X1']) - int(df_head1.loc[i-1]['X1']) #> tab_threshold:
        #df_head1[i-1][0] = df_head[i-1][0]+df_head[i][0]
        if (df_head1.loc[i]['X1']) - (df_head1.loc[i-1]['X2'])  < tab_threshold and  \
                (df_head1.loc[i]["Word"].upper() in [x.upper() for x in joined_words] and df_head1.loc[i]["Word"].upper() in [x.upper() for x in joined_words] ) :
            #print df_head1.loc[i - 1]['Word']+' '+ df_head1.loc[i]['Word']
            df_head1.at[i-1,'Word']=df_head1.loc[i - 1]['Word']+' '+ df_head1.loc[i]['Word']
            df_head1.at[i-1,'X2'] =df_head1.loc[i]['X2']
            #print 'dropped', df_head1.drop(df_head1.index[i])
            multi_word_head.append(i)
    #print multi_word_head
    #print df_head1
    df_head1=df_head1.drop(df_head1.index[multi_word_head])
    df_head2=df_head1[['Word','X1','Y1','X2','Y2']].reset_index(drop=True)

    print (df_head2)
    return df_head2

def main():
    #csv_file="/home/selvaprakash/BillD/CSV/Vishnu2.jpg_enh_clean_20180309215834.csv"
    #csv_file="/home/selvaprakash/BillD/CSV/Latta.jpg_enh_clean_20180305034439.csv"
    find_key_words(csv_file)
    #print df_all

if __name__ == '__main__':
    main()