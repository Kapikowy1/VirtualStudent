import os
from function import fix_polish_characters
from decouple import config


prod_path = config("PROD_PATH")
dev_path = config('DEV_PATH')

def read_data_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Your folder directories
main_folder = 'main'
folder_scend = 'DocumentAi'
folder_name_model = 'python_language_model'
MVP = 'MVP'

output_file_path = os.path.join(
    folder_name_model, MVP, 'output.txt')

production_path = f'{prod_path}output.txt'
final_dev_path= f'{dev_path}output.txt'

data = read_data_from_file(final_dev_path)


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


result = process_data(data)

for item in result:
    purpose = fix_polish_characters(result[0])
    topic = fix_polish_characters(result[1])