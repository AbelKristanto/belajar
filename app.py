# library yang digunakan
import streamlit as st
import pandas as pd
import pickle
from PIL import Image
import numpy as np
import time
import os
print("get directory", os.getcwd())
# import model iris
loaded_model_iris = pickle.load(open('model/generate_iris.pkl', 'rb'))

# import model heart_disease
loaded_model_heart = pickle.load(open('model/model.pkl', 'rb'))

# set page config
st.set_page_config(page_title="Halaman Modelling", layout="wide", initial_sidebar_state="auto")

## Judul Halaman
def judul():
    st.write("""
    # Welcome to my machine learning dashboard
    This dashboard created by : [@abelkristanto](https://www.linkedin.com/in/abelkristanto/)
    """)
    st.html("<font face='Times New Roman'>This <b>is</b> a simple text in Times New Roman font.</font>")

add_selectitem = st.sidebar.selectbox("Want to open about?", ("Iris species!", "Heart Disease!", "About Me!"))

def about_me():
    st.write("""
    This app is created by **Abel Kristanto**
    
    You can find me on [LinkedIn](https://www.linkedin.com/in/abelkristanto/) and [GitHub](https://github.com/abelkristanto)
    """)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def iris():
    # Intro
    st.sidebar.write("Enter the features of the iris flower below:")
    st.header("*Iris Species Prediction*")
    st.write("""
    This app predicts the **Iris Species**
    Data obtained from the [iris dataset](https://www.kaggle.com/uciml/iris) by UCIML. 
    """)
    # Display image
    st.image('image/iris.JPG', width=500)
    # Input features
    sepal_length = st.sidebar.number_input("Sepal Length (cm)", min_value=0.0, max_value=10.0, value=5.0)
    sepal_width = st.sidebar.number_input("Sepal Width (cm)", min_value=0.0, max_value=10.0, value=3.5, key="sepal_width")
    petal_length = st.sidebar.number_input("Petal Length (cm)", min_value=0.0, max_value=10.0, value=1.5, key="petal_length")
    petal_width = st.sidebar.number_input("Petal Width (cm)", min_value=0.0, max_value=10.0, value=0.2, key="petal_width")
    data = {'sepal_length': sepal_length,
            'sepal_width': sepal_width,
            'petal_length': petal_length,
            'petal_width': petal_width}
    
    # Create DataFrame for prediction
    features = pd.DataFrame(data, index=[0])
    if st.sidebar.button("Predict"):
        
        # Make prediction
        prediction = loaded_model_iris.predict(features)
        result = ['Iris-setosa' if prediction == 0 else 'Iris-versicolor' if prediction == 1 else 'Iris-virginica']
        output = str(result[0])
        with st.spinner("Predicting..."):
            time.sleep(2)
            st.balloons()
            st.success(f"The predicted species is: {output}")

def heart():
    st.header("*Heart Disease Prediction*")
    st.write("""
    This app predicts the **Heart Disease**
    
    Data obtained from the [Heart Disease dataset](https://archive.ics.uci.edu/dataset/45/heart+disease) by UCIML. 
    """)
    st.sidebar.header('User Input Features:')
    st.image('image/heart-disease.jpg', width=500)
    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
    else:
        def user_input_features():
            st.sidebar.header('Input Manual')
            age = st.sidebar.slider('Age', 29, 77, 54)
            sex = st.sidebar.selectbox('Sex', ['Male', 'Female'])
            cp_first = st.sidebar.selectbox('Chest Pain Type', ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])
            if cp_first == 'Typical Angina':
                cp = 1
            elif cp_first == 'Atypical Angina':
                cp = 2
            elif cp_first == 'Non-anginal Pain':
                cp = 3
            else:
                cp = 4
            thalach = st.sidebar.slider('Maximum Heart Rate Achieved', 71, 202, 150)
            exang = st.sidebar.selectbox('Exercise Induced Angina', ['Yes', 'No'])
            if exang == 'Yes':
                exang = 1
            else:
                exang = 0
            oldpeak = st.sidebar.slider('ST Depression Induced by Exercise Relative to Rest', 0.0, 6.2, 1.0)
            slope = st.sidebar.selectbox('Slope of the Peak Exercise ST Segment', ['Upsloping', 'Flat', 'Downsloping'])
            if slope == 'Upsloping':
                slope = 1
            elif slope == 'Flat':
                slope = 2
            else:
                slope = 3
            ca = st.sidebar.slider('Number of Major Vessels Colored by Fluoroscopy (0-3)', 0, 3, 0)
            thal = st.sidebar.selectbox('Thalassemia', ['Normal', 'Fixed Defect', 'Reversable Defect'])
            if thal == 'Normal':
                thal = 3
            elif thal == 'Fixed Defect':
                thal = 6
            else:
                thal = 7
            sex = 1 if sex == 'Male' else 0
            
            data = {'cp': cp,
                    'thalach': thalach,
                    'slope': slope,
                    'oldpeak': oldpeak,
                    'exang': exang,
                    'ca': ca,
                    'thal': thal,
                    'sex': sex,
                    'age': age}
            features = pd.DataFrame(data, index=[0])
            return features
        input_df = user_input_features()
        if st.sidebar.button('Predict!'):
            prediction = loaded_model_heart.predict(input_df)
            result = ['No Heart Disease' if prediction == 0 else 'Heart Disease']
            output = str(result[0])
            with st.spinner('Wait for it...'):
                time.sleep(4)
                st.success(f"Prediction of this app is {output}")


if add_selectitem == "Iris species!":
    iris()
if add_selectitem == "About Me!":   
    judul()
    about_me()
if add_selectitem == "Heart Disease!":
    heart()
