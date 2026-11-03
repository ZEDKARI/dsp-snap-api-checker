import streamlit as st
from api import api
from disbursement import disbursement

if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.set_page_config(
    layout='wide',
    page_title="API Checker",
    page_icon="🔥",  # emoji
)

if st.session_state.page == 'home':
    st.title('HOME')    

    if st.button('API', width='stretch'):
        st.session_state.page = 'api'
        st.rerun()
    
    if st.button('Disbursement', width='stretch'):
        st.session_state.page = 'disbursement'
        st.rerun()


if st.session_state.page == 'api':
    api()
    
if st.session_state.page == 'disbursement':
    disbursement()
    