
# User Data Management System

## Overview

This application is a user data management system that interacts with a SQL Server database and a JSON file. It allows you to collect, view, search, and insert user data into a SQL Server database. The application logs interactions and errors to the SQL Server database for tracking purposes.

## Features

- **Collect User Data**: Collects and validates user data including UserID, First Name, Last Name, Age, Gender, and Year of Birth.
- **Retrieve Stored Data**: Displays the content of the JSON file where user data is stored.
- **Search for a User**: Allows searching for a user by UserID.
- **Insert Data into SQL Server**: Inserts or updates user data into the SQL Server database.
- **Logging**: Logs interactions and errors to SQL Server for auditing and troubleshooting.

## Requirements

- Python 3.x
- `pyodbc` library for SQL Server connectivity
- A SQL Server instance (e.g., SQL Server Express)
- JSON file to store user data

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/user-data-management-system.git
    cd user-data-management-system
    ```

2. **Install dependencies:**

    You can use `pip` to install the required packages:

    ```bash
    pip install pyodbc
    ```

    Ensure that you have the SQL Server ODBC driver installed on your system. For SQL Server Express, you might need to install it from [Microsoft's website](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

## Usage

1. **Prepare the SQL Server Database:**

   Ensure you have a SQL Server instance running and a database named `UserDatabase`. Create the required tables with the following structure:

    ```sql
    CREATE TABLE LogEntries (
        LogID INT PRIMARY KEY IDENTITY,
        LogLevel VARCHAR(10),
        Message VARCHAR(255),
        AdditionalInfo TEXT,
        LogDate DATETIME DEFAULT GETDATE()
    );

    CREATE TABLE Users (
        user_id VARCHAR(50) PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        age INT,
        gender VARCHAR(10),
        year_of_birth INT
    );
    ```

2. **Run the Application:**

   To start the application, use the following command:

    ```bash
    python script_name.py --file path_to_your_json_file
    ```

   Replace `script_name.py` with the name of your Python script and `path_to_your_json_file` with the path to the JSON file where user data will be stored.

3. **Interact with the Application:**

   After running the application, you'll be presented with a menu with the following options:

   - **Y** - Enter new data: Collect and save new user data.
   - **Q** - Retrieve stored data: Display the content of the JSON file.
   - **F** - Search for a user: Search for a user by UserID.
   - **P** - Insert all data into SQL Server: Insert or update all data from the JSON file into the SQL Server database.
   - **N** - Exit the program: Exit the application.

   Follow the on-screen prompts to interact with the application.

## Logging

The application logs various actions and errors to the `LogEntries` table in the SQL Server database. Check this table for detailed logs of user interactions and any issues encountered.

## Troubleshooting

- **SQL Server Connection Issues**: Ensure your SQL Server instance is running and accessible. Verify connection details in the `log_to_sql` function.
- **Missing Dependencies**: Make sure all required Python packages are installed.

## Contributing

Feel free to fork the repository and submit pull requests with improvements or bug fixes. Please ensure that your code follows the existing style and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
