import numpy as np
import pandas as pd
import joblib
import streamlit as st

# Load Model
model = joblib.load('Calories_prediction.pkl')

def calories_prediction(input_data):
    column_names = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
    input_data = np.array(input_data).reshape(1, -1)
    input_df = pd.DataFrame(input_data, columns=column_names)
    pred = model.predict(input_df)
    prediction = pred[0]
    result = prediction**2
    return result

# Streamlit UI
def main():
    st.set_page_config(page_title="Calories Prediction", layout="wide")
    
    # Custom styling
    st.markdown(
        """
        <style>
            .main {background-color: #eef2f3;}
            h1 {color: #ff5722; text-align: center;}
            .stButton>button {width: 100%; background-color: #ff5722; color: white; font-size: 16px;}
            .stTextInput>label {font-weight: bold;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Header Image
    st.image("https://unsplash.com/photos/man-tying-his-shoes-d3bYmnZ0ank", use_container_width=True)
    
    st.title("🔥 Calories Burnt Prediction 🔥")
    st.write("Enter your details and exercise data to estimate the calories you burn.")
    
    # Personal Details Section
    st.subheader("👤 Personal Details")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        age = st.text_input("Age")
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    
    # Calories Prediction Section
    st.subheader("🔥 Exercise Details")
    col1, col2, col3 = st.columns(3)
    inputs = []
    fields = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']

    for i, field in enumerate(fields):
        with [col1, col2, col3][i % 3]:
            value = st.text_input(f"{field.replace('_', ' ').capitalize()} (e.g. 25)", key=field)
            inputs.append(value)
    
    prediction = ""

    # Proper indentation applied here 👇
    if st.button("💪 Predict Calories Burnt"):
        try:
            input_data = [float(value) for value in inputs]  # Convert inputs to float
            prediction = calories_prediction(input_data)
        except ValueError:
            prediction = "⚠️ Please enter valid numeric values in all fields."

        if isinstance(prediction, (int, float)):  # Check if it's a number
            st.subheader("🏋️ Calories Burnt:")
            st.write(f"🔥 {prediction:.2f} kcal")  
        else:
            st.write(prediction)  # Display error message as a string
        
        # Display GIF after prediction
        st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGl6Y3hlcndqYTIwc2wzdXd6bmNxa3M0ZTNhemx3d3hyNzNqeWg0bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XeY6MgvUXdWF5in9I1/giphy.gif", use_container_width=True)
        
if __name__ == '__main__':
    main()
