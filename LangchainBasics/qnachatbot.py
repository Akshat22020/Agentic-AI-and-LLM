"""
Simple LangChain Streamlit app with Groq
A beginner-friendly version focusing on core concepts

"""
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os


##page config for streamlit
st.set_page_config(page_title="Odi-Bot",page_icon="👾->🤖->🧠")


##Title
st.title("🤖Odi-Bot")
st.markdown("Welcome to my very own Chatbot")



with st.sidebar:
    st.header("Settings")
    
    ## API key text Input
    api_key=st.text_input("GROQ API KEY",type="password",help="Get Free API Key at console.groq.com").strip()
    
    ##Model selection
    model_name=st.selectbox(
        "Model",
        [
           "llama-3.1-8b-instant",
           "meta-llama/llama-4-scout-17b-16e-instruct" ,
           "llama-3.3-70b-versatile",
           "gemma2-9b-it"
        ],
        index=0
    )
    
    ##making clear button
    if st.button("Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

##initialize chat history
if"messages" not in st.session_state:
    st.session_state.messages=[]
    
##Initialize LLM
# @st.cache_resource
def get_chain(api_key , model_name):
    if not api_key:
        return None
    ## Initialize groq model
    llm=ChatGroq(groq_api_key=api_key,
             model_name=model_name,
             temperature =0.7,
             streaming=True)
    
    # Create prompt tempelate
    prompt=ChatPromptTemplate.from_messages([
        ("system", "You are a helpful friend-assistant who is powered by groq and works for akshat , answer the questions clearly and concisely"),
        ("user","{question}")
    ])
    
    ##create chain
    chain=prompt | llm | StrOutputParser()
    
    return chain

##get chain
chain=get_chain(api_key,model_name)

if not chain:
    st.warning("Please enter the API key")
    st.markdown("[Get your free API key here](https://console.groq.com)")
else:
    ##display the chat messages
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    ##Chat Input
    if question:=st.chat_input("Ask me anything"):
        ##add user method to session state
        st.session_state.messages.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)
            
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Stream response from Groq
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

## Examples

st.markdown("---")
st.markdown("### 💡 Try these examples:")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- What is LangChain?")
    st.markdown("- Explain Groq's LPU technology")
with col2:
    st.markdown("- How do I learn programming?")
    st.markdown("- Write a haiku about AI")
    
api_key = st.text_input(
    "GROQ API KEY",
    type="password"
).strip()

st.write("Key loaded:", bool(api_key))
st.write("Prefix:", api_key[:4] if api_key else "NONE")
st.write("Length:", len(api_key))

# Footer
st.markdown("---")
st.markdown("Built with LangChain & Groq | Experience the speed! ⚡")
