import streamlit as st
import pandas as pd
from util import load_data, preprocess_data, get_medicine_info, set_background
from model import train_model, find_medicine
from PIL import Image
import base64


#setting up the logo
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string
# Set background image
set_background('dr_penguin4.gif')
# Get base64 string for logo
logo_base64 = get_base64_image('45.png')
# Load and preprocess data
data_file = 'medicine_dataset.csv'
data = load_data(data_file)
data = preprocess_data(data)

# Train model
vectorizer, model = train_model(data)




# Custom CSS for background and styling
st.markdown(
    """
    <style>

    .logo-container {
        position: flex;
        top: 5px;
        left: 2px;
        margin-top: 20px;
        z-index: 1;
    }
    .logo-container img {
        height: 100px;
        width: 100px;
        border-radius: 50px;
        border: 2px solid skyblue;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <header>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo">
    </div>
    </header>
    """,
    unsafe_allow_html=True
)
st.markdown(
     """
    <style>
    .main {
        background:babypink;
        background-image: url('data:image/gif;base64,{}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh; /* Full viewport height */
    }
    h1 {
        color: #4CAF50;
        text-align: center;
        animation: fadeIn 2s;
    }
    .stButton button {
        background-color:white;
        color: black;
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
    footer {
    background: transparent;
    color: #fc9d03;
    padding: 20px 0;
    text-align: center;
    animation: fadeIn 2s ease-out;
}
.social-icons a {
    color: blue;
    margin: 0 10px;
    font-size: 1.5em;
    transition: color 0.3s;
}
.social-icons a:hover {
    color: #ff5722; /* Change color on hover */
}


    .warning {
        color: #FF4500; /* Neon orange */
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        background-color: transparent; /* Slightly transparent background */
        border-radius: 0px;
        box-shadow: none;
        animation: blink 2s infinite;
    }

    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
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
medicine_name = st.text_input("Enter the name of the medicine:",placeholder='Enter the proper medicine name')

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

if st.button("Search", key="search_button_id"):
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
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"
        integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A=="
        crossorigin="anonymous" referrerpolicy="no-referrer" />
    """,
    unsafe_allow_html=True
)
#IMPORTANT NOTICE 
st.markdown('<div class="warning">IT WILL ANALYZING WITH AI.IN ANY EMERGENCY CONDITION CONSULT WITH A DOCTOR.BEFORE TAKING SUBSTITUTE MEDICINE CONSULT WITH A DOCTOR.</div>', unsafe_allow_html=True)
        # Footer
st.markdown(
    """
    <footer>
        <div class="contain">
            <p class="animated-text">&copy; 2024 <a href="https://soumya-xd.github.io/Redalpha/" target="_blank">RedAlpha</a> Team. All rights reserved.</p>
            <div class="social-icons">
                <a href="https://www.facebook.com/soumya.singharoy.98" target="_blank"><i class="fab fa-facebook-f"></i></a>
                <a href="https://x.com/Soumya413876651" target="_blank" target="_blank"><i class="fab fa-twitter"></i></a>
                <a href="https://www.instagram.com/soumya_xd7/" target="_blank" target="_blank"><i class="fab fa-instagram"></i></a>
                <a href="https://www.linkedin.com/in/soumya-singha-roy-a20880261/" target="_blank"><i class="fab fa-linkedin"></i></a>
            </div>
        </div>
    </footer>
    """,
    unsafe_allow_html=True
)
