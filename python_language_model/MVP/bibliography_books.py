from docx import Document
from bibliography import name_docx, topic, filtered_lines
from function import get_GPT_request_point


system_settings = "You are a qualified bookseller and your task is to select three books or publications in scientific journals that perfectly match the informational needs regarding the point related to the topic of the work. Provide only from the hyphens the author or authors, title, publisher, place of publication, publication date. Example: '- Jakubczyk T., Klette A.: Measurements in acoustics. WNT, Warsaw 1997.'"

# Otwarcie istniejącego dokumentu
doc = Document(name_docx)

paragraphs = []
titles_set = set()  # Zbiór przechowujący unikalne tytuły

for point in filtered_lines:
    assistant_response_books = get_GPT_request_point(
        point, topic, system_settings)
    assistant_response_books = assistant_response_books.replace('\n\n', '\n')

    # Podział tekstu na akapity
    point_paragraphs = assistant_response_books.split('\n')

    # Strip each paragraph and add to the list
    for paragraph in point_paragraphs:
        title_start_index = paragraph.find(':')  # Find the index of the colon
        # Find the index of the period after the colon
        title_end_index = paragraph.find('.', title_start_index)
        if title_start_index != -1 and title_end_index != -1:  # Check if both colon and period are found
            title = paragraph[title_start_index +
                              1: title_end_index + 1]  # Extract the title
            if title not in titles_set:  # Check if the title is not in the set
                titles_set.add(title)  # Add the title to the set
                # Append the paragraph to the list
                paragraphs.append(paragraph.strip())

# Dodawanie akapitów bez wcięć na początku
for paragraph in paragraphs:
    doc.add_paragraph(paragraph)


# Przesunięcie na nową stronę po każdej sekcji
doc.add_page_break()

# Zapisz zaktualizowany dokument DOCX
doc.save(name_docx)
