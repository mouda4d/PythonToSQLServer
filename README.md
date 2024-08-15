
# **User Data Management System Documentation**

---

## **Usage Instructions**

To effectively use the User Data Management System, follow these detailed instructions:

### **Setup**

1. **Ensure Prerequisites**:
   - Install Python on your system.
   - Ensure required Python libraries are installed. You can use `pip` to install missing libraries:
     ```sh
     pip install pyodbc
     ```

2. **Configure SQL Server**:
   - Ensure that SQL Server is installed and running.
   - Update the connection parameters in the script to match your SQL Server configuration. This includes the `SERVER`, `DATABASE`, and optionally `UID` and `PWD` if authentication is required.

### **Running the Application**

1. **Start the Application**:
   - Run the Python script from the command line, providing the path to your JSON file:
     ```sh
     python script_name.py --file path_to_json_file
     ```
   - Replace `script_name.py` with the name of your Python script.
   - Replace `path_to_json_file` with the path to the JSON file used for storing user data.

2. **Follow On-Screen Prompts**:
   - The application will present a menu with various options. Choose the option that best suits your needs:
     - **Enter New Data**: Select 'Y' to add new user data.
     - **Retrieve Stored Data**: Select 'Q' to view the contents of the JSON file.
     - **Search for a User**: Select 'F' to search for a user by UserID.
     - **Insert All Data into SQL Server**: Select 'P' to upload all user data from the JSON file to SQL Server.
     - **Exit the Program**: Select 'N' to terminate the application.

---

## **Functions**

### **`create_json_file(file_name, isprint)`**

- **Purpose**: Handles the creation or reading of a JSON file to either print its content or return it as a dictionary.
- **Parameters**:
  - `file_name`: Specifies the path to the JSON file.
  - `isprint`: Boolean flag to determine if the content should be printed or returned as a dictionary.
- **Returns**: 
  - If `isprint` is `True`, returns the file content as a string.
  - If `isprint` is `False`, returns the file content parsed as a JSON dictionary.
- **Error Handling**: 
  - Catches and reports errors related to file reading and writing.
  - Logs the error and exits the application if an exception is encountered.

### **`log_to_sql(log_level, message, additional_info=None)`**

- **Purpose**: Logs events and messages to a SQL Server database for tracking and auditing purposes.
- **Parameters**:
  - `log_level`: The severity level of the log (e.g., INFO, WARNING, ERROR).
  - `message`: Main content of the log message.
  - `additional_info`: Optional parameter for additional context or details.
- **Error Handling**:
  - Handles SQL Server connection issues and logs any errors encountered during the logging process.

### **`data_collection(data, isvalid, error)`**

- **Purpose**: Collects user input through prompts and validates it based on a provided validation function.
- **Parameters**:
  - `data`: The prompt message presented to the user.
  - `isvalid`: A function used to validate the user input.
  - `error`: The error message to display if the input is invalid.
- **Returns**: The validated user input.
- **Error Handling**:
  - Prompts the user again if the input is invalid.
  - Logs and reports any issues related to input validation.

### **`userID_isvalid(id, existingID)`**

- **Purpose**: Validates a user ID to ensure it is both alphanumeric and unique within a set of existing IDs.
- **Parameters**:
  - `id`: The user ID to be validated.
  - `existingID`: A list of existing user IDs to check for uniqueness.
- **Returns**: 
  - `True` if the ID is valid and unique.
  - `False` otherwise.
- **Error Handling**:
  - Logs warnings if the ID is invalid or a duplicate, and notifies the user.

### **`isyes(question, allow_all=False)`**

- **Purpose**: Prompts the user with a yes/no question, with an optional 'all' choice to apply the action to all items.
- **Parameters**:
  - `question`: The question to be asked.
  - `allow_all`: Boolean to indicate if 'all' is a valid response.
- **Returns**: 
  - `True` if the user answers 'y'.
  - `False` if the user answers 'n'.
  - `'all'` if 'all' is allowed and chosen.
- **Error Handling**:
  - Handles invalid responses and prompts the user until a valid input is received.

### **`sql_connection(user_id, first_name, last_name, age, gender, year_of_birth, auto_confirm=False)`**

- **Purpose**: Connects to SQL Server to insert or update user data in the database.
- **Parameters**:
  - `user_id`: Unique identifier for the user.
  - `first_name`: User’s first name.
  - `last_name`: User’s last name.
  - `age`: User’s age.
  - `gender`: User’s gender.
  - `year_of_birth`: User’s year of birth.
  - `auto_confirm`: Boolean indicating if confirmation for updates should be automatic.
- **Error Handling**:
  - Catches and logs SQL errors.
  - Handles conflicts with existing records, providing options for automatic or manual confirmation for updates.

### **`collect_user_data(existingID)`**

- **Purpose**: Gathers and validates user data through a series of input prompts.
- **Parameters**:
  - `existingID`: A list of existing user IDs to ensure uniqueness.
- **Returns**: A dictionary where the key is the user ID and the value is another dictionary with the user’s details.
- **Error Handling**:
  - Utilizes the `data_collection` function to validate each piece of user input.
  - Logs and reports validation errors.

### **`handle_user_data(file_path, user_ids)`**

- **Purpose**: Updates the JSON file with new user data and performs SQL operations to insert or update records.
- **Parameters**:
  - `file_path`: Path to the JSON file where data will be stored.
  - `user_ids`: Dictionary of new user data to be added.
- **Error Handling**:
  - Updates the JSON file and handles SQL operations, logging success or failure of these actions.

### **`handle_user_interaction(file_path, merged_dict)`**

- **Purpose**: Manages user interactions for various actions such as entering new data, retrieving stored data, searching, and inserting data into SQL Server.
- **Parameters**:
  - `file_path`: Path to the JSON file.
  - `merged_dict`: Dictionary of existing data loaded from the JSON file.
- **Error Handling**:
  - Logs user choices and interactions.
  - Handles different user options including data entry, retrieval, searching, and SQL insertion.

### **`main()`**

- **Purpose**: Initializes the application and manages user interaction based on command-line arguments.
- **Parameters**: None.
- **Error Handling**:
  - Loads existing data from the JSON file.
  - Handles user input and manages the flow of the application.

---

## **Troubleshooting**

- **File Not Found**: 
  - Ensure the file path provided is correct and the file exists.
  - Check file permissions to ensure it is readable and writable.

- **SQL Connection Issues**: 
  - Verify SQL Server is running and accessible.
  - Confirm connection parameters are correct (e.g., server name, database name).

- **Invalid Input**: 
  - Follow prompts carefully and ensure input matches the expected format.
  - Refer to error messages for guidance on correcting input.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
