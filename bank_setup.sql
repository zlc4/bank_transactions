-- CREATE banking_db Database
-- create database banking_db;
use banking_db;

-- BASIC
-- TABLE 1: Staging Table Information
CREATE TABLE bank_staging (
	account_number varchar(8) NOT NULL,
	customer_first_name varchar(50),
	customer_last_name varchar(50),
	balance DECIMAL(10,2),
	transaction_date DATE
);

-- TABLE 2: Staging Table Information
CREATE TABLE account (
	account_id INT NOT NULL IDENTITY(1,1),
	account_number varchar(8) NOT NULL,
	customer_first_name varchar(50),
	customer_last_name varchar(50),
	balance DECIMAL (10,2), -- How much is in the account
	transaction_date DATE,
	CONSTRAINT account_PK1 PRIMARY KEY (account_id)
);

/* ADVANCED
-- TABLE 1: Customer Information
CREATE TABLE customer (
	customer_id INT NOT NULL IDENTITY (1,1),
	customer_first_name varchar(50),
	customer_middle_initial char(1),
	customer_last_name varchar(50),
	CONSTRAINT customer_PK1 PRIMARY KEY (customer_id)
);

-- TABLE 2: Account Information
CREATE TABLE account (
	account_id INT NOT NULL IDENTITY (1,1),
	customer_id INT NOT NULL,
	account_type varchar(50), -- Savings or Checking
	account_amount DECIMAL (10,2), -- How much is in the account
	CONSTRAINT account_PK1 PRIMARY KEY (account_id),
	CONSTRAINT account_FK1 FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- TABLE 3: Tranasactions Information
CREATE TABLE transactions (
	transactions_id INT NOT NULL IDENTITY (1,1),
	transaction_type varchar(15),
	from_account_id INT NOT NULL,
	from_account_amount DECIMAL(10,2), -- How much is in the account
	to_account_id INT NOT NULL,
	to_account_amount DECIMAL(10,2), -- How much is in the account
	transaction_time TIMESTAMP,
	CONSTRAINT transactions_PK1 PRIMARY KEY (transactions_id),
	CONSTRAINT transactions_FK1 FOREIGN KEY (from_account_id) REFERENCES account(account_id),
	CONSTRAINT transactions_FK2 FOREIGN KEY (from_account_id) REFERENCES account(account_id)
);*/

/*
-- DROP TABLES
DROP TABLE IF EXISTS bank_staging;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS transactions;
*/

/*
-- VIEW TABLES
SELECT * FROM bank_staging;
SELECT * FROM customer;
SELECT * FROM account;
SELECT * FROM transactions;
*/
