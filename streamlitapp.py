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
            model = load_model("C:/Users/Kotha/Downloads/AKGKMODEL.h5")
            new_title = '<p style="font-family:Georgia; color:##00FFFF; font-size: 29px;">DETECT CORONARY ARTERY BLOCKAGE BY CT SCAN</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Import your CT scan image here", type=["jpg", "jpeg"])

            class_type = {0: 'NO', 1: 'YES'}
            if uploaded_file is not None:
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                opencv_image = cv2.imdecode(file_bytes, 1)
                opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
                resized = cv2.resize(opencv_image, (512, 512))
                img = np.reshape(resized, [1, 512, 512, 3])

                st.image(opencv_image, channels="RGB")

                resized = preprocess_input(resized)
                img_reshape = resized[np.newaxis]

                Genrate_pred = st.button("DIAGNOSE")
                if Genrate_pred:
                    prediction = model.predict(img_reshape).argmax()
                    res = class_type[np.argmax(model.predict(img))]

                    if res == 'YES':
                        st.error(f"Sorry, Our app confirms that you are having the chances of blockage is  : {model.predict(img)[0][1]*100} percent")
                        st.warning('Please consult the doctor immediately !!!')
                    else:
                        st.success(f"our app confirms that the chances of being Normal is : {model.predict(img)[0][0]*100} percent")
                        st.info('If needed consult the doctor')

        if selected2 == 'DOCTOR DETAILS':
            new_title = '<p style="font-family:Georgia; color:##00FFFF; font-size: 29px;">CONSULT THE DOCTOR AND BOOK AN APPOINTMENT</p>'
            st.markdown(new_title, unsafe_allow_html=True)
            path = r"C:/Users/Kotha/Documents/project.csv"
            df = pd.read_csv(path)
            st.dataframe(df)

        if selected2 == 'PREDICT HEART DISEASE':
            loaded_model = pickle.load(open('C:/Users/Kotha/Downloads/trainedrfmodelofheart.sav', 'rb'))

            def heart(input_data):
                input_data_as_numpy_array = np.asarray(input_data)
                input_reshape = input_data_as_numpy_array.reshape(1, -1)
                prediction = loaded_model.predict(input_reshape)

                if prediction[0] == 0:
                    return st.success('This person has less chance of heart attack')
                else:
                    return st.error('This person has more chance of heart attack')

            def main():
                new_title = '<p style="font-family:Georgia; color:##00FFFF; font-size: 34px;">HEART DISEASE PREDICTION</p>'
                st.markdown(new_title, unsafe_allow_html=True)
                age = st.text_input('AGE')
                sex = st.radio("Select Gender: ", ('1', '0'))
                if sex == '1':
                    st.info("Male")
                else:
                    st.info("Female")
                st.write('<style>div.row-widget.stRadio>div{flex-direction:row;}</style>', unsafe_allow_html=True)
                chestpaintype = st.radio("CHEST PAIN TYPE (0 = typical angina,1 = atypical angina,2 = non — anginal pain,3= asymptotic)", ('0', '1', '2', '3'))
                restingbps = st.text_input('RESTING BLOOD PRESSURE')
                cholestrol = st.text_input('CHOLESTROL')
                fastingbloodsugar = st.radio("FASTING BLOOD SUGAR( > 120mg/dl : 1, else : 0)", ('1', '0'))
                restingecg = st.radio("RESTING ECG(0-normal, 1-abnormal)", ('0', '1'))
                maxheartrate = st.text_input('MAXIMUM HEART RATE ACHIEVED')
                exerciseangina = st.radio("EXERCISE INDUCED ANGINA(1-yes, 0-no)", ('1', '0'))
                oldpeak = st.text_input('ST DEPRESSION INDUCED BY EXERCISE REALTIVE TO REST')
                STslope = st.radio("PEAK EXERCISE ST SEGMENT(0 = upsloping,1 = flat,2= downsloping)", ('0', '1', '2'))

                if st.button('PREDICT'):
                    heart([age, sex, chestpaintype, restingbps, cholestrol, fastingbloodsugar, restingecg, maxheartrate, exerciseangina, oldpeak, STslope])

            if __name__ == '__main__':
                main()
