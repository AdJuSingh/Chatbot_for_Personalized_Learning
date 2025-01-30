import sqlite3


def initialize_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()

    # Create the table only if it doesn’t exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        feedback TEXT NOT NULL,
        user_suggestion TEXT
    );
    ''')

    conn.commit()
    conn.close()


# Run this at the start of your app
initialize_db()

import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
# from botocore.endpoint import history_recorder

st.set_page_config(page_title="Rasa Chatbot",
                   page_icon=":alien:",
                   layout="wide",
                   initial_sidebar_state="collapsed") # Options: "auto", "expanded", "collapsed")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# -- load assets---
lottie_coding = load_lottieurl("https://lottie.host/6a2bfd58-39f4-4c42-af27-4f6704cc9f01/W4K91PVZ2U.json")



# --header--
left_column, right_column = st.columns(2)
with left_column:
    st.title("Rasa Chatbot")
    st.subheader("I am an Educational Chatbot")
with right_column:
    st_lottie(lottie_coding, height=200, key="educational")

#---sidebar---
with st.sidebar:
    st.link_button("New Chat", url="http://localhost:8501", )
    st.title("✨ Special Features of the Personalized Learning Chatbot ✨")
    with st.container():
        st.markdown("""
    1. 🌟 **Topic-Based Dynamic Responses**  
       The chatbot provides detailed explanations and insights on a wide range of topics tailored to the user's queries.

    2. 🎯 **Personalized Learning Recommendations**  
       Suggests videos, books, and courses based on the user's interests and learning needs.

    3. 🌐 **Course Integration with APIs**  
       Fetches course details from platforms to recommend relevant learning materials.

    4. 🎨 **Engaging UI with LottieFiles**  
       Incorporates interactive animations to create an appealing and user-friendly interface.

    5. 💡 **Motivational Content and Study Tips**  
       Offers personalized study advice and motivational support to enhance the learning experience.

    6. 📨 **Seamless Feedback Collection with FormSubmit**  
       Allows users to provide feedback easily, ensuring continuous improvement of the chatbot.

    7. 🚀 **Streamlit-Powered Interactive Frontend**  
       Combines Rasa's robust conversational AI with Streamlit's simple and intuitive UI framework.
    """)



# Create a container for the chat interface
with st.container():
    # messages = st.container(height=500)
    chat_container = st.container(height=400, key="chat")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add chat messages to the container
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Inject custom CSS to style the chat input
    st.markdown(
        """
        <style>
        /* Style the chat input box */
        div[data-testid="stChatInput"] textarea {
            font-size: 20px; /* Change font size */
            color: #00000; /* Change text color */
            background-color: white !important;
            text-border: 1px solid black;
        }

        /* Optional: Style the placeholder text */
        div[data-testid="stChatInput"] textarea::placeholder {
            font-size: 20px; /* Change placeholder font size */
            color: black; /* Change placeholder text color */
            background-color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Chat input widget
    if user_input := st.chat_input("Type your message here..."):
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": user_input}
        )

        # Add user input to the chat container
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)

        # Update session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate assistant's response (replace with actual logic)
        assistant_response = f"{user_input}"

        # Add assistant message to chat container
        with chat_container:
            with st.chat_message("assistant"):
                assistant_response = "\n\n".join(
                    msg['text'] for msg in response.json())  # Combine messages into one response
                st.text_area("Bot:", value=assistant_response, height=150)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})


# use local css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)
local_css("style/style.css")


def save_feedback(feedback, user_suggestion):
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO feedback (feedback, user_suggestion) VALUES (?, ?);
    ''', (feedback, user_suggestion))

    conn.commit()
    conn.close()


# Create a container for the feedback buttons corner
st.markdown("""
    <style>
    .feedback-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        z-index: 100;
    }
    .feedback-button {
        background-color: #ff9a9e;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        cursor: pointer;
        font-weight: bold;
        font-size: 18px;
        color: white;
        transition: background-color 0.3s;
    }
    .feedback-button:hover {
        background-color: #ff5e62;
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar dropdown menu for topic selection
topic = st.sidebar.selectbox(
    "Select a topic to get book recommendations:",
    ["Select a topic", "AI", "Machine Learning", "Deep Learning", "Data Science", "NLP"]
)

import streamlit as st

# User suggestion input
user_suggestion = st.text_area("Enter your suggestion (optional):")

with st.container():
    st.markdown('<div class="feedback-container">', unsafe_allow_html=True)

    if st.button("👍", key="positive_feedback", help="Thumbs Up - Positive Feedback"):
        save_feedback("positive", user_suggestion)
        st.write("Thank you for your positive feedback!")

    if st.button("👎", key="negative_feedback", help="Thumbs Down - Negative Feedback"):
        save_feedback("negative", user_suggestion)
        st.write("Sorry to hear that! We appreciate your feedback.")

    st.markdown('</div>', unsafe_allow_html=True)


# Dictionary with book recommendations for each topic
book_recommendations = {
    "AI": [
        "1. Artificial Intelligence: A Modern Approach by Stuart Russell and Peter Norvig",
        "2. Superintelligence: Paths, Dangers, Strategies by Nick Bostrom",
        "3. The Age of Em: Work, Love, and Life when Robots Rule the Earth by Robin Hanson"
    ],
    "Machine Learning": [
        "1. Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow by Aurélien Géron",
        "2. Pattern Recognition and Machine Learning by Christopher Bishop",
        "3. Machine Learning Yearning by Andrew Ng"
    ],
    "Deep Learning": [
        "1. Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron Courville",
        "2. Neural Networks and Deep Learning by Michael Nielsen",
        "3. Deep Reinforcement Learning Hands-On by Maxim Lapan"
    ],
    "Data Science": [
        "1. Data Science for Business by Foster Provost and Tom Fawcett",
        "2. Python Data Science Handbook by Jake VanderPlas",
        "3. Practical Data Science with R by Nina Zumel and John Mount"
    ],
    "NLP": [
        "1. Speech and Language Processing by Daniel Jurafsky and James H. Martin",
        "2. Natural Language Processing with Python by Steven Bird, Ewan Klein, and Edward Loper",
        "3. Transformers for Natural Language Processing by Denis Rothman"
    ]
}

# Display book recommendations based on the selected topic in the sidebar
if topic != "Select a topic":
    st.sidebar.write(f"### Book Recommendations for {topic}:")
    for book in book_recommendations.get(topic, []):
        st.sidebar.write(book)


