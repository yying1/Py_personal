import pandas as pd
import re
import numpy as np
import os
import win32com.client
import win32com
import os
import sys
from datetime import datetime

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inboxsuc = outlook.Folders('yanxiaod@amazon.com').Folders("Variation")
#inboxfal = outlook.Folders("存档").Folders("RPA").Folders("Failed")
dicinfo={}
info=pd.DataFrame()
for item in inboxsuc.items:
    try:
        rein=[]
        b = item.body
        b=b.replace('\n','')
        b=b.split('\r')
        b[8]=b[8].replace( 'Task_Info:','')
        index=[0,2,4,5,6,7,8]
        for x in index:
            rein.append(b[x])
        rein=pd.DataFrame(rein).T
        info=pd.concat([info,rein])
    except:
        pass

##info=pd.DataFrame.from_dict(dicinfo,orient='index')

info.columns=['login','bot','start','end','runtime','taskinfo','comment']
info.taskinfo=info.taskinfo.apply(lambda x: x.replace('Task_Info:',''))
info.login=info.login.apply(lambda x: x.replace('Hi,',''))

info.bot=info.bot.apply(lambda x: x.replace('Robot_ID:',''))

info.start=info.start.apply(lambda x: x.replace('Start_Time:',''))
info.end=info.end.apply(lambda x: x.replace('End_Time:',''))


info.comment=info.comment.apply(lambda x: x.replace('Task_Status:',''))
mail=info.taskinfo.str.split('_',expand=True)

info=pd.concat([mail,info],axis=1)

info.to_excel('Info.xlsx',index=False)

