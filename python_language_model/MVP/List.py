""" Spis treści """

from function import get_data_GPT
from docx import Document
from file_processing import purpose, topic


system_settings = "I have significant experience in creating scientific content, assisting in the creation of an excellent table of contents for engineering projects. It's worth noting that the table of contents will be written in a language that is difficult to detect by artificial intelligence detectors. The layout of the table of contents should be modeled after the following structure: Table of Contents:\n 1. Introduction\n 2. Appropriate Title for Theoretical Chapter\n    2.1 Appropriate Subsection Titles\n    2.2 Appropriate Subsection Titles\n    2.3 Appropriate Subsection Titles\n 3. Appropriate Title for Practical Section\n    3.1 Appropriate Subsection Titles\n    3.2 Appropriate Subsection Titles\n    3.3 Appropriate Subsection Titles\n 4. Summary and Conclusions\n 5. Literature\n 6. Abstract. Follow the numbering from the example closely. Apply scientific terminology and expression style. Please provide the response in Polish. Do not add double \n in the response"


assistant_response_list = get_data_GPT(
    purpose, topic, system_settings, model="gpt-4", temperature=0.25)


# Podział na sekcje
list_of_contents = assistant_response_list.split('\n')

# Tworzenie nowego dokumentu docx
doc = Document()

# Dodawanie spisu treści
doc.add_heading('Spis treści', level=1)

for section in list_of_contents[1:]:
    if section.strip():  # Pomijanie pustych linii

        # Dodawanie punktu listy
        doc.add_paragraph(section)

# Przesunięcie na nową stronę po każdej sekcji
doc.add_page_break()

# Zapisywanie dokumentu do pliku
name_docx = f'{topic}.docx'
doc.save(name_docx)
