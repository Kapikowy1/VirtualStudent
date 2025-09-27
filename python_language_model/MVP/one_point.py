from language_model_introduction import name_docx
from file_processing import topic
import function
from ListCleaner import cleaned_data2


points = cleaned_data2
point = points[0]

system_settings = "Be an experienced creator of academic content, assisting in creating and editing a lengthy text for the given point of an engineering project. Carefully select words and structures to engage the reader right from the first sentences. Focus on presenting the essence of the topic and providing context. It's worth noting that the text will be written in a language that is challenging to detect by AI detectors. The text should be comprehensive enough to immerse the reader in the context, yet concise enough to maintain their attention. The text should be a minimum of 500 words. An essential aspect of scholarly work is utilizing credible sources. Use scientific terminology and statements. Don't include the purpose of the work in the generated text. Provide the answer in Polish"

assistant_response = function.get_GPT_request_point(
    point, topic, system_settings, model="gpt-3.5-turbo-16k")

heading = f'2.{point}'

function.get_docx(name_docx, heading, assistant_response)
