
import streamlit as st
import streamlit_authenticator as stauth
from settings import LOGIN_CREDENTIALS


def authentication(func):
    """
    decorator to check if the user is authenticated.
    """
    names = [LOGIN_CREDENTIALS.get('names')]
    usernames = [LOGIN_CREDENTIALS.get('usernames')]
    passwords = [LOGIN_CREDENTIALS.get('passwords')]
    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)


    name, authentication_status, username = authenticator.login('Login', 'sidebar')


    def wrapper(*args, **kwargs):

        if st.session_state['authentication_status'] is True:
            authenticator.logout('Logout', 'sidebar')
            func()

        elif st.session_state['authentication_status'] is False:
            st.error('Username/password is incorrect')

        elif st.session_state['authentication_status'] is None:
            st.warning('Please enter your username and password')

    return wrapper
