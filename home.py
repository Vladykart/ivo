import streamlit as st
import streamlit_authenticator as stauth
from st_auth import authentication
import json
st.set_page_config(page_title="Housewears", layout="wide")
st._config.set_option('theme.base', 'dark')


@authentication
def app():
    st.markdown("# Home")
    st.sidebar.markdown("# Home")
    # upload googleanalytics key file
    key_file = st.file_uploader("Upload Google Analytics Key File", type="json")
    # key file to session state
    if key_file is not None:
        st.session_state.key_file = key_file



app()