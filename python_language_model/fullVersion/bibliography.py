from openai import OpenAI
from decouple import config
from function import get_GPT_request_point
from summaries_and_Conclusions import name_docx, topic
from docx import Document
from List import assistant_response_list
import re
import requests
from requests.exceptions import ReadTimeout


client = OpenAI(api_key=config("OPENAI_API_KEY"))

system_settings = "You provide three links to points based on the topic of the work. Only scientific sources are provided. Make sure your response is in Polish. The links should be to websites of the https type."

# Otwarcie istniejącego dokumentu
doc = Document(name_docx)

# Podział tekstu na linie
lines = assistant_response_list.split('\n')

# Pominięcie sekcji "Literatura", "Streszczenie" i "Podsumowanie i wnioski"
filtered_lines = [line for line in lines if not any(
    section in line.lower() for section in ["literatura", "streszczenie", "Podsumowanie i wnioski"])]

# Tworzenie nowego nagłówka na potrzeby każdego elementu
doc.add_heading("Literatura", level=1)

# Zbiór przechowujący odwiedzone linki
visited_links = set()
visited_domains = set()  # Zbiór przechowujący odwiedzone domeny

for point in filtered_lines:
    assistant_response = get_GPT_request_point(
        point, topic, system_settings, temperature=0.25)

    # Finding links in the response text
    links = re.findall(r'(https?://\S+)', assistant_response)

    # Usunięcie dodatkowych linków w nawiasach
    clean_links = [re.sub(r'\]\(.+?\)', '', link) for link in links]

    for clean_link in clean_links:
        try:
            if clean_link.strip() and clean_link not in visited_links:
                # Wyodrębnienie pierwszego członu linku
                first_part = clean_link.split('/')[2]
                if first_part not in visited_domains:
                    # Dodanie pierwszego członu linku do zbioru odwiedzonych domen
                    visited_domains.add(first_part)
                    # Dodanie linka do zbioru odwiedzonych linków
                    visited_links.add(clean_link)
                    # Zwiększenie czasu oczekiwania na odpowiedź do 10 sekund
                    response = requests.head(clean_link, timeout=10)
                    if response.status_code == 200:
                        # Dodanie linku do dokumentu DOCX
                        p = doc.add_paragraph()
                        p.add_run(f"- {clean_link}")
                        p.alignment = 0  # Ustawienie wartości 0 dla lewego wyjustowania
                    elif response.status_code == 302:
                        # Sprawdzenie, czy w odpowiedzi znajduje się nagłówek "Location", który zawiera nowy adres URL
                        if 'Location' in response.headers:
                            new_url = response.headers['Location']
                            # Teraz możesz wykonać kolejne żądanie do nowego adresu URL, na przykład:
                            try:
                                if new_url.strip():  # Sprawdzenie, czy nowy adres URL nie jest pustym łańcuchem
                                    # Zwiększenie czasu oczekiwania na odpowiedź do 10 sekund
                                    new_response = requests.get(
                                        new_url, timeout=10)
                                    # Sprawdzenie, czy żądanie zostało pomyślnie wykonane
                                    if new_response.status_code == 200:
                                        # Dodanie nowego linku do dokumentu DOCX
                                        p = doc.add_paragraph()
                                        p.add_run(f"- {new_url}")
                                        p.alignment = 0  # Ustawienie wartości 0 dla lewego wyjustowania
                                        # Dodanie linka do zbioru odwiedzonych linków
                                        visited_links.add(new_url)
                            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.RequestException) as e:
                                print(
                                    f"Błąd podczas łączenia z {new_url}: {e}. Link zostanie pominięty.")
                                pass
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            print(
                f"Błąd podczas łączenia z {clean_link}: {e}. Link zostanie pominięty.")
            pass
        except requests.exceptions.InvalidURL:
            print(
                f"Nieprawidłowy adres URL: {clean_link}. Link zostanie pominięty.")
            pass
        except ReadTimeout:
            print(
                f"Czas oczekiwania na odpowiedź z {clean_link} przekroczony. Link zostanie pominięty.")
            pass

# Zapisz zaktualizowany dokument DOCX
doc.save(name_docx)
