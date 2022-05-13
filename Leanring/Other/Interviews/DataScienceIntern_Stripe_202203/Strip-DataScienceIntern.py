#!/usr/bin/env python
# coding: utf-8

# ## Stripe: Data Science Intern - Written Project
# #### Frank Yue Ying | 2022-03-07

# ### Raw Data
# merchant transaction activity, for merchants that start over a 2 year period (2033-2034). The data spans from 1/1/33 through 12/31/34. Each observation is a transaction amount in cents.
# #### Columns
# 1. ID: [1,1513719] natural order of rows in raw data
# 2. merchant: unique merchant ID with length of 10 digits & letters
# 3. time: format as YYYY-MM-DD HH:mm:ss, assuming in the same timezone
# 4. amount_usd_in_cents: integer number in cents

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


#Load the data
raw_data = pd.read_csv("takehome_ds_written.csv",header = 0,index_col =0)
# raw_data.head()


# In[3]:


#Transform the data: break time into year, month, day
data = raw_data.copy()
def convert_time(row,x):
    if x == 'year':
        return row.split(" ")[0].split("-")[0]
    elif x == 'month':
        return row.split(" ")[0].split("-")[1]
    elif x == 'day':
        return row.split(" ")[0].split("-")[2]

data['year'] = np.vectorize(convert_time)(data['time'], 'year')
data['month'] = np.vectorize(convert_time)(data['time'], 'month')
data['day'] = np.vectorize(convert_time)(data['time'], 'day')


# In[4]:


# set up unique merchant-based tracking table 
merchants = data['merchant'].unique().tolist()
merchant_data = pd.DataFrame(columns = ["id"])
# merchant_data.set_index("id")
merchant_data_columns_dict = {}
for year in ['count-2033','count-2034','volume-2033','volume-2034']:
    for month in range(1,13):
        merchant_data[year+"-"+str(month)] = 0
        merchant_data_columns_dict[year+"-"+str(month)] = 0


# In[ ]:

# calculate monthly transaction count and volume per merchant
def query_merchant(dt,merchant,merchant_data_columns_dict):
    merchant_data_values = merchant_data_columns_dict.copy()
    merchant_data = dt.loc[dt['merchant'] == merchant]
    merchant_data = merchant_data.groupby(["year","month"]).agg({"amount_usd_in_cents": [np.count_nonzero, np.sum]}).reset_index()
    for index, row in merchant_data.iterrows():
        merchant_data_values['count-'+str(row['year'].values[0])+"-"+str(int(row['month'].values[0]))] = int(row[2])
        merchant_data_values['volume-'+str(row['year'].values[0])+"-"+str(int(row['month'].values[0]))] = int(row[3])
    return pd.DataFrame([merchant_data_values], columns=merchant_data_values.keys())

for merchant in merchants:
    merchant_dt = query_merchant(data,merchant,merchant_data_columns_dict)
    merchant_dt['id'] = merchant
    # merchant_dt.set_index("id")
    merchant_data = pd.concat([merchant_data, merchant_dt], axis=0)

# merchant_data.to_csv("merchant_data.csv", index = False)
# merchant_data = pd.read_csv("merchant_data.csv",header = 0,index_col =0)
merchant_data.set_index("id",inplace=True)
# merchant_data.head()


# In[49]:

# Identify business types based on 50the percentile from transaction count and volume
merchant_data_businesstype = merchant_data.copy()
merchant_data_businesstype['count_average'] = 0
merchant_data_businesstype['volume_average'] = 0
for index, row in merchant_data.iterrows():
    merchant_data_businesstype.at[index, 'count_average'] = row[0:24].sum()/np.count_nonzero(row[0:24].to_numpy())
    merchant_data_businesstype.at[index, 'volume_average'] = row[24:48].sum()/np.count_nonzero(row[24:48].to_numpy())

# In[52]:


count_average_50 = merchant_data_businesstype['count_average'].quantile(
    q=0.50,                      # The percentile to calculate
#     axis=1,                     # The axis to calculate the percentile on
#     numeric_only=True,          # To calculate only for numeric columns
    interpolation='linear'      # The type of interpolation to use when the quantile is between 2 values
)
volume_average_50 = merchant_data_businesstype['volume_average'].quantile(
    q=0.50,                      # The percentile to calculate
#     axis=1,                     # The axis to calculate the percentile on
#     numeric_only=True,          # To calculate only for numeric columns
    interpolation='linear'      # The type of interpolation to use when the quantile is between 2 values
)


