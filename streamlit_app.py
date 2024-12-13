import streamlit as st
import pandas as pd

# Configurações de usuários e senhas (dados fixos no código)
USER_CREDENTIALS = {
    "cliente1": "senha123",
    "cliente2": "senha456"
}

# Função de tela de login
def login():
    st.title("Login 🔒")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Usuário ou senha incorretos. Tente novamente!")

# Função da calculadora de soma
def main_app():
    st.title("Calculadora de Soma 🎉")
    st.write(f"Olá, **{st.session_state['username']}**! Bem-vindo ao aplicativo.")
    st.write("Preencha os valores de **x**, **y** e **z** na tabela abaixo. O aplicativo calculará automaticamente a soma.")

    # Dados iniciais para a tabela
    data = {
        "x": [0],
        "y": [0],
        "z": [0],
        "Soma": [0],  # Coluna para exibir o resultado
    }

    # Criação de um DataFrame com os dados iniciais
    df = pd.DataFrame(data)

    # Exibe a tabela editável
    edited_df = st.experimental_data_editor(df, num_rows="dynamic", key="data_editor")

    # Calcula a soma para cada linha
    if edited_df is not None:
        edited_df["Soma"] = edited_df["x"] + edited_df["y"] + edited_df["z"]

        # Mostra a tabela com as somas atualizadas
        st.write("Tabela com os resultados:")
        st.dataframe(edited_df)

    # Botão para logout
    if st.button("Logout"):
        st.session_state["logged_in"] = False

# Controle de autenticação
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    main_app()
