
import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change as needed
st.set_page_config(page_title="RAG")
st.title('RAG Assistant !!')

st.markdown("""
    <style>
    /* Hide the file type text */
    div[data-testid="stFileUploader"] section div:nth-child(2) {
        display: none;
    }

    /* Remove outer border, padding, and background */
    div[data-testid="stFileUploader"] {
        border: none;
        padding: 0;
        background: transparent;
    }

    /* Style the Browse files button */
    div[data-testid="stFileUploader"] section div div {
        background-color: #4CAF50; /* green */
        color: white;
        border-radius: 8px;
        border: none !important;
        padding: 6px 16px;
        font-size: 14px;
        cursor: pointer;
    }

    /* Remove the big drop area effect */
    div[data-testid="stFileUploader"] section {
        padding: 0;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    
    st.header("Upload Document")
    uploaded_file = st.file_uploader(
        label="Choose a file",
        type=["pdf", "txt", "csv", "docx", "jpg", "jpeg", "png", "db"],
        key="file_upload"
    )

    model_name = st.selectbox(
        "Select Model",
        options=["Gemini", "GPT"],
        key="model_select"
    )
    

    if st.button("Upload", key="upload_btn", icon='🗃️') and uploaded_file is not None:
        with st.spinner("Uploading and processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            params = {"model_name": model_name}
            try:
                response = requests.post(f"{API_URL}/upload", files=files, params=params)
                response.raise_for_status()
                data = response.json()
                st.success('Data uploaded sucessfully')
                #st.success(f"Uploaded: {uploaded_file.name}")
                #st.write(f"Chunks created: {data.get('chunks', '?')}")
            except Exception as e:
                st.error(f"Upload failed: {e}")
    if st.button("Delete Files", key="delete_files_btn",type='primary'):
        with st.spinner("Deleting files..."):
            response = requests.post(f"{API_URL}/delete_files", json={"model_name": model_name})
            response.raise_for_status()  # will raise if error
            st.markdown(
                """
                <div style="white-space: normal; word-wrap: break-word; max-width: 100%;">
                    <p style="color: #28a745; font-weight: 600;">Files deleted successfully!</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
question = st.chat_input("How can i help you...", key="question_input")

if 'user_queries' not in st.session_state:
    st.session_state['user_queries'] = []
if 'answers' not in st.session_state:
    st.session_state['answers'] = []

if question:
    with st.spinner("Getting answer..."):
        payload = {"question": question}
        params = {"model_name": model_name}
        try:
            response = requests.post(f"{API_URL}/query", json=payload, params=params)
            response.raise_for_status()
            answer = response.json().get("answer", "")
            st.session_state['user_queries'].append(question)
            st.session_state['answers'].append(answer)
        except Exception as e:
            st.error(f"Query failed: {e}")

if st.session_state['user_queries']:
    for i in range(len(st.session_state['user_queries'])):
        st.chat_message("user").write(st.session_state['user_queries'][i])
        st.chat_message("assistant").write(st.session_state['answers'][i])
