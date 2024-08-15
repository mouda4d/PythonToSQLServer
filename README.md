
# **User Data Management System Documentation**

---

## **Usage Instructions**

To use the User Data Management System, follow these steps:

1. **Setup**: Ensure you have Python and the required libraries (`pyodbc`, `json`, `argparse`) installed. You may need to configure your SQL Server connection parameters in the script.

2. **Run the Application**:
   ```sh
   python script_name.py --file path_to_json_file
   ```
   - Replace `script_name.py` with the name of your Python script.
   - Replace `path_to_json_file` with the path to the JSON file used for storing user data.

3. **Interact with the Application**:
   - **Enter New Data**: Choose 'Y' to enter new user data. Follow the prompts to provide user details.
   - **Retrieve Stored Data**: Choose 'Q' to view the contents of the JSON file.
   - **Search for a User**: Choose 'F' to search for a user by their UserID.
   - **Insert All Data into SQL Server**: Choose 'P' to insert all data from the JSON file into the SQL Server database.
   - **Exit the Program**: Choose 'N' to exit the application.

4. **Follow Prompts**: The application will guide you through various options and requests for user input. Make selections based on your needs.

---

## **Functions**

### **`create_json_file(file_name, isprint)`**

- **Purpose**: Reads or prints the content of a JSON file.
- **Parameters**:
  - `file_name`: Path to the JSON file.
  - `isprint`: Boolean indicating whether to print the content or return it as a dictionary.
- **Returns**: JSON content as a string or dictionary.
- **Error Handling**: Logs and exits on file operation errors.

### **`log_to_sql(log_level, message, additional_info=None)`**

- **Purpose**: Logs messages to a SQL Server database.
- **Parameters**:
  - `log_level`: Severity level (e.g., INFO, WARNING, ERROR).
  - `message`: Main content of the log entry.
  - `additional_info`: Optional additional context.
- **Error Handling**: Handles SQL Server connection errors.

### **`data_collection(data, isvalid, error)`**

- **Purpose**: Collects and validates user input.
- **Parameters**:
  - `data`: Prompt message.
  - `isvalid`: Validation function.
  - `error`: Error message if validation fails.
- **Returns**: Validated user input.
- **Error Handling**: Re-prompts and logs invalid input.

### **`userID_isvalid(id, existingID)`**

- **Purpose**: Validates the user ID to be alphanumeric and unique.
- **Parameters**:
  - `id`: User ID to validate.
  - `existingID`: List of existing IDs.
- **Returns**: Boolean indicating validity.
- **Error Handling**: Logs warnings for invalid or duplicate IDs.

### **`isyes(question, allow_all=False)`**

- **Purpose**: Prompts the user with a yes/no question, with an optional 'all' choice.
- **Parameters**:
  - `question`: The question to ask.
  - `allow_all`: Boolean for allowing 'all' as a response.
- **Returns**: Boolean or 'all' based on input.
- **Error Handling**: Handles invalid responses.

### **`sql_connection(user_id, first_name, last_name, age, gender, year_of_birth, auto_confirm=False)`**

- **Purpose**: Connects to SQL Server to insert or update user data.
- **Parameters**:
  - `user_id`: User ID.
  - `first_name`: User's first name.
  - `last_name`: User's last name.
  - `age`: User's age.
  - `gender`: User's gender.
  - `year_of_birth`: User's year of birth.
  - `auto_confirm`: Boolean for automatic update confirmation.
- **Error Handling**: Handles SQL errors and conflicts with existing records.

### **`collect_user_data(existingID)`**

- **Purpose**: Collects and validates user data through input prompts.
- **Parameters**:
  - `existingID`: List of existing IDs for validation.
- **Returns**: Dictionary with collected user data.
- **Error Handling**: Validates input using `data_collection` and logs issues.

### **`handle_user_data(file_path, user_ids)`**

- **Purpose**: Updates the JSON file with new user data and performs SQL operations.
- **Parameters**:
  - `file_path`: Path to the JSON file.
  - `user_ids`: Dictionary of new user data.
- **Error Handling**: Updates the JSON file and performs SQL operations, logging success or failure.

### **`handle_user_interaction(file_path, merged_dict)`**

- **Purpose**: Manages user interaction for data management operations.
- **Parameters**:
  - `file_path`: Path to the JSON file.
  - `merged_dict`: Dictionary of existing data.
- **Error Handling**: Logs user choices and handles different options such as data entry, retrieval, searching, and SQL insertion.

### **`main()`**

- **Purpose**: Main function to handle user interactions and manage data.
- **Parameters**: None.
- **Error Handling**: Initializes the application and handles user input.

---

## **Troubleshooting**

- **File Not Found**: Ensure the file path is correct and the file exists.
- **SQL Connection Issues**: Check SQL Server configuration and connection parameters.
- **Invalid Input**: Follow prompts and ensure input adheres to specified formats.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
