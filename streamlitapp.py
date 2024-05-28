import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import cv2
import pickle
import requests
from streamlit_lottie import st_lottie
import pyrebase
import pandas as pd
from keras.models import load_model
from keras.applications.resnet import preprocess_input
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

st.set_page_config(
    page_title="CARDIO APP",
    page_icon="❤",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_menu_style = """
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

firebaseConfig = {
  'apiKey': "AIzaSyBOfECPmIIaF0qt6IGgIqSxyHeGxvfvpGE",
  'authDomain': "test-heart-dc84b.firebaseapp.com",
  'projectId': "test-heart-dc84b",
  'storageBucket': "test-heart-dc84b.appspot.com",
  'messagingSenderId': "620226178379",
  'appId': "1:620226178379:web:7f9301e9e197b5d8a2ccce",
  'measurementId': "G-85Q95KC866",
  'databaseURL': "https://test-heart-dc84b-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

text = st.sidebar.error('CARDIO APP ❤')

choice = st.sidebar.selectbox('LOGIN/SIGNUP', ['Login', 'Signup'])
email = st.sidebar.text_input('ENTER YOUR EMAIL ADDRESS')
password = st.sidebar.text_input('ENTER YOUR PASSWORD', type='password')

if choice == 'Signup':
    handle = st.sidebar.text_input("ENTER YOUR NAME", value='default')
    submit = st.sidebar.button('CREATE ACCOUNT')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.sidebar.success('ACCOUNT CREATED SUCCESSFULLY')
        st.info('WELCOME' + '--' + handle)
        st.caption('THANKS FOR SIGNING UP, PLEASE LOGIN TO CONTINUE')
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child('Handle').set(handle)
        db.child(user['localId']).child('Id').set(user['localId'])

if choice == 'Login':
    login = st.sidebar.checkbox('Login')

    if login:
        st.sidebar.success('LOGGED IN SUCCESSFULLY')
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio>div{flex-direction:row;}</style>', unsafe_allow_html=True)

        selected2 = option_menu(None, ["Home", "DIAGNOSE CAD", "PREDICT HEART DISEASE", 'DOCTOR DETAILS'],
                                icons=['house', 'cloud-upload', "activity", 'envelope'],
                                menu_icon="cast", default_index=0, orientation="horizontal",
                                styles={
                                    "container": {"padding": "0!important", "background-color": "#000000"},
                                    "icon": {"color": "red", "font-size": "20px"},
                                    "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#413839"},
                                    "nav-link-selected": {"background-color": "#000000"},
                                })

        if selected2 == 'Home':
            new_title = '<p style="font-family:Georgia; color:#00FFFF; font-size: 34px;">GUIDELINES OF THE CARDIO APP</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            new_title = '<p style="font-family:Open Sans; color:#FFFFFF; font-size: 24px;">The Cardio app aims at helping people by diagnosing coronary artery blockage and heart disease immediately. The main advantage is, it diagnose the disease automatically without the help of doctor. Using Artificial Intelligence(AI) the app is developed and make sure to consult the doctor for the confirmation of diseases.</p>'
            st.markdown(new_title, unsafe_allow_html=True)

            new_title = '<p style="font-family:Georgia; color:#00FFFF; font-size: 34px;">HOW TO USE THE APP</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            video_file = open('C:/Users/Kotha/Documents/Wondershare Filmora 9/Output/demo_instruc.mp4', 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)

            new_title = '<p style="font-family:Georgia; color:#00FFFF; font-size: 34px;">HOW TO PREVENT HEART PROBLEMS ?</p>'
            st.markdown(new_title, unsafe_allow_html=True)

            st.write('⭕ Don’t smoke or use tobacco')
            st.write('⭕ Manage high cholesterol, high blood pressure and diabetes')
            st.write('⭕ Eat a heart-healthy diet.')
            st.write('⭕ Limit alcohol use')
            st.write('⭕ Manage stress')
            st.write('⭕ Increase your activity level. Exercise helps you lose weight, improve your physical condition and relieve stress.')
            st.write('⭕ Do 30 minutes of walking 5 times per week or walking 10,000 steps per day')

            new_title = '<p style="font-family:Georgia; color:#00FFFF; font-size: 34px;">SOME FACTS ABOUT THE HEART</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            st.write('⭕ The average heart is the size of a fist in an adult')
            st.write('⭕ Your heart will beat about 115,000 times each day')
            st.write('⭕ Your heart pumps about 2,000 gallons of blood every day')
            st.write('⭕ The heart pumps blood through 60,000 miles of blood vessels')
            st.write('⭕ A woman’s heart beats slightly faster than a man’s heart')
            st.write('⭕ The heart can continue beating even when it’s disconnected from the body')
            st.write('⭕ Laughing is good for your heart. It reduces stress and gives a boost to your immune system')

            def load_lottieurl(url: str):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()

            lottie_url_hello = "https://assets3.lottiefiles.com/packages/lf20_0ssane8p.json"
            lottie_url_download = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
            lottie_hello = load_lottieurl(lottie_url_hello)
            lottie_download = load_lottieurl(lottie_url_download)
            st_lottie(lottie_hello, key="hello")

        if selected2 == 'DIAGNOSE CAD':
            model = load_model("C:/Users
