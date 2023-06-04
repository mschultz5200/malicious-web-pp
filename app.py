import streamlit as st
from current_scripts.complete import predict_malicious
import pandas as pd


st.write('''
# Tracking Malicious Transactions on the Ethereum Transactions
''')

st.text_input("Wallet Address", key="wallet")
st.text_input("Moralis API Key", key="key")

st.button('Submit', 'submit')

def predict():
    results = predict_malicious(st.session_state.api, st.session_state.wallet)