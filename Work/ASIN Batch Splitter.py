import pandas as pd

# fi1=pd.read_excel(r"C:\Users\yanxiaod\Desktop\Dev\Splliter\AU_Orphan_RPA_20191019_Apparel.xlsx")
# fi2=pd.read_excel(r"C:\Users\yanxiaod\Desktop\Dev\Splliter\AU_Orphan_RPA_20191019_Shoes.xlsx")
# fi=pd.concat([fi1,fi2])
fi=pd.read_excel(input('Please add the file:').replace('"',''))

fi=fi.drop_duplicates()

# root=r'C:\Users\yanxiaod\Desktop\Dev\Splliter\AAA'

# tmp=pd.DataFrame()
# import os
# for v in os.listdir(root):
#     v=pd.read_excel(os.path.join(root,v))
#     tmp=pd.concat([tmp,v])

# tmp=tmp.reset_index(drop=True)
# tmp.to_excel('CheckPC.xlsx',index=False)

orphan=fi.orphan_asin.unique()

base=pd.DataFrame()
brand='N'
index=int(input('Please input starting batch ID:'))
for asin in orphan:
    lenbase=len(base)
    asin=str(asin)
    part=fi[fi.orphan_asin==asin]
    length=len(part)
    if lenbase+length>=1500: 
        print(asin,'to the next file.')
        if brand =='Y':
            base.to_excel(str(index)+'_b'+'.xlsx',index=False)
            index=index+1
        else:
            base.to_excel(str(index)+'.xlsx',index=False)
            index=index+1
        base=pd.DataFrame()
        base=base.append(part)
    else:
        base=base.append(part)

lock=(index-1)*2000
finew=fi.iloc[lock:,:]
base=base.append(finew)
if brand =='Y':
    base.to_excel(str(index)+'_b'+'.xlsx',index=False)
else:
    base.to_excel(str(index)+'.xlsx',index=False)
print('Done.')
