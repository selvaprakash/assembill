import cv2
import numpy as np
import  pandas as pd
import math

csv_file="D:\Others\BillDog\CSV\Peri1_enh_clean.csv"
lined_img='D:\Others\BillDog\Pics\Peri1_lined.jpg'
def_line_spacing=12
start_Y=371
end_Y=582

head_words = ['Item','ltem','Name','Item Name','ltem Name','Product','Prod','Qty','Oty','Quantity','0uantity','Value','Amount','Desc','Particulars','MRP','Rate']
tab_threshold=10
def_line_spacing=15

'''
def find_key_words(path):
    df1 = pd.read_csv(path)
    #print df1.columns.values.tolist()
    multi_word_head = []
    head_y_val=0
    head_word_count=0
    head_search_count = 0
    head_cols=[]
    head_cols_df=pd.DataFrame()
    df_head=pd.DataFrame(columns= ["Word","Y"])
    for i  in range(1, len(df1)):
        if df1.loc[i]["Word"].upper() in head_words:
            #print df1.loc[i]['Word'] ,df1.loc[i]['Y1']
            head_y_val=max(head_y_val,df1.loc[i]['Y1'])
            head_word_count+=1
            df_head=df_head.append(df1.loc[i])
            if head_word_count <2:
                head_search_count+=1
                continue
            elif head_word_count == 2:
                break
    #print df_head
    head_loc_y = math.ceil(df_head['Y1'].sum() / head_word_count)
    print 'Header Location ', math.ceil(df_head['Y1'].sum() / head_word_count)
    head_cols_df = df1.loc[(df1['Y1'] >= head_loc_y - def_line_spacing) & (df1['Y1'] <= head_loc_y + def_line_spacing)]
    #print head_cols_df

    #print head_cols_df.reset_index(drop=True)
    df_head1= head_cols_df.reset_index(drop=True)
    for i   in range(1,len(df_head1)):
        #print 'Diff',df_head1.loc[i]['X1'], df_head1.loc[i-1]['X1'] , (df_head1.loc[i]['X1']) - int(df_head1.loc[i-1]['X1']) #> tab_threshold:
        #df_head1[i-1][0] = df_head[i-1][0]+df_head[i][0]
        if (df_head1.loc[i]['X1']) - (df_head1.loc[i-1]['X2']) < tab_threshold:
            print df_head1.loc[i - 1]['Word']+' '+ df_head1.loc[i]['Word']
            df_head1.at[i-1,'Word']=df_head1.loc[i - 1]['Word']+' '+ df_head1.loc[i]['Word']
            df_head1.at[i-1,'X2'] =df_head1.loc[i]['X2']
            #print 'dropped', df_head1.drop(df_head1.index[i])
            multi_word_head.append(i)
    #print multi_word_head
    #print df_head1
    df_head1=df_head1.drop(multi_word_head)
    df_head2=df_head1[['Word','X1','Y1','X2','Y2']]
    #print 'df_head2',df_head2
    #print df_head1.reset_index(drop=True)
    print 'Header Y Value Loc', head_y_val
    #print 'Header Word Count', head_word_cout

    return df_head2
'''
def draw_split_lines(csv_file,df_head,orig_image,lined_img,end_Y):
    line_y=[]
    print (df_head)
    df=pd.read_csv(csv_file)
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
    return df_lines
def main():
    df_head=find_key_words(csv_file)
    draw_split_lines(csv_file,df_head.reset_index(drop=True),lined_img)

if __name__=='__main__':
    main()