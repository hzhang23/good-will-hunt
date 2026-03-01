import streamlit as st
import requests
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

# Configuration from secrets.toml
auth_secrets = st.secrets.get("auth", {})
google_secrets = auth_secrets.get("google", {})

CLIENT_ID = google_secrets.get("client_id")
CLIENT_SECRET = google_secrets.get("client_secret")
REDIRECT_URI = auth_secrets.get("redirect_uri")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
]

def login_user():
    """Generates the Google login URL and shows a link styled as a button."""
    scope_str = " ".join(SCOPES)
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope_str}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    # Styled HTML link to look like a Streamlit button but open in SAME tab
    button_html = f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; 
            color: white; 
            background-color: #FF4B4B; 
            padding: 0.5rem 1rem; 
            border-radius: 0.5rem; 
            display: inline-block;
            font-weight: 500;
            font-family: sans-serif;
        ">
            Log in with Google
        </a>
    """
    st.markdown(button_html, unsafe_allow_html=True)

def logout_user():
    for key in ["google_creds", "google_user"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def check_auth():
    """Manually handles the redirect 'code' exchange using requests."""
    if "google_creds" in st.session_state:
        return True

    # Check if we just returned from Google
    if "code" in st.query_params:
        code = st.query_params["code"]
        try:
            # Manual token exchange to bypass Flow object state issues
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            response = requests.post(token_url, data=data)
            token_data = response.json()
            
            if "error" in token_data:
                st.error(f"Login failed: {token_data.get('error_description', token_data['error'])}")
                return False

            # Create Credentials object
            creds = Credentials(
                token=token_data["access_token"],
                refresh_token=token_data.get("refresh_token"),
                token_uri=token_url,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                scopes=SCOPES
            )
            st.session_state["google_creds"] = creds
            
            # Fetch user info
            service = googleapiclient.discovery.build("oauth2", "v2", credentials=creds)
            user_info = service.userinfo().get().execute()
            st.session_state["google_user"] = user_info
            
            # Clear the code from URL
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")
    
    return False

def get_logged_in_user():
    return st.session_state.get("google_user")

def get_credentials():
    return st.session_state.get("google_creds")
