import numpy as np
import pandas as pd
import joblib
import streamlit as st
import os

# Load Model
model = joblib.load('Calories_prediction.pkl')

def calories_prediction(input_data):
    column_names = ['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']
    input_data = np.array(input_data).reshape(1, -1)
    input_df = pd.DataFrame(input_data, columns=column_names)
    pred = model.predict(input_df)
    return pred[0] ** 2

# File to store user data
data_file = "user_data.csv"

def save_user_data(user_details):
    df = pd.DataFrame([user_details])
    if os.path.exists(data_file):
        existing_df = pd.read_csv(data_file)
        if not existing_df[(existing_df['Name'] == user_details["Name"]) & (existing_df['Age'] == user_details["Age"])].empty:
            return  # Prevent duplicate entries
        df.to_csv(data_file, mode='a', header=False, index=False)
    else:
        df.to_csv(data_file, index=False)

def load_user_data(name):
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        return df[df['Name'] == name]  # Show only the logged-in user's data
    return pd.DataFrame()

# Streamlit UI
def main():
    st.set_page_config(page_title="Torch & Track: Burn Calories Smarter!", layout="wide")
    
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
    st.image("front_pic.jpg", use_container_width=True)
    
    st.title("👟 Torch & Track: Burn Calories Smarter!")
    st.write("Enter your details and exercise data to estimate the calories you burn.")
    
    # Personal Details Section
    st.subheader("👤 Personal Details")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        age = st.text_input("Age (years)")
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
    
    st.write("🔹 **Units:** Height (cm), Weight (kg), Temperature (°C), Heart Rate (bpm)")
    
    # Calories Prediction Section
    st.subheader("🏃🏾‍➡ Exercise Details")
    col1, col2, col3 = st.columns(3)
    inputs = []
    fields = {
        'Height': 'Height (cm)',
        'Weight': 'Weight (kg)',
        'Duration': 'Duration (minutes)',
        'Heart_Rate': 'Heart Rate (bpm)',
        'Body_Temp': 'Body Temp (°C)'
    }

    for i, (field, label) in enumerate(fields.items()):
        with [col1, col2, col3][i % 3]:
            value = st.text_input(f"{label}", key=field)
            inputs.append(value)
    
    prediction = ""

    # Save details and predict calories
    if st.button("💪 Predict Calories Burnt"):
        if "" in inputs or not age:
            st.warning("⚠️ Please fill in all fields with valid numeric values.")
        else:
            try:
                input_data = [float(age)] + [float(value) for value in inputs]  # Convert inputs to float
                prediction = calories_prediction(input_data)
                user_details = {"Name": name, "Age": age, "Gender": gender, "Activity Level": activity_level, 
                                "Height": inputs[0], "Weight": inputs[1], "Duration": inputs[2],
                                "Heart Rate": inputs[3], "Body Temp": inputs[4], "Calories Burnt": prediction}
                save_user_data(user_details)
                
                st.subheader("🏋️ Calories Burnt:")
                st.write(f"🔥 {prediction:.2f} kcal")  
            except ValueError:
                st.warning("⚠️ Please enter valid numeric values in all fields.")
            
            # Display GIF after prediction
            st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGl6Y3hlcndqYTIwc2wzdXd6bmNxa3M0ZTNhemx3d3hyNzNqeWg0bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XeY6MgvUXdWF5in9I1/giphy.gif", use_container_width=True)
    
    # Display past records for the logged-in user
    st.subheader("📜 Your Saved Records")
    if name:
        user_data = load_user_data(name)
        if not user_data.empty:
            st.dataframe(user_data)
        else:
            st.write("No records found for you.")

if __name__ == '__main__':
    main()
