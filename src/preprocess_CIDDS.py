import pandas as pd

def preprocess_data(input_file, output_file):
    # Read the CSV file
    data = pd.read_csv(input_file)

    # Convert the 'Date first seen' column to datetime format
    data['Date first seen'] = pd.to_datetime(data['Date first seen'])

    # Extract day, year, and month from the 'Date first seen' column
    data['Day'] = data['Date first seen'].dt.day
    data['Year'] = data['Date first seen'].dt.year
    data['Month'] = data['Date first seen'].dt.month

    # Drop the specified columns
    columns_to_drop = ['attackType', 'attackID', 'attackDescription']
    data = data.drop(columns=columns_to_drop)

    # Save the preprocessed data to a new CSV file
    data.to_csv(output_file, index=False)

# Example usage
input_file = "data//user_data//CIDDS-001.csv"
output_file = "data//preprocessed//preprocessed_data.csv"
preprocess_data(input_file, output_file)


