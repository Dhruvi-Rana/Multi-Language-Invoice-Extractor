from dotenv import load_dotenv

load_dotenv() #load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as ai

ai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#Function to load Gemini Pro Vision
# model=ai.GenerativeModel('gemini-pro-vision')
model = ai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_detail(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts= [
            {
                "mime_type": uploaded_file.type,  #get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploded")

#initialize our stramlit app

st.set_page_config(page_title="MutiLanguage Invoice Extractor")
st.header("gemini Application")
input = st.text_input("Image Prompt: ", key="input") #space is recommended-> input space = space st..
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image/Invoice", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload a image as invoice
and you will have to answer any questions based on the uploaded invoices image
"""

#If submit butoon is clicked
if submit:
    image_data=input_image_detail(uploaded_file)
    response=get_gemini_response(input_prompt, image_data,input)
    st.subheader("The Response is")
    st.write(response)






# from dotenv import load_dotenv
# import streamlit as st
# import os
# from google.cloud import generativeai 

# load_dotenv()

# # Initialize Gemini
# # 
# # Initialize client
# client = generativeai.GenerativeAiClient(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(prompt, image):
#     # Use client to call API
#     response = client.generate(prompt, visuals=[image])
#     return response

# def input_image_detail(uploaded_file):
#     if uploaded_file is not None:
#         return uploaded_file
#     else:
#         raise FileNotFoundError("No file uploaded")

# # Streamlit App
# st.set_page_config(page_title="Multilingual Invoice Extractor")
# st.header("Gemini Application")

# input_prompt = st.text_input("Image Prompt: ", key="input")
# uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     image = uploaded_file
#     st.image(image, caption="Uploaded Image/Invoice", use_column_width=True)

# submit = st.button("Tell me about the invoice")

# # Default prompt
# default_prompt = """
# You are an expert in understanding invoices. We will upload an image as an invoice, 
# and you will have to answer any questions based on the uploaded invoice image.
# """

# # If submit button is clicked
# if submit:
#     image_data = input_image_detail(uploaded_file)
#     prompt = default_prompt + "\n" + input_prompt
#     response = get_gemini_response(prompt, image_data)
#     st.subheader("The Response is")
#     st.write(response)