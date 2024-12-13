import streamlit as st
import pandas as pd

# Título do aplicativo
st.title("Calculadora de Soma 🎉")

# Instruções
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
