import json
from datetime import datetime
import sys
import time
import pyodbc

def create_json_file(file_name, isprint):
    """
    Reads or prints the content of a JSON file.
    """
    with open(file_name, 'a+') as f:
        f.seek(0)
        content = f.read()
    if isprint:
        return content
    if content:
        return json.loads(content)
    else:
        return {}

def data_collection(data, isvalid, error):
    """
    Collects user input and validates it based on the provided validation function.
    """
    while True:
        user_input = input(data)
        if isvalid(user_input):
            return user_input
        else:
            print(error)

def userID_isvalid(id, existingID):
    """
    Validates the user ID ensuring it is alphanumeric and unique.
    """
    if id.isalnum():
        if id not in existingID:
            return True
        else:
            print("ID already exists, please use a UNIQUE ID.")
            return False
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
    
    try:
        cursor.execute(insert_query, (user_id, first_name, last_name, age, gender, year_of_birth))
        connection.commit()
        print(f"Record for {user_id} inserted successfully.")
    except pyodbc.IntegrityError:
        if auto_confirm or isyes(f"{user_id} already exists. Do you want to update the record? (Y/N): "):
            cursor.execute(update_query, (first_name, last_name, age, gender, year_of_birth, user_id))
            connection.commit()
            print(f"Record for {user_id} updated successfully.")
        else:
            print(f"Record for {user_id} was not updated.")
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def collect_user_data(existingID):
    """
    Collects user data through input prompts and returns it as a dictionary.
    """
    inputs = [
        {"data": "Enter your UserID : ", "isvalid": lambda id: userID_isvalid(id, existingID), "error": ""},
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

    return {user_id: user_inputs}

def handle_user_data(file_path, user_ids):
    """
    Updates the JSON file with new user data and handles SQL operations.
    """
    dict_data = create_json_file(file_path, False)
    merged_dict = dict_data | user_ids

    with open(file_path, 'w') as file:
        json.dump(merged_dict, file, indent=4)

    user_id = list(user_ids.keys())[0]  # Get the single user ID
    user_data = user_ids[user_id]
    
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
        program_term = input("Type Y to enter new data, Q to retrieve stored data, F to search for a user, P to insert all data into SQL Server, N to exit the program: ").upper()
        match program_term:
            case 'Y':
                print("You may enter more data.")
                main()
            case 'Q':
                print("Displaying File content...")
                content = create_json_file(file_path, True)
                print(content)
            case 'F':
                search_userID = input("Type the UserID to search for: ")
                print("Searching for UserID...")
                if search_userID in merged_dict.keys():
                    print("User Found!")
                    print(merged_dict[search_userID])  # Display user data
                else:
                    print("User not found!")
            case 'P':
                autoconfirm = None
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
                        except KeyError as e:
                            print(f"KeyError: {e} for user_id: {user_id}")
                        
                        if autoconfirm != 'all':
                            autoconfirm = isyes(f"Do you want to continue inserting the next record? (Y/N/All): ", True)
            case 'N':
                print("All data has been saved properly, exiting...")
                time.sleep(3)
                sys.exit()

def main():
    """
    Main function to orchestrate data collection, handling, and user interaction.
    """
    file_path = 'user_data.txt'
    dict_data = create_json_file(file_path, False)
    existingID = dict_data.keys()
    user_ids = collect_user_data(existingID)
    handle_user_data(file_path, user_ids)
    merged_dict = create_json_file(file_path, False) | user_ids
    handle_user_interaction(file_path, merged_dict)

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
