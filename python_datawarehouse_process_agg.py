import pandas as pd
#from IPython.display import display
from sqlalchemy import create_engine
import time

csv_file_path = 'Superstore.csv'


def main(filename):
    pd.options.display.max_rows = 2000
    sales_data = pd.read_csv(csv_file_path,header=0,index_col=0, sep=',')
    #display(sales_data)
    #print(sales_data.shape[0])
    #print(sales_data.describe())
    #print(pd.options.display.max_rows) 
    performDataAccumlation(sales_data)

def performDataAccumlation(sales_data):
    column_name ="Sales"
    total_sales = sales_data[column_name].sum()
    average_sales = sales_data[column_name].mean()
    sales_by_category = sales_data.groupby('Category')[column_name].sum()
    sales_by_segment = sales_data.groupby('Segment')[column_name].sum()
    print(f"Total Sales: {total_sales}")
    print("X-------------------X------------------------X")
    print(f"Average Sales: {average_sales}")
    print("X-------------------X------------------------X")
    print(sales_by_category)
    print(sales_by_segment)
  

    # calculate time taken by the process
    start_time = time.time()
    sinkDatatoWarehouse(sales_by_category,sales_by_segment)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to ingest to Postgres: {execution_time} seconds")

def sinkDatatoWarehouse(sales_by_category,sales_by_segment):
    
    try:

        db_user = 'demoDB_owner'
        db_password = 'Pv4lxD3yuWJI'
        db_host = 'ep-billowing-pond-a450qgrv.us-east-1.aws.neon.tech'
        db_port = '5432'
        db_name = 'demoDB'

        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require')

        # sales_by_category_df = sales_by_category.reset_index()
        # # Rename the columns to 'Category Name' and 'Count'
        # sales_by_category_df.columns = ['Category_Name', 'Count']
        # # Display the resulting DataFrame
        # print(sales_by_category_df)

        sales_by_category.to_sql('sales_by_category', engine, if_exists='replace', index=True)

        
        sales_by_segment.to_sql('sales_by_segment', engine, if_exists='replace', index=True)

        print("Data inserted into PostgreSQL successfully.")
  
    except Exception as ex:
        print(ex)



if __name__ == "__main__":
    main(csv_file_path)