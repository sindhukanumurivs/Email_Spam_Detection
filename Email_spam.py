import streamlit as st
import time
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download nltk resources
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# Load model and vectorizer
vkl = pickle.load(open(r'C:\Users\sindh\OneDrive\Desktop\thonny\vectorizer.pkl', 'rb'))
model = pickle.load(open(r'C:\Users\sindh\Downloads\model.pkl', 'rb'))

# Page Layout
st.set_page_config(
    page_title="Email spam dectector",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Navigation Bar
st.markdown(
    """
    <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background-color: #FFFFFF;
            color: white;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 999;
        }
        .navbar-brand {
            font-size: 1.5rem;
            margin: 0;
            padding: 0;
        }
        .navbar-brand a {
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
        }
        .navbar a:hover {
            background-color: #555555;
        }
        @media only screen and (max-width: 600px) {
            .navbar {
                flex-direction: column;
                align-items: flex-start;
            }
            .navbar a {
                padding: 0.5rem;
            }
            .navbar-brand {
                margin-bottom: 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="navbar">
        <div class="navbar-brand">
            <h2 style="margin-right: 1rem; line-height:1.6;">Email Spam Detector !!</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Main Content
input_sms = st.text_area("Enter email content here...")

if st.button('Predict'):
    # Check if input is empty
    if input_sms.strip() == "":
        st.warning("Please enter a message to predict.")
    else:
        # Show loading spinner
        with st.spinner('Predicting...'):
            time.sleep(3)  # Simulate prediction time
            # 1. Preprocess
            transformed_sms = transform_text(input_sms)
            # 2. Vectorize
            vector_input = vkl.transform([transformed_sms])
            # 3. Predict
            result = model.predict(vector_input)[0]
            # 4. Display
            if result == 1:
                st.header("⚠️ ALERT!! SPAM")
            else:
                st.header("RELAX!! NOT A SPAM")
