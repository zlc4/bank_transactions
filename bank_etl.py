import sys, pandas, datetime, os
os.environ["PYSPARK_PYTHON"] = sys.executable;
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable;
os.environ["SPARK_CONF_DIR"] = os.path.dirname(os.path.abspath(__file__));

from pyspark.sql import SparkSession
import pyspark.sql.functions as f

def run_pyspark_etl(input_file):
  
    spark = SparkSession.builder.appName('BankSparkApp').getOrCreate(); # CREATE SPARK SESSION
    #spark.sparkContext.setLogLevel("ERROR");  #  Options: ERROR, WARN, INFO, DEBUG

    try:
        # EXTRACTION
        print('Extracting...');
        
        # READ THE EXTERNAL OUTPUT FILE (bank_extl.csv)
        df = spark.read.format('csv') \
        .option('header', True).option('inferSchema', True).load(input_file);

        # --TRANSFORM--
        print('Transforming...');

        # Transform the account number to be formatted as BANK####
        df = df.withColumn('AccountNumber', f.concat(f.lit('BANK'), f.lpad(f.col('AccountNumber'), 4, '0')));
                                                                
        # Transform the customer name into first and last name column
        df = df.withColumn('FirstName', f.split(f.col('CustomerName'), ' ').getItem(0)) \
                .withColumn('LastName', f.split(f.col('CustomerName'), ' ').getItem(1));
        
        # Remove the customer name from the table
        df = df.drop(f.col('CustomerName'));

        # Remove the $ from the balance amount
        df = df.withColumn('Balance', f.split(f.col('Balance'), '\$').getItem(1));

        # Reorder the column names to prepare for loading
        df = df.select('AccountNumber', 'FirstName', 'LastName', 'Balance','TransactionDate');
        
         # --LOAD--
        print('Loading...');
        etl_file = 'bank_etl_output.csv'; # DEFINE ETL FILE

        #df.printSchema(); # PRINT THE DATA SCHEMA
        df.show(); #PRINT THE DATA FRAME

        # WRITE TO ETL FILE
        df.coalesce(1) \
          .write.format('csv') \
          .mode('overwrite') \
          .option('header', 'true') \
          .save(etl_file);
    
    except Exception as e:
        print(f'ETL failed due to {e}');
        sys.exit(-1);
    
    finally:
        #END SPARK SESSION
        spark.stop();  

def run_pandas_etl (input_file):
        
    try:
        # --EXTRACTION--
        print('Extracting...');
        df = pandas.read_csv(filepath_or_buffer=input_file);  # READ THE EXTERNAL OUTPUT FILE (bank_extl.csv)
    
        # --TRANSFORM--
        print('Transforming...');

        # Transform the account number to be formatted as BANK####
        df['AccountNumber'] = df['AccountNumber'].apply(lambda x: f'BANK{x:04}');

        # Transform the customer name into first and last name column
        df[['FirstName', 'LastName']] = df['CustomerName'].str.split(n=1, expand=True);
        df = df.drop(columns=['CustomerName']);

        # Remove the $ from the balance amount
        df['Balance'] = df['Balance'].str.split(pat='$', n=1, expand=True)[1];

        # Reorder the column names to prepare for loading
        df = df[['AccountNumber', 'FirstName', 'LastName', 'Balance','TransactionDate']];

        # --LOAD--
        print('Loading...');
        print(df); #PRINT THE DATA FRAME
        etl_file = 'bank_etl_output.csv'; # DEFINE ETL FILE
        df.to_csv(etl_file, index=False); # WRITE TO ETL FILE
        
    except Exception as e:
        print(f'ETL failed due to error: {e}');
        sys.exit(-1);

def main():
    begin_etl_time = datetime.datetime.now()
    print(f'ETL Process Began at {begin_etl_time}\n');

    input_file = 'bank_transactions.csv';
    etl_process = input('Enter 1 for Pandas, Enter 2 for PySpark: ');

    # decide which ETL process to use
    match (etl_process):
        case '1':  # ETL PROCESS FOR PANDAS 
            run_pandas_etl(input_file= input_file);
        case '2': # ETL PROCESS FOR PYSPARK
            run_pyspark_etl(input_file= input_file);
        case _:
            print('Invalid Input');
            sys.exit(-1);
   
    end_etl_time = datetime.datetime.now();
    print(f'ETL Process Ended at {end_etl_time}');

if __name__ == "__main__":
    main();