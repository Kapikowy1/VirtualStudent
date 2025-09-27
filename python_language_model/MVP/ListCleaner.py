from List import list_of_contents


data_of_links = list_of_contents.copy()

# Słowa do usunięcia
words_to_remove = ['Wprowadzenie', 'Podsumowanie i wnioski',
                   'Streszczenie', 'Bibliografia']

# Usuń pierwszy element z listy
data_of_links = data_of_links[1:]

# Oczyść listę z liczb, kropkami, spacjami i znakami '*'
cleaned_data = [element.strip(' \t*1234567890.').replace('- ', '').replace(',', '')
                for element in data_of_links if element.strip()]

# Usuń określone słowa
cleaned_data = [
    element for element in cleaned_data if element not in words_to_remove]

words_to_remove2 = ['Wstęp']

cleaned_data2 = [
    element for element in cleaned_data if element not in words_to_remove2]
