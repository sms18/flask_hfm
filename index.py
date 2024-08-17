import pandas as pd
import sqlite3

def clean_column_names(df):
    """
    Clean DataFrame column names to ensure they are valid SQL identifiers.
    """
    df.columns = [str(col) for col in df.columns]  # Ensure all column names are strings
    df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores
    df.columns = df.columns.str.replace(r'\W', '', regex=True)  # Remove non-alphanumeric characters
    return df

# Custom function to print the SQL create statement for debugging
def get_sql_create_statement(df, table_name):
    temp_conn = sqlite3.connect(':memory:')
    df.to_sql(table_name, temp_conn, if_exists='replace', index=False)
    cursor = temp_conn.cursor()
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    create_statement = cursor.fetchone()[0]
    temp_conn.close()
    return create_statement

# Step 1: Read the Excel file
excel_file = r'C:\Users\SMS\Desktop\read\name.xlsx'  # Use raw string for Windows path
df = pd.read_excel(excel_file, sheet_name=None)  # Read all sheets into a dictionary of DataFrames

# Step 2: Create an SQLite database and a connection to it
sqlite_file = r'C:\Users\SMS\Desktop\read\database.sqlite'  # Specify the path for the SQLite file
conn = sqlite3.connect(sqlite_file)

# Step 3: Write the data to the SQLite database
for sheet_name, data in df.items():
    # Clean column names
    data = clean_column_names(data)
    
    # Save DataFrame to CSV to check data integrity
    data.to_csv(f'C:\\Users\\SMS\\Desktop\\read\\{sheet_name}.csv', index=False, encoding='utf-8-sig')
    print(f'Sheet "{sheet_name}" written to CSV.')

    # Print SQL create statement for debugging
    create_statement = get_sql_create_statement(data, sheet_name)
    print(f"Create statement for table '{sheet_name}':")
    print(create_statement)
    
    # Write DataFrame to SQLite
    data.to_sql(sheet_name, conn, if_exists='replace', index=False)

# Close the connection
conn.close()
print('Data imported to SQLite database successfully.')
