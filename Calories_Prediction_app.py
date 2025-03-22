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
    
    # Add Image
    #/mnt/data/alexander-red-d3bYmnZ0ank-unsplash (1).jpg
    #https://unsplash.com/photos/man-tying-his-shoes-d3bYmnZ0ank
    st.image("https://unsplash.com/photos/man-tying-his-shoes-d3bYmnZ0ank", use_container_width=True)
    
    st.title("🔥 Calories Burnt Prediction 🔥")
    st.write("Enter your exercise details to estimate the calories you burn.")
    
    # Create input fields
    col1, col2, col3 = st.columns(3)
    inputs = []
    fields = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']

    for i, field in enumerate(fields):
        with [col1, col2, col3][i % 3]:
            value = st.text_input(f"{field.replace('_', ' ').capitalize()} (e.g. 25)", key=field)
            inputs.append(value)

    prediction = ""
    
    if st.button("💪 Predict Calories Burnt"):
        try:
            input_data = [float(value) for value in inputs]
            prediction = calories_prediction(input_data)
        except ValueError:
            prediction = "⚠️ Please enter valid numeric values in all fields."
    
    if prediction:
        st.subheader("🏋️ Calories Burnt:")
        st.write(f"🔥 {prediction:.2f} kcal")

if __name__ == '__main__':
    main()
