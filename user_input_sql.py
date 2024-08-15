import json
import argparse
from datetime import datetime
import sys
import time
import pyodbc

def create_json_file(file_name, isprint):
    """
    Reads or prints the content of a JSON file.
    """
    try:
        with open(file_name, 'a+') as f:
            f.seek(0)
            content = f.read()
        if isprint:
            return content
        if content:
            return json.loads(content)
        else:
            return {}
    except Exception as e:
        print(f"Error reading or creating JSON file: {e}")
        sys.exit(1)

def log_to_sql(log_level, message, additional_info=None):
    """
    Logs a message to the SQL Server database.
    """
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=localhost\\SQLExpress;'
            'DATABASE=UserDatabase;'
            #'UID=your_username;'
            #'PWD=your_password'
        )
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO LogEntries (LogLevel, Message, AdditionalInfo)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_query, (log_level, message, additional_info))
        connection.commit()
    except pyodbc.Error as e:
        print(f"Error logging to SQL Server: {e}")
    finally:
        cursor.close()
        connection.close()

def data_collection(data, isvalid, error):
    """
    Collects user input and validates it based on the provided validation function.
    """
    while True:
        user_input = input(data)
        if isvalid(user_input):
            log_to_sql('INFO', f"User input '{user_input}' is valid.")
            print(f"Input '{user_input}' is valid.")
            return user_input
        else:
            log_to_sql('WARNING', f"Invalid input '{user_input}': {error}")
            print(f"Invalid input '{user_input}': {error}")

def userID_isvalid(id, existingID):
    """
    Validates the user ID ensuring it is alphanumeric and unique.
    """
    if id.isalnum():
        if id not in existingID:
            return True
        else:
            log_to_sql('WARNING', f"ID '{id}' already exists.")
            print("ID already exists, please use a UNIQUE ID.")
            return False
    log_to_sql('WARNING', f"Invalid ID '{id}': Only AlphaNumeric Characters are allowed.")
    print("Only AlphaNumeric Characters are allowed.")
    return False

def isyes(question, allow_all=False):
    """
    Prompts the user with a yes/no question, with an optional 'all' choice.
    """
    while True:
        answer = input(question).lower()
        if allow_all and answer in ['y', 'n', 'all']:
            if answer == 'all':
                return 'all'
            return True if answer == 'y' else False
        elif answer in ['y', 'n']:
            return True if answer == 'y' else False
        else:
            print("Please enter 'Y' for Yes, 'N' for No" + (" or 'All' for Yes to All." if allow_all else "."))

def sql_connection(user_id, first_name, last_name, age, gender, year_of_birth, auto_confirm=False):
    """
    Connects to SQL Server and inserts or updates user data.
    """
    try:
        connection = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=localhost\\SQLExpress;'
            'DATABASE=UserDatabase;'
            #'UID=your_username;'
            #'PWD=your_password'
        )
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO Users (user_id, first_name, last_name, age, gender, year_of_birth)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        update_query = """
        UPDATE Users
        SET first_name = ?, last_name = ?, age = ?, gender = ?, year_of_birth = ?
        WHERE user_id = ?
        """
        
        cursor.execute(insert_query, (user_id, first_name, last_name, age, gender, year_of_birth))
        connection.commit()
        log_to_sql('INFO', f"Record for {user_id} inserted successfully.")
        print(f"Record for {user_id} inserted successfully.")
    except pyodbc.IntegrityError:
        log_to_sql('WARNING', f"Record for {user_id} already exists.")
        print(f"Record for {user_id} already exists.")
        if auto_confirm or isyes(f"{user_id} already exists. Do you want to update the record? (Y/N): "):
            cursor.execute(update_query, (first_name, last_name, age, gender, year_of_birth, user_id))
            connection.commit()
            log_to_sql('INFO', f"Record for {user_id} updated successfully.")
            print(f"Record for {user_id} updated successfully.")
        else:
            log_to_sql('INFO', f"Record for {user_id} was not updated.")
            print(f"Record for {user_id} was not updated.")
    except pyodbc.Error as e:
        log_to_sql('ERROR', f"SQL Error: {e}")
        print(f"SQL Error: {e}")
    finally:
        cursor.close()
        connection.close()

def collect_user_data(existingID):
    """
    Collects user data through input prompts and returns it as a dictionary.
    """
    print("Collecting user data. Please provide the following information:")
    inputs = [
        {"data": "Enter your UserID : ", "isvalid": lambda id: userID_isvalid(id, existingID), "error": "Invalid UserID."},
        {"data": "Enter your First Name : ", "isvalid": lambda x: x.isalpha(), "error": "First Name must contain only alphabetic characters."},   
        {"data": "Enter your Last Name : ", "isvalid": lambda x: x.isalpha(), "error": "Last Name must contain only alphabetic characters."},  
        {"data": "Enter your age : ", "isvalid": lambda x: x.isdigit() and int(x) > 0, "error": "Age must be a positive integer."},  
        {"data": "Enter your gender : ", "isvalid": lambda x: x.lower() in ["male", "female"], "error": "Gender must be either 'male' or 'female'."},  
        {"data": "Enter your Year of Birth : ", "isvalid": lambda x: x.isdigit() and datetime.now().year - int(x) >= 18, "error": "You must be at least 18 years old. Please enter a valid year of birth."}
    ]

    user_inputs = {}
    user_id = None

    for index, input_data in enumerate(inputs):
        user_input = data_collection(input_data["data"], input_data["isvalid"], input_data["error"])
        key = input_data["data"].split()[2].replace(' ', '_').lower()  # Use consistent key names

        if index == 0:
            user_id = user_input
        user_inputs[key] = user_input

    print(f"Collected data: {user_inputs}")
    return {user_id: user_inputs}

