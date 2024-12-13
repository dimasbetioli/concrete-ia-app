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
    st.write("Preencha os valores de **x**, **y** e **z** abaixo. O aplicativo calculará automaticamente a soma.")

    # Número de linhas na tabela
    num_rows = st.number_input("Número de linhas:", min_value=1, max_value=20, value=1, step=1)

    # Criar DataFrame inicial
    data = {"x": [0] * num_rows, "y": [0] * num_rows, "z": [0] * num_rows, "Soma": [0] * num_rows}
    df = pd.DataFrame(data)

    # Entrada dinâmica de valores
    for i in range(num_rows):
        col1, col2, col3 = st.columns(3)
        with col1:
            df.at[i, "x"] = st.number_input(f"Valor x (Linha {i + 1}):", key=f"x_{i}")
        with col2:
            df.at[i, "y"] = st.number_input(f"Valor y (Linha {i + 1}):", key=f"y_{i}")
        with col3:
            df.at[i, "z"] = st.number_input(f"Valor z (Linha {i + 1}):", key=f"z_{i}")

    # Calcular soma
    df["Soma"] = df["x"] + df["y"] + df["z"]

    # Exibir resultados
    st.write("Tabela com os resultados:")
    st.dataframe(df)

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
