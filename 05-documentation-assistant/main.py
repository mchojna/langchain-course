from backend.core import run_llm
import streamlit as st
from typing import Set

def create_sources_string(sources: Set[str]) -> str:
    if not sources:
        return ""
    sources_list = list(sources)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        source = source.replace("data/", "")
        sources_string += f"{i+1}. {source} \n"
    return sources_string

st.header("LangChain documentation assistant")

prompt = st.text_input("Prompt", placeholder="Enter your prompt...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if prompt:
    with st.spinner("Generating response..."):
        response = run_llm(
            query=prompt,
            chat_history=st.session_state["chat_history"],
        )
        sources = set([doc.metadata["source"] for doc in response["context"]])

        formated_response = (
            f"{response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formated_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", response["answer"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_prompt in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"]
    ):
        st.chat_message("user").write(user_prompt)
        st.chat_message("assistant").write(generated_response)