import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    html, body, [class*="css"] {
        background-color: #0e1117;
        color: white;
        font-family: 'Inter', sans-serif;
    }

    .card {
        background: #161b22;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.4);
    }

    .kpi {
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50;
    }

    </style>
    """, unsafe_allow_html=True)
