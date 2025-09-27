from function import get_data_GPT, get_docx
from List import name_docx
from file_processing import purpose, topic


system_settings = "Be an experienced creator of academic content, assisting in crafting a compelling introduction for an engineering project. Carefully select words and structures to engage the reader right from the first sentences. Focus on presenting the essence of the topic, providing context, and clearly defining the purpose of the work. The project's goal should be formulated before outlining its scope. At the end, outline the project scope in the form of bullet points. It's worth noting that the introduction will be written in a language that is challenging to detect by AI detectors. The introduction should be comprehensive enough to immerse the reader in the context, yet concise enough to maintain their attention. The introduction should be around 500 words long. An essential aspect of scholarly work is utilizing credible sources and supporting claims through citations. Use scientific terminology and statements. Provide the answer in Polish"

assistant_response = get_data_GPT(purpose, topic, system_settings)

heading = '1. Wstęp'

get_docx(name_docx, heading, assistant_response)
