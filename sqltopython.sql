-- Create the database if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'UserDatabase')
BEGIN
    CREATE DATABASE UserDatabase;
END
GO

USE UserDatabase;
GO

-- Create the Users table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        user_id NVARCHAR(50) PRIMARY KEY,
        first_name NVARCHAR(100),
        last_name NVARCHAR(100),
        age NVARCHAR(10),
        gender NVARCHAR(10),
        year_of_birth NVARCHAR(10)
    );
END
GO

-- Create the LogEntries table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'LogEntries')
BEGIN
    CREATE TABLE LogEntries (
        id INT IDENTITY(1,1) PRIMARY KEY,
        LogLevel NVARCHAR(50),
        Message NVARCHAR(MAX),
        AdditionalInfo NVARCHAR(MAX),
        Timestamp DATETIME DEFAULT GETDATE()
    );
END
GO
select * from Users;
select * from LogEntries;