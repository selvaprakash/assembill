import pandas as pd

def_line_spacing=12
head_line_Y=478
csv_file="/home/selvaprakash/BillD/CSV/Thang_enh.csv"

def find_item_end(csv_file,head_line_Y):
    df=pd.read_csv(csv_file)
    df=df.loc[df["Y1"]>head_line_Y]
    #print df
    sorted_df = df.sort_values(by=['Y1'])
    df = sorted_df.reset_index(drop=True)
    #sorted_df.to_csv("D:\Others\BillDog\Latta\Sorted_Latta2.csv")

    for i in range(1, len(df)):
        if abs((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1'])) <def_line_spacing:
            #print df.loc[i - 1]['Y1'], df.loc[i]['Y1'], df.loc[i - 1]['Word'], df.loc[i]['Word']
            df.at[i,'Y1']=df.loc[i - 1]['Y1']
        else:
            continue
    df = df.sort_values(by=['Y1','X1'])
    df1=pd.DataFrame(columns=['Y1','Word'])
    #df.to_csv("D:\Others\BillDog\Latta\Sorted_Latta21.csv")
    for i in range(1, len(df)):
        if df.loc[i]['Y1']>head_line_Y:
            if ((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1'])) > 3*def_line_spacing:
                print (df.loc[i-1]['Y1'],df.loc[i]['Y1'],df.loc[i-1]['Word'])
                df1=df1.append({'Y1':df.loc[i]['Y1'],'Word':df.loc[i]['Word']},ignore_index=True)

            else:
                continue
        #print 'df1', df1
        print ('end_Y', df1['Y1'].min())
        return df1['Y1'].min()


def main():
    find_item_end(csv_file,head_line_Y)

if __name__ == '__main__':
    main()