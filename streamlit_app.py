import streamlit as st
import pickle
import numpy as np
import pandas as pd
import joblib
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Previsão de Resistência do Concreto",
    page_icon="https://raw.githubusercontent.com/dimasbetioli/concrete-ia-app/refs/heads/main/mult3.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Adicionar imagem no topo da página
st.image(
    "https://raw.githubusercontent.com/dimasbetioli/concrete-ia-app/refs/heads/main/topo.png",
    use_container_width=True
)

# Título principal
st.markdown(
    "<h1 style='text-align: center; color: #2196F3; font-size: 18px;'> PROJETO - IA APLICADA À PREVISÃO DA RESISTÊNCIA DE CONCRETOS AOS 28 DIAS</h1>",
    unsafe_allow_html=True,
)

# Introdução
st.markdown(
    '<h3 style="text-align: center; color: #2C2C2C; font-size: 14px; margin-bottom: 20px;">Equipe liderada pelo Prof André C.P.F.L. de Carvalho</h3>',
    unsafe_allow_html=True,
)

# Opções de entrada: manual ou por arquivo
# Título informativo
st.markdown(
    """
    <p style="text-align: center; font-size: 16px; color: #2C2C2C;">
        <span style="font-size: 30px; color: #4CAF50;">&#8595;</span> Escolha se deseja inserir os dados manualmente ou carregar um arquivo Excel <span style="font-size: 30px; color: #4CAF50;">&#8595;</span>
    </p>
    """,
    unsafe_allow_html=True
)

# Inicializando o estado da escolha
if 'tipo_entrada' not in st.session_state:
    st.session_state.tipo_entrada = None

# Centralizar e exibir botões lado a lado
col1, col2 = st.columns(2)  # Criando duas colunas de igual largura para exibir os botões lado a lado

with col1:
    if st.button("Inserir manualmente"):
        st.session_state.tipo_entrada = "Inserir manualmente"

with col2:
    if st.button("Carregar arquivo Excel"):
        st.session_state.tipo_entrada = "Carregar arquivo Excel"

# Lógica condicional baseada na escolha do usuário
if st.session_state.tipo_entrada == "Inserir manualmente":
    st.write("Você escolheu inserir os dados manualmente.")

    # Opções de configuração
    opcao = st.radio(
        "Escolha a configuração de entrada:",
        [
            "CT_Cimento e CT_Agua",
            "CT_Cimento, CT_Agua, e resistências reais (3d, 7d, 28d)",
            "CT_Cimento, CT_Agua, resistências reais, e Fc_7d",
            "CT_Cimento, CT_Agua, resistências reais, Fc_7d, e aditivos",
            "Todas as variáveis"
        ]
    )

    entradas = []
    model_path = ""

    # Usando session_state para armazenar os valores dos inputs
    if 'entradas' not in st.session_state:
        st.session_state.entradas = []

    if opcao == "CT_Cimento e CT_Agua":
        model_path = "modelo1.pkl"
        st.session_state.entradas = [
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0, key="ct_cimento"),
            st.number_input("CT_Agua (kg/m³):", min_value=0.0, step=1.0, key="ct_agua")
        ]
    
    elif opcao == "CT_Cimento, CT_Agua, e resistências reais (3d, 7d, 28d)":
        model_path = "modelo2.pkl"
        st.session_state.entradas = [
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0, key="ct_cimento"),
            st.number_input("CT_Agua (kg/m³):", min_value=0.0, step=1.0, key="ct_agua"),
            st.number_input("cimento_Resistencia_real_3d (MPa):", min_value=0.0, step=1.0, key="resistencia_3d"),
            st.number_input("cimento_Resistencia_real_7d (MPa):", min_value=0.0, step=1.0, key="resistencia_7d"),
            st.number_input("cimento_Resistencia_real_28d (MPa):", min_value=0.0, step=1.0, key="resistencia_28d")
        ]
    
    elif opcao == "CT_Cimento, CT_Agua, resistências reais, e Fc_7d":
        model_path = "modelo3.pkl"
        st.session_state.entradas = [
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0, key="ct_cimento"),
            st.number_input("CT_Agua (kg/m³):", min_value=0.0, step=1.0, key="ct_agua"),
            st.number_input("cimento_Resistencia_real_3d (MPa):", min_value=0.0, step=1.0, key="resistencia_3d"),
            st.number_input("cimento_Resistencia_real_7d (MPa):", min_value=0.0, step=1.0, key="resistencia_7d"),
            st.number_input("cimento_Resistencia_real_28d (MPa):", min_value=0.0, step=1.0, key="resistencia_28d"),
            st.number_input("Fc_7d (MPa):", min_value=0.0, step=1.0, key="fc_7d")
        ]
    
    elif opcao == "CT_Cimento, CT_Agua, resistências reais, Fc_7d, e aditivos":
        model_path = "modelo4.pkl"
        st.session_state.entradas = [
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0, key="ct_cimento"),
            st.number_input("CT_Agua (kg/m³):", min_value=0.0, step=1.0, key="ct_agua"),
            st.number_input("cimento_Resistencia_real_3d (MPa):", min_value=0.0, step=1.0, key="resistencia_3d"),
            st.number_input("cimento_Resistencia_real_7d (MPa):", min_value=0.0, step=1.0, key="resistencia_7d"),
            st.number_input("cimento_Resistencia_real_28d (MPa):", min_value=0.0, step=1.0, key="resistencia_28d"),
            st.number_input("Fc_7d (MPa):", min_value=0.0, step=1.0, key="fc_7d"),
            st.number_input("CT_Silica (kg/m³):", min_value=0.0, step=1.0, key="ct_silica"),
            st.number_input("CT_Plastificante (kg/m³):", min_value=0.0, step=1.0, key="ct_plastificante")
        ]

    # Botão para calcular
    if st.button("Calcular Resistência"):
        if all(v > 0 for v in st.session_state.entradas):
            try:
                model = joblib.load(model_path)
                entrada = np.array([st.session_state.entradas])
                resistencia_28d = model.predict(entrada)[0]
                st.success(f"A resistência prevista do concreto aos 28 dias é: **{resistencia_28d:.2f} MPa**")
            except Exception as e:
                st.error(f"Erro ao carregar o modelo ou realizar a predição: {e}")
        else:
            st.error("Por favor, insira valores válidos para todas as variáveis.")

elif st.session_state.tipo_entrada == "Carregar arquivo Excel":
    st.write("Aqui você pode carregar um arquivo Excel para fazer a previsão.")
    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Processamento do arquivo Excel
        df = pd.read_excel(uploaded_file)
        st.write(df.head())  # Exibe as primeiras linhas do DataFrame para visualização

        if st.button("Fazer previsão com o Excel"):
            try:
                # Supondo que o modelo já foi carregado previamente
                model = joblib.load("modelo_geral.pkl")
                # Extrair dados relevantes do Excel para fazer a previsão
                input_data = df.iloc[:, :-1].values  # Supondo que a última coluna é a variável alvo
                previsoes = model.predict(input_data)
                st.write(f"Previsões: {previsoes}")
            except Exception as e:
                st.error(f"Erro ao realizar a previsão: {e}")
