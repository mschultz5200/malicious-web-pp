import streamlit as st
from current_scripts.complete import predict_malicious
import pandas as pd

def predict(api, wallet):
    if st.session_state.api == '' or st.session_state.wallet == '':
        return 'Please Enter a Valid API Key or Wallet'
    if '0x' not in st.session_state.wallet:
        return 'Please Enter A Valid Ethereum Wallet'
    else:
        results = predict_malicious(api, wallet)
        return results

st.write('''
# Tracking Malicious Transactions on the Ethereum Transactions
''')

st.text_input("Wallet Address", 
              key="wallet",
              placeholder="Enter Wallet Here: 0x...")
st.text_input("Moralis API Key", 
              key="api",
              placeholder='Enter Moralis API Here')

st.button('Submit', 'submit')

st.write(predict(st.session_state.api, st.session_state.wallet))

