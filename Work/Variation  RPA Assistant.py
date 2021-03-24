import os
import numpy
import pandas as pd
import time
base=input('Please input file path:')
file=str(input('Please input file name:'))
frame=pd.DataFrame()
frame1=pd.DataFrame()
filterlist=batchlist=pd.read_excel('batch.xlsx').batch_id.tolist()
filterlist=[str(x) for x in filterlist]
for f in os.listdir(base):
    if str(f) in filterlist:
        try:
            batch={}
            batch1={}
            fpath=os.path.join(base,f)
            for n in os.listdir(fpath):
                if str(file)=='Result':
                    if str(file)in str(n):
                        npath=os.path.join(fpath,n)
                        nn=pd.read_excel(npath,sheet_name='Sheet1').fillna('')
                        for x in nn.index:
                            batch[x]=str(f)
                        newcol=pd.DataFrame.from_dict(batch,orient='index')
                        newcol.columns=['batch']
                        nn=pd.concat([nn,newcol],axis=1)
                        frame=pd.concat([frame,nn])
                        print(frame.columns)
                        #####
                        error=pd.read_excel(npath,sheet_name='Error').fillna('')
                        for y in error.index:
                            batch1[y]=str(f)
                        newerror=pd.DataFrame.from_dict(batch1,orient='index')
                        newerror.columns=['batch']
                        error=pd.concat([error,newerror],axis=1)
                        frame1=pd.concat([frame1,error])
                else:
                    if str(file) in str(n):
                        npath=os.path.join(fpath,n)
                        nn=pd.read_excel(npath).fillna('')
                        for x in nn.index:
                            batch[x]=str(f)
                        newcol=pd.DataFrame.from_dict(batch,orient='index')
                        newcol.columns=['batch']
                        nn=pd.concat([nn,newcol],axis=1)
                        frame=pd.concat([frame,nn],ignore_index=True)
        except:
            pass
import openpyxl
frame=frame.drop_duplicates(subset=None, keep='first', inplace=False)
writer=pd.ExcelWriter('Output_'+str(file)+str(int(time.time())+1)+'.xlsx')
frame.to_excel(writer,str(file),index=False)
try:
    frame1.to_excel(writer,'Error',index=False)
except:
    pass
writer.save()
