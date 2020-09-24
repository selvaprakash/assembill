import pandas as pd

def_line_spacing=10
def_char_spacing=6
head_line_Y=371
csv_file="D:\Others\BillDog\CSV\Peri1_enh.csv"
new_csv_file="D:\Others\BillDog\CSV\Peri1_enh_clean.csv"

def cleanup_text_file(csv_file,new_csv_file):
    df=pd.read_csv(csv_file)
    sorted_df = df.sort_values(by=['Y1'])
    df = sorted_df.reset_index(drop=True)
    print (df)
    #df.to_csv("D:\Others\BillDog\CSV\Sorted_Peri1_enh.csv")

    for i in range(1, len(df)):
        if abs((df.loc[i]['Y1']) - (df.loc[i - 1]['Y1'])) <def_line_spacing:
            #print df.loc[i - 1]['Y1'], df.loc[i]['Y1'], df.loc[i - 1]['Word']
            df.at[i,'Y1']=df.loc[i - 1]['Y1']
        else:
            continue
    df = df.sort_values(by=['Y1','X1'])

    sorted_df = df.sort_values(by=['X1'])
    df = sorted_df.reset_index()

    for i in range(1, len(df)):
        if abs((df.loc[i]['X1']) - (df.loc[i - 1]['X1'])) <def_char_spacing:
            #print df.loc[i - 1]['Y1'], df.loc[i]['Y1'], df.loc[i - 1]['Word']
            df.at[i,'X1']=df.loc[i - 1]['X1']
        else:
            continue
    df = df.sort_values(by=['Y1','X1'])

    df.to_csv(new_csv_file)




def main():
    df_all = cleanup_text_file(csv_file,new_csv_file)
    print (df_all)



if __name__ == '__main__':
    main()