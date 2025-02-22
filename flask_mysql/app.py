import mysql.connector
from mysql.connector import Error

def connect_to_database():
    try:
        # Try connecting to the database
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="19030ee235",  # Replace with your actual password
            database="school"  # Replace with your database name
        )
        
        # If connection is successful, print success message
        if connection.is_connected():
            print("Connection to MySQL database is successful")
            return connection  # Return the connection object to use later

    except Error as e:
        # If there is an error, print the error message
        print(f"Error: {e}")
        return None

# Example of calling the function and using the connection
if __name__ == "__main__":
    connection = connect_to_database()
    if connection:
        # Do something with the connection (like querying the database)
        # Don't forget to close the connection after you're done
        connection.close()
    else:
        print("Failed to connect to the database.")
