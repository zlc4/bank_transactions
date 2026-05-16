use banking_db;

-- Load Transactions into database
BEGIN TRY
	BEGIN TRANSACTION;

	-- Reset banking_staging table
	TRUNCATE TABLE bank_staging; 

	-- Insert data from CSV file into staging table (you will need to enter the entire filepath for the bank_transactions.csv)
	BULK INSERT bank_staging FROM '[ENTER FILEPATH FOR ETL OUTPUT FILE]' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n', FIRSTROW = 2);

	-- View the staging table to see the data
	SELECT * FROM bank_staging;

	-- Merge the data into the teams table
	MERGE account as target USING bank_staging as source ON target.account_number = source.account_number
		WHEN MATCHED THEN
			UPDATE SET
			target.account_number = source.account_number,
			target.customer_first_name = source.customer_first_name,
			target.customer_last_name = source.customer_last_name,
			target.balance = source.balance,
			target.transaction_date = source.transaction_date

		WHEN NOT MATCHED BY TARGET THEN
			INSERT (account_number, customer_first_name, customer_last_name, balance, transaction_date) 
				VALUES(source.account_number, source.customer_first_name, source.customer_last_name, source.balance, source.transaction_date)

		WHEN NOT MATCHED BY SOURCE THEN
			DELETE

		OUTPUT $action as action_taken, inserted.*, deleted.*;

		SELECT * FROM account;
	
	COMMIT;
END TRY
BEGIN CATCH
	ROLLBACK;
	PRINT ERROR_MESSAGE();
END CATCH