def handle_user_data(file_path, user_ids):
    """
    Updates the JSON file with new user data and handles SQL operations.
    """
    print("Handling user data...")
    dict_data = create_json_file(file_path, False)
    merged_dict = dict_data | user_ids

    with open(file_path, 'w') as file:
        json.dump(merged_dict, file, indent=4)
    print(f"Data saved to {file_path}.")

    user_id = list(user_ids.keys())[0]  # Get the single user ID
    user_data = user_ids[user_id]
    
    # No decryption needed for SQL insertion/update
    sql_connection(
        user_id, 
        user_data.get('first_name', 'Unknown'), 
        user_data.get('last_name', 'Unknown'), 
        user_data.get('age', '0'), 
        user_data.get('gender', 'Unknown'), 
        user_data.get('year_of_birth', '1900')
    )

def handle_user_interaction(file_path, merged_dict):
    """
    Manages user interaction for various actions such as viewing, searching, and inserting data.
    """
    while True:
        print("\nChoose an option:")
        print("Y - Enter new data")
        print("Q - Retrieve stored data")
        print("F - Search for a user")
        print("P - Insert all data into SQL Server")
        print("N - Exit the program")

        program_term = input("Your choice: ").upper()
        match program_term:
            case 'Y':
                print("You chose to enter new data.")
                log_to_sql('INFO', "User chose to enter new data.")
                new_user_data = collect_user_data(merged_dict.keys())
                handle_user_data(file_path, new_user_data)
                # Update merged_dict with new data
                merged_dict.update(new_user_data)
                print("New data has been collected and saved.")
            case 'Q':
                print("You chose to retrieve stored data.")
                log_to_sql('INFO', "User chose to retrieve stored data.")
                print("Displaying File content...")
                content = create_json_file(file_path, True)
                print(content)
            case 'F':
                print("You chose to search for a user.")
                log_to_sql('INFO', "User chose to search for a user.")
                search_userID = input("Enter the UserID to search for: ")
                print("Searching for UserID...")
                if search_userID in merged_dict:
                    print("User found!")
                    print(merged_dict[search_userID])  # Display user data
                else:
                    print("User not found!")
            case 'P':
                autoconfirm = None
                print("You chose to insert all data into SQL Server.")
                log_to_sql('INFO', "User chose to insert all data into SQL Server.")
                print("Inserting all data into SQL Server...")
                for user_id, user_data in merged_dict.items():
                    if autoconfirm is None:
                        autoconfirm = isyes(f"Insert {user_id} into SQL Server? (Y/N/All): ", True)
                    if autoconfirm == 'all' or autoconfirm:
                        try:
                            sql_connection(
                                user_id, 
                                user_data.get('first_name', 'Unknown'), 
                                user_data.get('last_name', 'Unknown'), 
                                user_data.get('age', '0'), 
                                user_data.get('gender', 'Unknown'), 
                                user_data.get('year_of_birth', '1900'),
                                auto_confirm=(autoconfirm == 'all')
                            )
                            print(f"Data for {user_id} inserted successfully.")
                        except Exception as e:
                            log_to_sql('ERROR', f"Error during data insertion: {e}", additional_info=str(e))
                            print(f"Error inserting data for {user_id}.")
                        
                        if autoconfirm != 'all':
                            autoconfirm = isyes(f"Do you want to continue inserting the next record? (Y/N/All): ", True)
            case 'N':
                print("Exiting program.")
                log_to_sql('INFO', "Exiting program.")
                print("All data has been saved properly. Exiting...")
                time.sleep(3)
                sys.exit()
            case _:
                print("Invalid choice. Please enter a valid option.")
                log_to_sql('WARNING', "Invalid input.")

def main():
    """
    Main function to handle user interactions and manage data.
    """
    parser = argparse.ArgumentParser(description="User Data Management System")
    parser.add_argument('--file', type=str, required=True, help="Path to the JSON file for user data")
    args = parser.parse_args()

    file_path = args.file
    print(f"Initializing with file: {file_path}")

    # Load existing data from JSON file
    merged_dict = create_json_file(file_path, False)
    print(f"Existing data loaded from {file_path}")

    # Handle user interaction
    handle_user_interaction(file_path, merged_dict)

if __name__ == "__main__":
    main()
