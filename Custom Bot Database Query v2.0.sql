-- Check if the database exists
IF NOT EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = 'MY_CUSTOM_BOT')
BEGIN
    -- Create the database
    CREATE DATABASE MY_CUSTOM_BOT;
    PRINT 'Database MY_CUSTOM_BOT created successfully.';
END
GO

-- Use the database
USE MY_CUSTOM_BOT;
GO

-- Check if the SearchQueries table exists
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'SearchQueries')
BEGIN
    -- Create the SearchQueries table
    CREATE TABLE SearchQueries (
        QueryID INT PRIMARY KEY IDENTITY(1,1),
        OriginalQuery NVARCHAR(500),
        CleanedQuery NVARCHAR(500),
        Timestamp DATETIME DEFAULT GETDATE()
    )
    PRINT 'SearchQueries table created successfully.';
END
ELSE
BEGIN
    PRINT 'SearchQueries table already exists.';
END
GO

-- Check if the URLs table exists
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'URLs')
BEGIN
    -- Create the URLs table
    CREATE TABLE URLs (
        URLID INT PRIMARY KEY IDENTITY(1,1),
        QueryID INT,
        SearchEngine NVARCHAR(50),
        URL NVARCHAR(MAX),
        FOREIGN KEY (QueryID) REFERENCES SearchQueries(QueryID)
    )
    PRINT 'URLs table created successfully.';
END
ELSE
BEGIN
    PRINT 'URLs table already exists.';
END
GO

-- Check if the SearchTermFrequency table exists
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'SearchTermFrequency')
BEGIN
    -- Create the SearchTermFrequency table
    CREATE TABLE SearchTermFrequency (
        FrequencyID INT PRIMARY KEY IDENTITY(1,1),
        QueryID INT,
        URLID INT,
        SearchTerm NVARCHAR(50),
        Frequency INT,
        FOREIGN KEY (QueryID) REFERENCES SearchQueries(QueryID),
        FOREIGN KEY (URLID) REFERENCES URLs(URLID)
    )
    PRINT 'SearchTermFrequency table created successfully.';
END
ELSE
BEGIN
    PRINT 'SearchTermFrequency table already exists.';
END
GO


--select * from SearchQueries
--select * from URLs
--select * from SearchTermFrequency

--delete from SearchQueries
--delete from URLs
--delete from SearchTermFrequency
--DROP DATABASE MY_CUSTOM_BOT


--WITH RankedRows AS (
--    SELECT *,
--           ROW_NUMBER() OVER (PARTITION BY QueryID, URLID, SearchTerm ORDER BY Frequency DESC) AS RowNum
--    FROM SearchTermFrequency
--)
--DELETE FROM RankedRows
--WHERE RowNum > 1;


--WITH LastQueryID AS (
--    SELECT TOP 1 QueryID
--    FROM SearchQueries
--    ORDER BY QueryID DESC
--)
--SELECT URLs.URL, SUM(SearchTermFrequency.Frequency) AS TotalFrequency
--FROM SearchTermFrequency
--JOIN URLs ON SearchTermFrequency.URLID = URLs.URLID
--WHERE SearchTermFrequency.QueryID = (SELECT QueryID FROM LastQueryID)
--GROUP BY URLs.URL, SearchTermFrequency.URLID
--ORDER BY TotalFrequency DESC;
