import os
from function import fix_polish_characters
from decouple import config

prod_path = config("PROD_FULL_VERSION_PATH")
dev_path = config('DEV_FULL_VERSION_PATH')

def read_data_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



output_file_path = os.path.join('python_language_model','fullVersion','output.txt')
print(output_file_path)
# Function call


production_path = f'{prod_path}output.txt'
final_dev_path= f'{dev_path}output.txt'


data=''
if os.path.exists(production_path):
    print(f'Plik istnieje: {production_path}')
    data = read_data_from_file(production_path)
else:
    print(f'Plik nie istnieje: {production_path}')



def process_data(data):

    # Podziel dane na linie
    lines = data.split('\n')

    result = []

    # Iteruj przez każdą linię
    for line in lines:
        # Podziel linię na części po ":"
        parts = line.split(': ')
        if len(parts) == 2:
            value = parts[1]
            result.append(value)

    return result

if data :
    result = process_data(data)
    for item in result:
        purpose = fix_polish_characters(result[0])
        topic = fix_polish_characters(result[1])

