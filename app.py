import streamlit as st
import numpy as np
import requests
from PIL import Image

st.title("Face Recognition App")

# Instructions
st.markdown("""
**Instructions:**

- **Upload images:** You can upload one image or up to as many as five, but it's recommended to upload three to five images.
- **Image requirements:** Ensure that the images are of the same person.
- **Face extraction:** The app will extract faces from the uploaded images.
- **Storage:** Extracted faces will be stored in the database (Elasticsearch).
""")

uploaded_images_store = st.file_uploader("Upload images to store face", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
if st.button("Store Faces"):
    if uploaded_images_store:
        image_lists = [np.array(Image.open(img)).tolist() for img in uploaded_images_store]
        
        # Call face recognition API to store faces
        payload = {"faces": image_lists}
        response = requests.post("http://localhost:8000/Face_Recognition_ES_multiple_images", json=payload)
        if response.status_code == 200 and "Image Index and Backend called Successfully." in response.text:
            st.success("Person successfully indexed in Database.")
        elif response.status_code == 200 and "Image found." in response.text:
            st.success("Person is already stored in Database.")
        else:
            st.write(response.text)

# Instructions for recognition
st.markdown("""
**Instructions:**

- **Upload images:** You can upload one image or up to as many as five, but it's recommended to upload three to five images.
- **Image requirements:** Ensure that the images are of the same person.
- **Face extraction:** The app will extract faces from the uploaded images.
- **Matching with database:** The app will match the uploaded images with the database (Elasticsearch).
- **Search result:** Based on the similarity search, the app will determine if the person exists in the database.
- **Storage:** If the person is not found, the app will store the face in the database (Elasticsearch).
""")

uploaded_images_recognize = st.file_uploader("Upload images to recognize face", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])
if st.button("Recognize Faces"):
    if uploaded_images_recognize:
        # Convert UploadedFile objects to numpy arrays
        image_lists = [np.array(Image.open(img)).tolist() for img in uploaded_images_store]

        # Call face recognition API to recognize faces
        payload = {"faces": image_lists}
        response = requests.post("http://localhost:8000/Face_Recognition_ES_multiple_images", json=payload)
        if response.status_code == 200 and "Image Index and Backend called Successfully." in response.text:
            st.success("Person not found in the database. Storing face...")
        elif response.status_code == 200 and "Image found." in response.text:
            st.success("Person found in the database.")
        else:
            st.write(response.text)
