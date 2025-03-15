import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Calculadora de Pegada de Carbono", initial_sidebar_state="collapsed", layout="wide")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* ───── Remove header & padding on top ───── */
    [data-testid="stHeader"] {display: none;}
    [data-testid="stMainBlockContainer"] {padding-top: 1rem;}
    
    /* ───── Hide overflowing navbar columns ───── */
    .st-emotion-cache-ocqkz7.eiemyj0 { /* Target navbar container */
        height: 35px; /* Adjust height for logo size */
        overflow: hidden;
    }
    
    
    /* ───── Move sidebar toggle to the right and replace SVG ───── */
    [data-testid="stSidebarCollapsedControl"] {
        position: fixed;
        right: 3rem;
    }
    [data-testid="stSidebarCollapsedControl"] svg {
        display: none;
    }
    
    [data-testid="stSidebarCollapsedControl"]::before {
        content: "☰"; /* Hamburger menu icon */
        font-size: 24px;
        position: fixed;
        right: 3rem;
    }
    
    
    /* ───── Display sidebar button based on screen size ───── */
    @media (min-width: 640px) {
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
    }
    
    @media (max-width: 639px) {
        [data-testid="stSidebarCollapsedControl"] {
            display: flex;
            justify-content: flex-end;  /* Align hamburger icon right */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Calculadora de Pegada de Carbono")
st.write("Descubra sua pegada de carbono e veja como reduzir seu impacto ambiental!")

# Perguntas ao usuário (passo a passo)
st.sidebar.header("📋 Questionário")
perguntas = [
    "Você usa transporte próprio? (Carro, Moto, Nenhum)",
    "Se usa transporte próprio, quantos km percorre por semana?",
    "Você utiliza transporte coletivo? (Sim ou Não)",
    "Se usa transporte coletivo, quantos dias por semana?",
    "Consumo mensal de energia (kWh)?",
    "Qual sua dieta?",
    "Quantos voos de longa distância por ano?",
    "Quantos produtos industrializados você consome por semana?",
    "Quantas refeições você consome fora de casa por semana?",
    "Você recicla lixo regularmente?",
    "Você faz compostagem de restos orgânicos?",
    "Quantas compras de roupas novas você faz por ano?"
]

respostas = {}
if 'pagina' not in st.session_state:
    st.session_state.pagina = 0

if st.session_state.pagina < len(perguntas):
    if perguntas[st.session_state.pagina] == "Qual sua dieta?":
        resposta = st.selectbox(perguntas[st.session_state.pagina], ["Vegetariana", "Pouca carne", "Consumo médio de carne", "Muita carne"])
    elif perguntas[st.session_state.pagina] == "Você usa transporte próprio? (Carro, Moto, Nenhum)":
        resposta = st.selectbox(perguntas[st.session_state.pagina], ["Carro", "Moto", "Nenhum"])
    elif perguntas[st.session_state.pagina] == "Você utiliza transporte coletivo? (Sim ou Não)":
        resposta = st.selectbox(perguntas[st.session_state.pagina], ["Sim", "Não"])
    else:
        resposta = st.number_input(perguntas[st.session_state.pagina], min_value=0, step=1)
    
    if st.button("Próximo"):
        respostas[perguntas[st.session_state.pagina]] = resposta
        st.session_state.pagina += 1
        st.experimental_rerun()
else:
    # Calcular pegada de carbono
    def calcular_pegada(respostas):
        fator_carro = 0
        fator_moto = 0
        fator_onibus = 0
        
        if respostas["Você usa transporte próprio? (Carro, Moto, Nenhum)"] == "Carro":
            fator_carro = 0.18 * respostas["Se usa transporte próprio, quantos km percorre por semana?"] * 52
        elif respostas["Você usa transporte próprio? (Carro, Moto, Nenhum)"] == "Moto":
            fator_moto = 0.08 * respostas["Se usa transporte próprio, quantos km percorre por semana?"] * 52
        
        if respostas["Você utiliza transporte coletivo? (Sim ou Não)"] == "Sim":
            fator_onibus = 0.06 * respostas["Se usa transporte coletivo, quantos dias por semana?"] * 52
        
        fator_energia = 0.35 * respostas["Consumo mensal de energia (kWh)?"] * 12
        fator_voos = respostas["Quantos voos de longa distância por ano?"] * 1100
        fator_produtos = respostas["Quantos produtos industrializados você consome por semana?"] * 50
        fator_refeicoes = respostas["Quantas refeições você consome fora de casa por semana?"] * 75
        fator_roupas = respostas["Quantas compras de roupas novas você faz por ano?"] * 100
        fator_reciclagem = -500 if respostas["Você recicla lixo regularmente?"] > 0 else 0
        fator_compostagem = -300 if respostas["Você faz compostagem de restos orgânicos?"] > 0 else 0
        
        fator_dieta = {"Vegetariana": 1500, "Pouca carne": 2500, "Consumo médio de carne": 3500, "Muita carne": 4500}
        
        pegada_total = (fator_carro + fator_moto + fator_onibus + fator_energia + fator_voos + fator_produtos +
                        fator_refeicoes + fator_roupas + fator_reciclagem + fator_compostagem + fator_dieta[respostas["Qual sua dieta?"]])
        return pegada_total
    
    pegada = calcular_pegada(respostas)
    media_global = 4800  # Média global de emissão per capita
    restauracao_por_arvore = 22  # Cada árvore absorve 22kg de CO2/ano
    arvores_necessarias = pegada / restauracao_por_arvore
    
    st.subheader("📊 Resultado da sua Pegada de Carbono")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Sua Pegada de Carbono", value=f"{pegada:.2f} kg CO2")
    with col2:
        st.metric(label="Média Global", value=f"{media_global:.2f} kg CO2")
    
    st.write(f"🌳 Para equilibrar sua emissão, seria necessário restaurar **{arvores_necessarias:.0f} árvores**!")
    
    # Gráfico comparativo
    fig, ax = plt.subplots()
    categorias = ['Sua Pegada', 'Média Global']
    valores = [pegada, media_global]
    ax.bar(categorias, valores, color=['green', 'red'])
    ax.set_ylabel("kg CO2 por ano")
    ax.set_title("Comparação com a Média Global")
    st.pyplot(fig)
    
    # Sugestões para redução
    st.subheader("🌱 Dicas para Reduzir Sua Pegada")
    if respostas["Se usa transporte próprio, quantos km percorre por semana?"] > 50:
        st.write("🚴 **Use bicicleta ou transporte público para trajetos curtos.")
    if respostas["Consumo mensal de energia (kWh)?"] > 200:
        st.write("💡 **Reduza o consumo de energia com lâmpadas LED e eletrônicos eficientes.")
    if respostas["Qual sua dieta?"] in ["Consumo médio de carne", "Muita carne"]:
        st.write("🥦 **Reduza o consumo de carne e adote mais refeições à base de vegetais.")
    if respostas["Quantos voos de longa distância por ano?"] > 2:
        st.write("✈️ **Evite voos curtos sempre que possível, priorize transporte terrestre.")
    if respostas["Você recicla lixo regularmente?"] == 0:
        st.write("♻️ **Comece a reciclar para reduzir emissões desnecessárias.")

    st.write("🌿 Pequenas mudanças no dia a dia ajudam a preservar o planeta!")

    if st.session_state.respostas.get("Você recicla lixo regularmente?", "Não") == "Não":
        st.write("♻️ **Comece a reciclar para reduzir emissões desnecessárias.")

    st.write("🌿 Pequenas mudanças no dia a dia ajudam a preservar o planeta!")
