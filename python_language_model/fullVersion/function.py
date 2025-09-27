import re
from docx import Document
from decouple import config
from openai import OpenAI
# from translate import Translator

client = OpenAI(api_key=config("OPENAI_API_KEY"))


# Function Open AI
def get_data_GPT(purpose, topic, system_settings, model="gpt-4-0613", temperature=0.2, max_tokens=4096, top_p=1, frequency_penalty=1.5, presence_penalty=1):

    response = client.chat.completions.create(

        model=model,
        messages=[

            {

                "role": "system",

                "content": system_settings

            },

            {

                "role": "user",

                "content": f"Temat pracy: {topic}. Cel pracy: {purpose}"

            }

        ],

        temperature=temperature,

        max_tokens=max_tokens,

        top_p=top_p,

        frequency_penalty=frequency_penalty,

        presence_penalty=presence_penalty

    )

    return response.choices[0].message.content


# Function for docx-y
def get_docx(name_docx, heading, assistant_response):

    # Otwarcie istniejącego dokumentu
    doc = Document(name_docx)

    doc.add_heading(heading, level=1)

    # Podział tekstu na akapity
    paragraphs = assistant_response.split('\n\n')

    # Dodawanie akapitów bez wcięć na początku
    for paragraph in paragraphs[1:]:
        doc.add_paragraph(paragraph)

    # Dodanie przejścia na nową stronę
    doc.add_page_break()

    # Zapisywanie zmian w dokumencie
    doc.save(name_docx)


# Function Open AI by bibliography
def get_GPT_request_point(point, topic, system_settings, model="gpt-3.5-turbo-16k", temperature=0.25, max_tokens=4096, top_p=1, frequency_penalty=1.5, presence_penalty=1):

    response = client.chat.completions.create(

        model=model,
        messages=[

            {

                "role": "system",

                "content": system_settings

            },

            {

                "role": "user",

                "content": f"Nazwa punktu: {point} i temat pracy: {topic}"

            }

        ],

        temperature=temperature,

        max_tokens=max_tokens,

        top_p=top_p,

        frequency_penalty=frequency_penalty,

        presence_penalty=presence_penalty

    )

    return response.choices[0].message.content




def fix_polish_characters(text):
    text = text.replace("Ä™", "ę")
    text = text.replace("ĹĽ", "ż")
    text = text.replace("Ăł", "ó")
    text = text.replace("Ĺ›", "ś")
    text = text.replace("Ĺ‚", "ł")
    text = text.replace("Ä‡", "ć")
    text = text.replace("Ĺ„", "ń")

    return text


def clean_text(text):
    # Usuwanie znaków "**"
    cleaned_text = text.replace('**', '')

    # Usuwanie znaków "###"
    cleaned_text = cleaned_text.replace('###', '')

    # Usuwanie znaków "#"
    cleaned_text = cleaned_text.replace('#', '')

    return cleaned_text


def correct_formatting(input_list):
    # Generujemy liczby w różnych formatach
    generated_numbers = {}
    for i in range(1, 10):
        for j in range(1, 10):
            formatted_number1 = f"{i},,{j}"
            generated_numbers[formatted_number1] = f"{i}.{j}."
            formatted_number1 = f"{i}.{j}"
            generated_numbers[formatted_number1] = f"{i}.{j}."
            formatted_number2 = f"{i},.{j}"
            generated_numbers[formatted_number2] = f"{i}.{j}."
            formatted_number3 = f"{i}.,{j}"
            generated_numbers[formatted_number3] = f"{i}.{j}."
            formatted_number4 = f"{i}..{j}"
            generated_numbers[formatted_number4] = f"{i}.{j}."
            formatted_number5 = f"{i},{j}"
            generated_numbers[formatted_number5] = f"{i}.{j}."
            formatted_number6 = f"{i},{j}."
            generated_numbers[formatted_number6] = f"{i}.{j}."
            formatted_number6 = f".{i}.{j}."
            generated_numbers[formatted_number6] = f"{i}.{j}."
            formatted_number6 = f".{i}.{j}"
            generated_numbers[formatted_number6] = f"{i}.{j}."
            formatted_number6 = f".{i},{j}"
            generated_numbers[formatted_number6] = f"{i}.{j}."
            formatted_number6 = f".{i}{j}"
            generated_numbers[formatted_number6] = f"{i}.{j}."

    # Porównujemy całe teksty z input_list z wygenerowanymi wartościami i dokonujemy zamiany
    for idx, item in enumerate(input_list):
        for key, new_prefix in generated_numbers.items():
            if key in item:
                input_list[idx] = item.replace(key, new_prefix)

    # Zamiana sekwencji typu ".," lub ".." na pojedynczy znak "."
    for idx, item in enumerate(input_list):
        input_list[idx] = item.replace('.,', '.').replace('..', '.')

    # Usuwanie podwójnych tabulatorów
    for idx, item in enumerate(input_list):
        while '\t\t' in item:
            item = item.replace('\t\t', '\t')
        input_list[idx] = item

    # Zwracamy zmodyfikowaną listę
    return input_list