# In[57]:


merchant_data_businesstype['count_average_50'] = np.where(merchant_data_businesstype['count_average']> count_average_50 , 1, 0)
merchant_data_businesstype['volume_average_50'] = np.where(merchant_data_businesstype['volume_average']> volume_average_50 , 1, 0)


# In[58]:

merchant_data_businesstype.to_csv("merchant_data_businesstype.csv")


# In[ ]:

# Getting merchants that never churn, calculate their ratios
count_columns_names = [str(x) for x in merchant_data_columns_dict.keys() if "count" in x ]
volume_columns_names = [str(x) for x in merchant_data_columns_dict.keys() if "volume" in x]
count_columns_names
merchant_data_nonchurn = merchant_data[~(merchant_data == 0).any(axis=1)].copy()
merchant_data_nonchurn['min_count'] = merchant_data_nonchurn.loc[:,count_columns_names].min(axis=1)
merchant_data_nonchurn['avg_count'] = merchant_data_nonchurn[count_columns_names].mean(axis=1)
merchant_data_nonchurn['min_volume'] = merchant_data_nonchurn[volume_columns_names].min(axis=1)
merchant_data_nonchurn['avg_volume'] = merchant_data_nonchurn[volume_columns_names].mean(axis=1)
merchant_data_nonchurn['min/avg_count'] = merchant_data_nonchurn['min_count']/merchant_data_nonchurn['avg_count']
merchant_data_nonchurn['min/avg_volume'] = merchant_data_nonchurn['min_volume']/merchant_data_nonchurn['avg_volume']
print(merchant_data_nonchurn['min/avg_count'].mean(axis = 0))
print(merchant_data_nonchurn['min/avg_volume'].mean(axis = 0))
# Insights: min/avg_count = 0.324346, min/avg_volume = 0.272355, use 30% as the indicator for potential default


# In[ ]:

# Getting moving averages and assign scores for every month 
merchant_data_churnpotential = merchant_data[(merchant_data == 0).any(axis=1)].copy().reset_index()
merchant_data_churntable = pd.DataFrame(columns = ["id"])
merchant_data_churntable.set_index("id")
merchant_data_churntable_dict = {}
for year in ['2033','2034']:
    for month in range(1,13):
        merchant_data_churntable[year+"-"+str(month)] = 0
        merchant_data_churntable_dict[year+"-"+str(month)] = 0
for index, row in merchant_data_churnpotential.iterrows():
    merchant_data_churntable_dict_copy = merchant_data_churntable_dict.copy()
    for i in range(4,25):
        moving_avg_count = row[ i-3:i].mean()
        moving_avg_volume = row[ i+12-3:i+12].mean()
        merchant_data_churnpotential[str(i)+"-mac"] = moving_avg_count
        merchant_data_churnpotential[str(i)+"-mav"] = moving_avg_volume
        if (int(row[i]) <= moving_avg_count*.3 and int(row[i+12]) <= moving_avg_volume*.3 and moving_avg_count > 0 ):
            merchant_data_churntable_dict_copy[list(merchant_data_churntable_dict_copy)[i-1]] = -1
        elif (int(row[i]) > moving_avg_count*.3 or int(row[i+12]) > moving_avg_volume*.3):
            merchant_data_churntable_dict_copy[list(merchant_data_churntable_dict_copy)[i-1]] = 1
        else:
            merchant_data_churntable_dict_copy[list(merchant_data_churntable_dict_copy)[i-1]] = 0
    merchant_row = pd.DataFrame([merchant_data_churntable_dict_copy], columns=merchant_data_churntable_dict_copy.keys())
    merchant_row['id'] = str(row[0])
    merchant_data_churntable = pd.concat([merchant_data_churntable, merchant_row], axis=0)
merchant_data_churntable['total_score'] = merchant_data_churntable.iloc[:,1:25].sum(axis=1)
merchant_data_churntable['last_6_month_score'] = merchant_data_churntable.iloc[:,-7:-1].sum(axis=1)

# In[ ]:


merchant_data_churntable.to_csv("merchant_data_churntable.csv")


# In[ ]:


# merchant_data_churnpotential.to_csv("merchant_data_churnpotential.csv")



# ### References
# 1. https://chaotic-flow.com/saas-metrics-faqs-what-is-churn/#:~:text=SaaS%20churn%20is%20the%20percentage,important%20parameter%20in%20revenue%20forecasting.
# 2. https://dataconomy.com/2017/07/churn-predictive-analytics/
