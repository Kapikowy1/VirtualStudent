from docx import Document
from language_model_introduction import name_docx, topic
from List import assistant_response_list
import function


system_settings = "Be an experienced creator of academic content, assisting in creating and editing a lengthy text for the given point of an engineering project. Carefully select words and structures to engage the reader right from the first sentences. Focus on presenting the essence of the topic and providing context. It's worth noting that the text will be written in a language that is challenging to detect by AI detectors. The text should be comprehensive enough to immerse the reader in the context, yet concise enough to maintain their attention. The text should be a minimum of 500 words. An essential aspect of scholarly work is utilizing credible sources. Use scientific terminology and statements. Don't include the purpose of the work in the generated text. Provide the answer in Polish"

""" Processing data from the list """


# Podział tekstu na linie
lines = assistant_response_list.split('\n')

# Usunięcie sekcji "Literatura", "Streszczenie", "Podsumowanie i wnioski", "Wstęp" i "Spis treści" ze zmiennej lines
filtered_lines = [line for line in lines if not any(
    section in line.lower() for section in ["literatura", "streszczenie", "podsumowanie i wnioski", "podsumowanie oraz wnioski", "wstęp", "spis treści", "podziękowania", "wprowadzenie"])]

correct_format = list(filter(lambda x: x.strip(), filtered_lines))

list_of_contents = function.correct_formatting(correct_format)

# Podział na sekcje
contents_dict = {}

current_main_point = None

for item in list_of_contents:
    item = item.strip()
    if item[0].isdigit() and '.' in item:
        if item.count('.') == 1:  # Główny punkt
            current_main_point = item
            contents_dict[current_main_point] = []
        else:  # Podpunkt
            if current_main_point:  # Sprawdźmy, czy mamy aktualny główny punkt
                contents_dict[current_main_point].append(item)


""" Generating a response for a point """

# Otwarcie istniejącego dokumentu
doc = Document(name_docx)

for main_point, sub_points in contents_dict.items():
    points = [main_point]  # Rozpoczynamy listę punktów od głównego punktu

    if sub_points:
        points.extend(sub_points)  # Dodajemy podpunkty do listy punktów

    for point in points:
        assistant_response = function.get_GPT_request_point(
            point, topic, system_settings)

        # Wybór poziomu nagłówka
        doc.add_heading(point, level=1 if point == main_point else 2)

        # Czyszczenie danych
        assistant_response = function.clean_text(assistant_response)

        # Podział tekstu na akapity i wyrazy
        paragraphs = assistant_response.split('\n\n')

        # Iteracja przez akapity i dodanie ich bezpośrednio do dokumentu
        for paragraph in paragraphs[1:]:
            doc.add_paragraph(paragraph)

        # Dodanie przejścia na nową stronę
        doc.add_page_break()

# Zapisywanie zmian w dokumencie
doc.save(name_docx)
