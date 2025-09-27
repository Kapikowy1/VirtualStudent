from function import get_data_GPT, get_docx
from bibliography_books import name_docx
from file_processing import purpose, topic
# import os
# import shutil


system_settings = "Be an experienced creator of academic content, assisting in crafting a persuasive summary of an engineering project. Carefully choose words and structures to engage the reader from the very first sentences of the summary. Focus on presenting the essence of the topic, providing context. It's worth noting that the summary and conclusions will be written in a language that is challenging to detect by AI detectors. A significant aspect of scholarly work is utilizing credible sources and supporting statements through citations. Use scientific terminology and expressions. Provide the response in Polish"


assistant_response = get_data_GPT(purpose, topic, system_settings)

heading = 'Streszczenie'

get_docx(name_docx, heading, assistant_response)

