from openai import OpenAI
from decouple import config


# Import data

input_text = "Ważną cechą sieci neuronowych jest zdolność uczenia się poprzez dostosowywanie wag połączeń między jej elementami. Proces ten polega na prezentowaniu sieci zestawu treningowego - zbioru danych wejściowych razem z odpowiadającymi im prawidłowymi odpowiedziami - oraz modyfikacji wag tak, aby minimalizować błąd pomiędzy predykowanym a rzeczywistym wynikiem."
purpose = "Celem tej pracy inżynierskiej jest zaprojektowanie i implementacja optymalizowanych sieci neuronowych do przetwarzania obrazów w czasie rzeczywistym. W ramach tego projektu, będziesz badać różne techniki optymalizacji, takie jak przycinanie wag, kwantyzację i binarzację, aby zmniejszyć złożoność obliczeniową sieci neuronowych bez znaczącego wpływu na ich dokładność. Wyniki twojej pracy mogą znaleźć zastosowanie w wielu dziedzinach, takich jak rozpoznawanie obrazów, analiza wideo w czasie rzeczywistym, autonomiczne pojazdy i wiele innych"
topic = "Optymalizacja sieci neuronowych dla przetwarzania obrazów w czasie rzeczywistym"


# GPT API

sytem_settings = "Be an experienced creator of academic content, assisting in refining the provided text for an engineering project. Carefully choose words and structures to improve the given text as effectively as possible. It is worth noting that the revised text will be written in a manner that is challenging for AI detectors to identify. Use scientific terminology and expressions. Omit stating the purpose and title, as well as other phrases. Provide the response in Polish"


client = OpenAI(api_key=config("OPENAI_API_KEY"))


def get_GPT_edit_text(purpose, topic, sytem_settings, input_text, model="gpt-4-0613", temperature=0.25, max_tokens=4096, top_p=1, frequency_penalty=1.5, presence_penalty=1):

    response = client.chat.completions.create(


        model=model,

        messages=[


            {


                "role": "system",


                "content": sytem_settings


            },


            {


                "role": "user",


                "content": f"Na podstawie cel pracy: {purpose} i temat pracy: {topic} zmień tekst: {input_text}"


            }


        ],

        temperature=temperature,


        max_tokens=max_tokens,

        top_p=top_p,


        frequency_penalty=frequency_penalty,

        presence_penalty=presence_penalty


    )

    return response.choices[0].message.content


assistant_response = get_GPT_edit_text(
    purpose, topic, sytem_settings, input_text)

# Podziel tekst na linie
lines = assistant_response.split('\n')

# Pomiń pierwszą linię i połącz resztę z powrotem w ciąg
output = '\n'.join(lines[1:])

print(output)
