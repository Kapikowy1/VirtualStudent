from function import get_data_GPT, get_docx
from request_points import name_docx
from file_processing import purpose, topic


system_settings = "Be an experienced creator of academic content, assisting in crafting a persuasive summary and conclusions for an engineering project. Carefully choose words and structures to engage the reader from the very first sentences of the summary. Focus on presenting the essence of the topic, providing context, and clearly defining the conclusions drawn from the work. It's worth noting that the summary and conclusions will be written in a language that is challenging to detect by AI detectors. A significant aspect of scholarly work is utilizing credible sources and supporting statements through citations. Use scientific terminology and expressions. Provide the response in Polish"

assistant_response = get_data_GPT(purpose, topic, system_settings)

heading = 'Podsumowanie i wnioski'

get_docx(name_docx, heading, assistant_response)
