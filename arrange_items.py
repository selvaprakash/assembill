import pandas as pd

def arrange_items(df_items,df_head,df_lines):
    num_items = df_items.Y1.nunique()
    df_cons=pd.DataFrame(columns=df_head['Word'])
    df_items = df_items.reset_index(drop=True)
    df_head = df_head.reset_index(drop=True)
    df_lines = df_lines.reset_index(drop=True)
    print ('df_lines',df_lines)
    k=len(df_head)-1
    print ('k', k)
    j=0
    i=0
    Item_Mat=[['' for x in range(len(df_head))] for y in range(num_items)]
    print ('df_items',df_items)
    #x=0
    for j in range(num_items):
                while i<= (len(df_items)-1):
                    for k in range(len(df_head)):
                        if ((df_items.loc[i]["X1"]<df_lines.loc[k]["Line_X"])) :
                            Item_Mat[j][k]=str(Item_Mat[j][k])+' '+str(df_items.loc[i]["Word"])
                            print ('j',j,'i',i,'k',k)
                            print ('Word',df_items.loc[i]["Word"])
                            i+=1
                            break
                    if k==len(df_head)-1:
                        #j+=1
                        break
                    else:
                        continue
                #j+=1



    df_cons1=pd.DataFrame(data=Item_Mat,columns=df_head['Word'])
    print (df_cons1)
    return df_cons1