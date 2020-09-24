#!/usr/bin/python2.7


import pandas as pd

def_line_spacing=12
head_line_Y=158
csv_file="/home/selvaprakash/BillD/CSV/Venkat.jpg_final_clean_20180316130931.csv"
end_key_words= ['Item','Total','Items','Qty','Quantity','Net','Subtotal','Amount','Subtota']

def find_item_end(csv_file,head_line_Y):
    def_line_spacing=12
    if head_line_Y==0:
        def_line_spacing=100
    print 'def_line_spacing',def_line_spacing
    df=pd.read_csv(csv_file)
    df=df.loc[df["Y1"]>head_line_Y]
   # print (df)
    sorted_df = df.sort_values(by=['Y1'])
    df = sorted_df.reset_index(drop=True)
    print (df)
    #sorted_df.to_csv("D:\Others\BillDog\Latta\Sorted_Latta2.csv")



    df = df.sort_values(by=['Y1','X1'])
    df1=pd.DataFrame(columns=['Y1','Word'])
    print df
    #df.to_csv("D:\Others\BillDog\Latta\Sorted_Latta21.csv")
    for i in range(1, len(df)):
        if df.loc[i]['Y1']>head_line_Y:
            if ((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1'])) > 3*def_line_spacing or str(df.loc[i]["Word"]).upper() in [x.upper() for x in end_key_words]:
                print (df.loc[i-1]['Y1'],df.loc[i]['Y1'],df.loc[i-1]['Word'])
                df1=df1.append({'Y1':df.loc[i]['Y1'],'Word':df.loc[i]['Word']},ignore_index=True)

            else:
                continue
        print 'df1', df1
        print ('end_Y', df1['Y1'].min())
        return df1['Y1'].min()


def main():
    find_item_end(csv_file,head_line_Y)

if __name__ == '__main__':
    main()