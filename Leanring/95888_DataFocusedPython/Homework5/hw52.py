# -*- coding: utf-8 -*-
# Frank Yue Ying
# yying2

import pandas as pd

gdp = pd.read_csv("countryGDP.csv", header = 0)
print(gdp)
medals = pd.read_csv("medals.csv", header = None)
print(medals)
medals.rename(columns = {0:'Country',1:"Gold",2:'Silver',3:'Bronze',4:'Country_Code'},inplace = True)
medals['Total'] = 3*medals['Gold'] + 2*medals['Silver'] + 1*medals['Bronze']
print(medals.sort_values(by=["Total"], ascending = False))
print("Total Gold: ",medals['Gold'].sum())
print("Total Silver: ",medals['Silver'].sum())
print("Total Bronze: ",medals['Bronze'].sum())
print("Total Medal: ",medals['Gold'].sum()+medals['Silver'].sum()+medals['Bronze'].sum())
print("Total Weighted: ",medals['Total'].sum())
popMedals = gdp[["Country","GDP","Population"]]
popMedals = popMedals.merge(medals,on= 'Country')
popMedals = popMedals[["Country","GDP","Total","Population"]]
print(popMedals.sort_values(by=["Country"]))
popMedals['Formula'] = 0.215 * (popMedals['Population']*popMedals['GDP']**2)**(1/3)
print(popMedals.sort_values(by=["Country"]))
print("Correlation of total against population =",round(popMedals['Total'].corr(popMedals['Population']),2))
print("Correlation of total against GDP =",round(popMedals['Total'].corr(popMedals['GDP']),2))
print("Correlation of total against Formula =",round(popMedals['Total'].corr(popMedals['Formula']),2))