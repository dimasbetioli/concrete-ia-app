import streamlit as st
import pickle
import numpy as np
import joblib

# Configuração da página
st.set_page_config(
    page_title="Previsão de Resistência do Concreto",
    page_icon="🧱",
    layout="centered",
    initial_sidebar_state="expanded"
)

model = joblib.load("HistGB.pkl")

# Título principal
st.markdown(
    "<h1 style='text-align: center; color: #2196F3;'>🧱 Previsão da Resistência do Concreto aos 28 Dias</h1>",
    unsafe_allow_html=True,
)

# Caixa de introdução
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="text-align: center; color: #FF5722;">Digite os valores de CT_Cimento e CT_Agua para calcular a resistência do concreto aos 28 dias.</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Entradas do usuário
col1, col2 = st.columns(2)
with col1:
    ct_cimento = st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0)
with col2:
    ct_agua = st.number_input("CT_Agua (kg/m³):", min_value=0.0, step=1.0)

# Botão para calcular
if st.button("Calcular Resistência"):
    if ct_cimento > 0 and ct_agua > 0:
        # Criar array de entrada para o modelo
        entrada = np.array([[ct_cimento, ct_agua]])
        
        # Fazer previsão com o modelo
        resistencia_28d = model.predict(entrada)[0]
        
        # Exibir resultado
        st.success(f"A resistência prevista do concreto aos 28 dias é: **{resistencia_28d:.2f} MPa**")
    else:
        st.error("Por favor, insira valores válidos para CT_Cimento e CT_Agua.")

# Footer
st.markdown(
    """
    <footer style="text-align: center; margin-top: 20px;">
        <small>Projeto Embrapii | USP | ITA</small>
    </footer>
    """,
    unsafe_allow_html=True,
)
