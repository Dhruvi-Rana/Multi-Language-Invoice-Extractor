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
