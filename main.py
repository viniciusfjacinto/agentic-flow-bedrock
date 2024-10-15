import streamlit as st
from utils import invoke_flow

# Set up the Streamlit interface
st.title("Assistente virtual")
st.write("Um aplicativo para que professores visualizem dados de suas turmas e alunos")

# Text input for the user query
user_input = st.text_area("Digite sua questão:", "")

# Create a submit button
if st.button("Submit"):
    if user_input.strip() == "":
        st.write("Por favor faça uma pergunta válida.")
    else:
        # Call the invoke_flow function from utils.py
        with st.spinner("Aguardando resposta do Assistente..."):
            response = invoke_flow(user_input)
        
        # Display the response
        if response:
            st.write("### Resposta do Assistente:")
            st.write(response)
        else:
            st.write("Ops. Parece que algo deu errado. Tente novamente mais tarde")
