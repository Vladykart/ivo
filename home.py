import streamlit as st
import streamlit_authenticator as stauth
from st_auth import authentication

st.set_page_config(page_title="Housewears", layout="wide")
st._config.set_option('theme.base', 'dark')


@authentication
def app():
    st.markdown("# Home")
    st.sidebar.markdown("# Home")


app()