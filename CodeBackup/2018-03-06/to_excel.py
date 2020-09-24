import pandas as pd
import xlsxwriter
import numpy as np


def to_excel(df,img,excel):


    nrows=df.shape[0]
    ncols=df.shape[1]
    df=df.reset_index(drop=True)
    df = df.fillna(0)
    print (nrows,ncols)

    print (df)
    #print len(df.columns)
    #print df.columns[1]
    row = 1
    col = 0
    workbook=xlsxwriter.Workbook(excel)
    worksheet=workbook.add_worksheet()
    for i in range(ncols):
        worksheet.write(0, col,df.columns[i])
        col+=1
    col=0
    for i in range(nrows):
        for j in range(ncols):
            print (df.iloc[i][j])
            #content=(df.iloc[i][j])
            worksheet.write(row, col, df.iloc[i][j])
            col+=1
        row+=1
        col=0

    worksheet.insert_image(2,ncols+1, img)
    workbook.close()

def main():
    df = pd.read_csv("D:\Others\BillDog\Pics\CSV\Thang.csv")
    img = 'D:\Others\BillDog\Pics\Thang.jpg'
    excel = 'D:\Others\BillDog\Pics\CSV\XLSX_sample1.xlsx'
    to_excel(df,img,excel)

if __name__=='__main__':

    main()