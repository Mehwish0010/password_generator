import streamlit as st
import random
import string

# ---- UI Enhancements ----
st.set_page_config(page_title="Password Generator", page_icon="🔑", layout="centered")

# Custom CSS for Styling
st.markdown("""
    <style>
        body {
            background-color: #0f172a;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
        }
        .password-box {
            font-size: 20px;
            font-weight: bold;
            background-color: #4f46e5;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            color: white;
            margin-top: 10px;
            overflow-x: auto;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            opacity: 0.7;
        }
        .copy-button {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }
        /* Style Buttons */
        .stButton>button {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            transition: 0.3s;
            border: none;
        }
        .stButton>button:hover {
            transform: scale(1.05);
        }
        .generate-button button {
            background-color: #2563eb;
            color: white;
        }
        .generate-button button:hover {
            background-color: #1d4ed8;
        }
        .download-button button {
            background-color: #16a34a;
            color: white;
        }
        .download-button button:hover {
            background-color: #15803d;
        }
        .regenerate-button button {
            background-color: #ea580c;
            color: white;
        }
        .regenerate-button button:hover {
            background-color: #c2410c;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Password Generation Function ----
def generate_password(length, use_digit, use_special):
    characters = string.ascii_letters  # Add letters
    if use_digit:
        characters += string.digits  # Add numbers
    if use_special:
        characters += string.punctuation  # Add special characters
    return ''.join(random.choice(characters) for _ in range(length))

# ---- Password Strength Checker ----
def check_strength(password):
    length = len(password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    if length >= 12 and has_digit and has_special:
        return "Strong"
    elif length >= 8 and (has_digit or has_special):
        return "Medium"
    else:
        return "Weak"

# ---- Password History ----
if "history" not in st.session_state:
    st.session_state.history = []

# ---- Main UI ----
st.title("Secure Password Generator")

length = st.slider("Select Password Length", min_value=6, max_value=32, value=12)
use_digits = st.checkbox("Include Digits")
use_special = st.checkbox("Include Special Characters")

password_placeholder = st.empty()  # Placeholder for the password
strength_placeholder = st.empty()  # Placeholder for strength indicator

# ---- Generate Password Button ----
col1, col2 = st.columns([3, 1])
with col1:
    generate = st.button("Generate Password", key="generate", help="Click to generate a strong password")
with col2:
    regenerate = st.button("Regenerate", key="regenerate", help="Click to regenerate another password")

if generate or regenerate:
    password = generate_password(length, use_digits, use_special)
    
    # Store password in session state history (keep last 5)
    st.session_state.history.insert(0, password)
    st.session_state.history = st.session_state.history[:5]
    
    password_placeholder.markdown(f'<div class="password-box">{password}</div>', unsafe_allow_html=True)
    strength_placeholder.write(f"**Strength:** {check_strength(password)}")

    # Save to session state for copy/download
    st.session_state.generated_password = password

# ---- Copy to Clipboard ----
if "generated_password" in st.session_state:
    st.text_input("Copy your password:", st.session_state.generated_password)

# ---- Download Password ----
st.markdown('<div class="download-button">', unsafe_allow_html=True)
if "generated_password" in st.session_state:
    st.download_button(
        label="Download Password",
        data=st.session_state.generated_password,
        file_name="password.txt",
        mime="text/plain"
        
    )
st.markdown('</div>', unsafe_allow_html=True)

# ---- Password History ----
if st.session_state.history:
    st.write("Password History (Last 5)")
    for idx, past_password in enumerate(st.session_state.history):
        st.code(past_password)

# ---- Footer ----
st.markdown('<p class="footer">Made by <b>Mehwish Fatima</b></p>', unsafe_allow_html=True)

