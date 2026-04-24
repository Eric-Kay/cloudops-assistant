import streamlit as st
import requests

API_BASE = "http://cloudops-assistant-1285171244.us-east-1.elb.amazonaws.com/api"

st.set_page_config(page_title="CloudOps Assistant", layout="wide")
st.title("CloudOps Assistant")

if "token" not in st.session_state:
    st.session_state.token = None

with st.sidebar:
    st.header("Login")
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", type="password", value="admin123")

    if st.button("Login"):
        response = requests.post(
            f"{API_BASE}/login",
            json={"username": username, "password": password},
            timeout=30,
        )
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.success("Logged in")
        else:
            st.error(response.text)

st.subheader("Upload document")
uploaded_file = st.file_uploader("Choose a .txt, .md, or .log file")

if uploaded_file and st.session_state.token:
    if st.button("Upload"):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            f"{API_BASE}/upload",
            files=files,
            headers=headers,
            timeout=60,
        )
        st.write(response.json())

st.subheader("Ask a question")
question = st.text_area("Question", height=120)

if st.button("Ask") and question and st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.post(
        f"{API_BASE}/chat",
        json={"question": question},
        headers=headers,
        timeout=60,
    )
    result = response.json()
    st.write("### Answer")
    st.write(result.get("answer"))

    st.write("### Sources")
    for source in result.get("sources", []):
        st.write(f"**{source['filename']}**")
        st.code(source["snippet"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👍 {source['filename']}"):
                feedback_response = requests.post(
                    f"{API_BASE}/feedback",
                    json={
                        "question": question,
                        "answer": result.get("answer", ""),
                        "rating": "up",
                    },
                    headers=headers,
                    timeout=30,
                )
                st.write(feedback_response.json())
        with col2:
            if st.button(f"👎 {source['filename']}"):
                feedback_response = requests.post(
                    f"{API_BASE}/feedback",
                    json={
                        "question": question,
                        "answer": result.get("answer", ""),
                        "rating": "down",
                    },
                    headers=headers,
                    timeout=30,
                )
                st.write(feedback_response.json())