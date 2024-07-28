import streamlit as st
import pandas as pd
from util import load_data, preprocess_data, get_medicine_info, set_background
from model import train_model, find_medicine
# Set background image
set_background('dr_penguin4.gif')

# Load and preprocess data
data_file = 'medicine_dataset.csv'
data = load_data(data_file)
data = preprocess_data(data)

# Train model
vectorizer, model = train_model(data)



#IMPORTANT NOTICE 
st.markdown('<div class="overlay">IT WILL ANALYZING WITH AI, THIS APP IS IN THE TESTING MODE NOW.</div>', unsafe_allow_html=True)
st.markdown('<div class="warning">IN ANY EMERGENCY CONDITION CONSULT WITH A DOCTOR AND DO NOT TAKE THE SUBSTITUTE MEDICINE</div>', unsafe_allow_html=True)
# Custom CSS for background and styling
st.markdown(
     """
    <style>
    .main {
        background-color:yellow;
        background-size: cover;
    }
    h1 {
        color: #4CAF50;
        text-align: center;
        animation: fadeIn 2s;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        animation: fadeIn 2s;
    }
    .stTextInput input {
        background-color: #e0f7fa;
        border-radius: 5px;
        border: 2px solid #4CAF50;
        color: #4CAF50;
        animation: fadeIn 2s;
    }
    .info-box {
        background-color: #e0f7fa;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        animation: fadeIn 2s;
        white-space: pre-line;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("DR+ Medicine Information Finder")

# Initialize the session state
if 'search_button' not in st.session_state:
    st.session_state['search_button'] = False

# Input field
medicine_name = st.text_input("Enter the name of the medicine:")

# JavaScript to trigger the search button on Enter key press
st.markdown(
    """
    <script type="text/javascript">
    document.addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            document.querySelector('button[title="Search"]').click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)

if st.button("Search"):
    st.session_state['search_button'] = True

if st.session_state['search_button']:
    if medicine_name:
        # Using the model to find the closest match
        index = find_medicine(vectorizer, model, medicine_name)
        medicine_info = get_medicine_info(data, data.iloc[index]['name'])

        # Filter out empty and 0 values
        uses = [use for use in medicine_info['uses'] if use]
        side_effects = [se for se in medicine_info['side_effects'] if se]
        substitutes = [sub for sub in medicine_info['substitutes'] if sub]

        # Display data in separate boxes
        st.write(f"### Uses of {medicine_name.capitalize()}")
        if uses:
            st.markdown('<div class="info-box">' + ''.join(uses) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No uses found</div>', unsafe_allow_html=True)

        st.write(f"### Side Effects of {medicine_name.capitalize()}")
        if side_effects:
            st.markdown('<div class="info-box">' + ''.join(side_effects) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No side effects found</div>', unsafe_allow_html=True)

        st.write(f"### Substitutes for {medicine_name.capitalize()}")
        if substitutes:
            st.markdown('<div class="info-box">' + ''.join(substitutes) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">No substitutes found</div>', unsafe_allow_html=True)

        # Reset the search button state
        st.session_state['search_button'] = False
    else:
        st.write("Please enter a medicine name.")
