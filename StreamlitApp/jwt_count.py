import base64
import hashlib
import hmac
import json
import streamlit as st

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def generate_jwt(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}

    h = b64url(json.dumps(header, separators=(",", ":")).encode())
    p = b64url(json.dumps(payload, separators=(",", ":")).encode())

    signing_input = f"{h}.{p}"
    sig = hmac.new(
        secret.encode(),         
        signing_input.encode(),
        hashlib.sha256,
    ).digest()                       

    return f"{signing_input}.{b64url(sig)}"

def jwt_token():
    st.title('Generate JWT')
    if st.button('Back', width='stretch'):
        st.session_state.page = 'home'
        st.rerun()
    st.divider()
    with st.container(horizontal=True):
        st.text_input('Partner ID:', placeholder='Input your partner ID here...', key='partner_id')
        st.text_input('Secret Key:', placeholder='Input client secret key here...', key='secret')

    if st.session_state.partner_id and st.session_state.secret:
        st.code(generate_jwt({"clientId": st.session_state.partner_id}, st.session_state.secret))
