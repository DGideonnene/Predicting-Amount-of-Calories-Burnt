import numpy as np
import pandas as pd
import joblib
import streamlit as st
import os
import hashlib

# Load Model
model = joblib.load('Calories_prediction.pkl')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    auth_file = "user_auth.csv"
    if os.path.exists(auth_file):
        df = pd.read_csv(auth_file)
        hashed_pw = hash_password(password)
        if ((df['Email'] == email) & (df['Password'] == hashed_pw)).any():
            return True
    return False

def register_user(email, password):
    auth_file = "user_auth.csv"
    hashed_pw = hash_password(password)
    new_user = pd.DataFrame([[email, hashed_pw]], columns=['Email', 'Password'])
    if os.path.exists(auth_file):
        existing_df = pd.read_csv(auth_file)
        if (existing_df['Email'] == email).any():
            return False
        new_user.to_csv(auth_file, mode='a', header=False, index=False)
    else:
        new_user.to_csv(auth_file, index=False)
    return True

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
        if not existing_df[(existing_df['Email'] == user_details["Email"])].empty:
            return  # Prevent duplicate entries
        df.to_csv(data_file, mode='a', header=False, index=False)
    else:
        df.to_csv(data_file, index=False)

def load_user_data(email):
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        return df[df['Email'] == email]  # Show only the logged-in user's data
    return pd.DataFrame()

# Streamlit UI
def main():
    st.set_page_config(page_title="Torch & Track: Burn Calories Smarter!", layout="wide")
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.email = ""
    
    # User Authentication
    st.sidebar.subheader("🔐 Login or Register")
    auth_choice = st.sidebar.radio("Select an option", ["Login", "Register"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    
    if auth_choice == "Register":
        if st.sidebar.button("Register"):
            if register_user(email, password):
                st.sidebar.success("✅ Registration successful! Please log in.")
            else:
                st.sidebar.error("⚠️ User already exists!")
    
    if auth_choice == "Login":
        if st.sidebar.button("Login"):
            if authenticate_user(email, password):
                st.sidebar.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.session_state.email = email
            else:
                st.sidebar.error("⚠️ Invalid credentials!")
                st.session_state.logged_in = False
    
    if st.session_state.logged_in:
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
                    user_details = {"Email": st.session_state.email, "Name": name, "Age": age, "Gender": gender, "Activity Level": activity_level, 
                                    "Height": inputs[0], "Weight": inputs[1], "Duration": inputs[2],
                                    "Heart Rate": inputs[3], "Body Temp": inputs[4], "Calories Burnt": prediction}
                    save_user_data(user_details)
                    
                    st.subheader("🏋️ Calories Burnt:")
                    st.write(f"🔥 {prediction:.2f} kcal")  
                except ValueError:
                    st.warning("⚠️ Please enter valid numeric values in all fields.")
        
        # Display past records for the logged-in user
        st.subheader("📜 Your Saved Records")
        user_data = load_user_data(st.session_state.email)
        if not user_data.empty:
            st.dataframe(user_data)
        else:
            st.write("No records found for you.")

if __name__ == '__main__':
    main()
