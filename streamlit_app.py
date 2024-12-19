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
    "<h1 style='text-align: center; color: #2196F3;'> Previsão da Resistência do Concreto aos 28 Dias</h1>",
    unsafe_allow_html=True,
)

# Introdução
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="text-align: center; color: #FF5722;">Escolha o conjunto de variáveis para calcular a resistência do concreto aos 28 dias.</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Opções de entrada: manual ou por arquivo
tipo_entrada = st.radio(
    "Como você gostaria de fornecer os dados?",
    ["Inserir manualmente", "Carregar arquivo Excel"]
)

if tipo_entrada == "Inserir manualmente":
    # Opções de configuração
    opcao = st.radio(
        "Escolha a configuração de entrada:",
        [
            "CT_Cimento e CT_Água",
            "CT_Cimento, CT_Água, e resistências reais (3d, 7d, 28d)",
            "CT_Cimento, CT_Água, resistências reais, e Fc_7d",
            "CT_Cimento, CT_Água, resistências reais, Fc_7d, e aditivos",
            "Todas as variáveis"
        ]
    )

    entradas = []
    model_path = ""

    if opcao == "CT_Cimento e CT_Água":
        model_path = "modelo1.pkl"
        entradas.append(st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0))
        entradas.append(st.number_input("CT_Água (kg/m³):", min_value=0.0, step=1.0))
    
    elif opcao == "CT_Cimento, CT_Água, e resistências reais (3d, 7d, 28d)":
        model_path = "modelo2.pkl"
        entradas.extend([
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Água (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 3d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 7d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 28d (MPa):", min_value=0.0, step=1.0),
        ])
    
    elif opcao == "CT_Cimento, CT_Água, resistências reais, e Fc_7d":
        model_path = "modelo3.pkl"
        entradas.extend([
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Água (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 3d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 7d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 28d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Fc 7d (MPa):", min_value=0.0, step=1.0),
        ])
    
    elif opcao == "CT_Cimento, CT_Água, resistências reais, Fc_7d, e aditivos":
        model_path = "modelo4.pkl"
        entradas.extend([
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Água (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 3d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 7d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 28d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Fc 7d (MPa):", min_value=0.0, step=1.0),
            st.number_input("CT_Sílica (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Plastificante (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Polifuncional (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Superplastificante (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Brita_0 (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Brita_1 (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Areia_natural (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Areia_artificial (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_AC (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Aditivo (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Teor_de_Argamassa (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Teor_de_Agua (kg/m³):", min_value=0.0, step=1.0),
        ])
    
    elif opcao == "Todas as variáveis":
        model_path = "modelo5.pkl"
        entradas.extend([
            st.number_input("CT_Cimento (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Água (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 3d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 7d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Cimento resistência real 28d (MPa):", min_value=0.0, step=1.0),
            st.number_input("Fc 7d (MPa):", min_value=0.0, step=1.0),
            st.number_input("CT_Sílica (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Plastificante (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Polifuncional (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Superplastificante (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Brita_0 (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Brita_1 (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Areia_natural (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Areia_artificial (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_AC (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Aditivo (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Teor_de_Argamassa (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("CT_Teor_de_Agua (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Volume (m³):", min_value=0.0, step=1.0),
            st.number_input("Mesp_Brita_0 (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Mesp_Brita_1 (kg/m³):", min_value=0.0, step=1.0),
            st.number_input("Tempo_de_transporte (s):", min_value=0.0, step=1.0),
            st.number_input("Slump (cm):", min_value=0.0, step=1.0),
        ])

    # Botão para calcular
    if st.button("Calcular Resistência"):
        if all(v > 0 for v in entradas):
            try:
                model = joblib.load(model_path)
                entrada = np.array([entradas])
                resistencia_28d = model.predict(entrada)[0]
                st.success(f"A resistência prevista do concreto aos 28 dias é: **{resistencia_28d:.2f} MPa**")
            except Exception as e:
                st.error(f"Erro ao carregar o modelo ou realizar a predição: {e}")
        else:
            st.error("Por favor, insira valores válidos para todas as variáveis.")

elif tipo_entrada == "Carregar arquivo Excel":
    # Selecionar a configuração de entrada
    st.write("Selecione a configuração de entrada para os dados do Excel:")
    opcao = st.radio(
        "Escolha a configuração de entrada:",
        [
            "CT_Cimento e CT_Água",
            "CT_Cimento, CT_Água, e resistências reais (3d, 7d, 28d)",
            "CT_Cimento, CT_Água, resistências reais, e Fc_7d",
            "CT_Cimento, CT_Água, resistências reais, Fc_7d, e aditivos",
            "Todas as variáveis"
        ]
    )

    # Mapear opções para modelos e colunas esperadas
    configuracoes = {
        "CT_Cimento e CT_Água": ("modelo1.pkl", ["CT_Cimento", "CT_Água"]),
        "CT_Cimento, CT_Água, e resistências reais (3d, 7d, 28d)": (
            "modelo2.pkl", 
            ["CT_Cimento", "CT_Água", "cimento_Resistencia_real_3d", 
             "cimento_Resistencia_real_7d", "cimento_Resistencia_real_28d"]
        ),
        "CT_Cimento, CT_Água, resistências reais, e Fc_7d": (
            "modelo3.pkl", 
            ["CT_Cimento", "CT_Água", "cimento_Resistencia_real_3d", 
             "cimento_Resistencia_real_7d", "cimento_Resistencia_real_28d", 
             "Fc_7d"]
        ),
        "CT_Cimento, CT_Água, resistências reais, Fc_7d, e aditivos": (
            "modelo4.pkl", 
            ["CT_Cimento", "CT_Água", "cimento_Resistencia_real_3d", 
             "cimento_Resistencia_real_7d", "cimento_Resistencia_real_28d", 
             "Fc_7d", "CT_Silica", "CT_Plastificante", "CT_Polifuncional", 
             "CT_Superplastificante", "CT_Brita_0", "CT_Brita_1", 
             "CT_Areia_natural", "CT_Areia_artificial", "CT_AC", "CT_Aditivo", 
             "CT_Teor_de_Argamassa", "CT_Teor_de_Agua"]
        ),
        "Todas as variáveis": (
            "modelo5.pkl", 
            ["CT_Cimento", "CT_Água", "cimento_Resistencia_real_3d", 
             "cimento_Resistencia_real_7d", "cimento_Resistencia_real_28d", 
             "Fc_7d", "CT_Silica", "CT_Plastificante", "CT_Polifuncional", 
             "CT_Superplastificante", "CT_Brita_0", "CT_Brita_1", 
             "CT_Areia_natural", "CT_Areia_artificial", "CT_AC", "CT_Aditivo", 
             "CT_Teor_de_Argamassa", "CT_Teor_de_Agua", "Volume", 
             "Mesp_Brita_0", "Mesp_Brita_1", "Tempo_de_transporte", "Slump"]
        )
    }

    model_path, colunas_necessarias = configuracoes[opcao]

    uploaded_file = st.file_uploader("Faça o upload do arquivo Excel com os dados", type=["xlsx"])
    if uploaded_file is not None:
        try:
            # Carregar os dados do Excel
            data = pd.read_excel(uploaded_file)
            st.write("Dados carregados com sucesso:", data.head())

            # Validar as colunas do arquivo
            if not all(col in data.columns for col in colunas_necessarias):
                st.error(
                    "O arquivo Excel não contém todas as colunas necessárias para o modelo selecionado. "
                    f"As colunas esperadas são: {colunas_necessarias}"
                )
            else:
                # Carregar o modelo correspondente
                model = joblib.load(model_path)

                # Selecionar apenas as colunas necessárias
                data_modelo = data[colunas_necessarias]

                # Fazer a previsão
                resultados = model.predict(data_modelo)
                data['Resistência 28d (MPa)'] = resultados
                st.success("Previsões realizadas com sucesso!")
                st.write(data)

                # Gerar arquivo Excel com os resultados
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    data.to_excel(writer, index=False, sheet_name="Resultados")

                # Botão para baixar o arquivo Excel
                st.download_button(
                    label="Baixar resultados em Excel",
                    data=buffer.getvalue(),
                    file_name="resultados_resistencia_28d.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        except Exception as e:
            st.error(f"Erro ao processar o arquivo ou realizar a predição: {e}")
# Footer
st.markdown(
    """
    <footer style="text-align: center; margin-top: 20px;">
        <small>Projeto Embrapii | USP | ITA</small>
    </footer>
    """,
    unsafe_allow_html=True,
)
