def data_cleaner():

    import pandas as pd
    import re
    df = pd.read_csv("~/store_files_airflow/raw_store_transactions.csv")

#clean store location spl symbols
    def clean_store_location(st_loc):
        return re.sub(r'[^\w\s]','',st_loc).strip()

#will clean the product_id column
    def clean_product_id(pd_id):
        matches = re.findall(r'\d+',pd_id)
        if matches:
            return matches[0]
        return pd_id

# remove dollar from all the price column
    def remove_dollar(amount):
        return float(amount.replace('$',''))

# func call to clean_store_location and clean_product_id
    df['STORE_LOCATION]']=df['STORE_LOCATION'].map(lambda x: clean_store_location(x))
    df['PRODUCT_ID']=df['PRODUCT_ID'].map(lambda x:clean_product_id(x))

    for to_clean in ['MRP','CP','DISCOUNT','SP']:
        df[to_clean]=df[to_clean].map(lambda x: remove_dollar(x))

    df.to_csv('~/store_files_airflow/clean_store_transactions.csv', index=False)

