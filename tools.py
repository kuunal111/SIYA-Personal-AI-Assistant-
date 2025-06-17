from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun

from dotenv import load_dotenv
import os
import openai
import  requests
from PIL import Image
from io import BytesIO  

def searchWeb(parameters): 
    query = parameters.get("query")
    results = DuckDuckGoSearchRun(query=query)
    return results

def save_to_text_file(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")

    formatted_data = f"{data}"


    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_data + "\n")


def create_html_file(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")
    title = parameters.get("title")

    formatted_data = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <p>{data}</p> 
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(formatted_data)

def generate_image(parameter):
    prompt = parameter.get("prompt")
    filename = parameter.get("filename")
    size = parameter.get("size", "1024x1024")
    save_dir = parameter.get("save_dir", "genetared_images")

    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    client = openai.OpenAI()

    response = openai.images.generate(
        prompt=prompt,
        model="dall-e-3",
        n=1,
        size=size,
        quality="standard"
    )

    image_url = response.data[0].url
    print(response)

    imgage_response = requests.get(image_url)
    image = Image.open(BytesIO(imgage_response.content))
    image.save(filepath)


ClientTools = ClientTools()
ClientTools.register("searchWeb", searchWeb)
ClientTools.register("save_to_text_file", save_to_text_file)
ClientTools.register("create_html_file", create_html_file)
ClientTools.register("generate_image", generate_image)