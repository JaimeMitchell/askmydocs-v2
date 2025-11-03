
import streamlit as st
import requests

st.title("AskMyDocs v2 Chat")
st.subheader("Powered by BLOOMZ 3B 🤖")

query = st.text_input("Enter your question:")
if st.button("Ask"):
    try:
        resp = requests.post("http://localhost:8000/ask", data={"query": query})
        st.write(resp.json()["answer"])
    except Exception as e:
        st.write("Error contacting API:", e)
