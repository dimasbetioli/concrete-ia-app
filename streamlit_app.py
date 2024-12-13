import streamlit as st
import pandas as pd

# Título do aplicativo
st.title("Calculadora de Soma 🎉")

# Número de linhas na tabela
num_rows = st.number_input("Número de linhas:", min_value=1, max_value=20, value=1, step=1)

# Criar dataframe inicial
data = {"x": [0] * num_rows, "y": [0] * num_rows, "z": [0] * num_rows}
df = pd.DataFrame(data)

# Receber inputs para cada linha
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

# Exibir tabela com resultados
st.write("Tabela com os resultados:")
st.dataframe(df)
