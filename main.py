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
    "Quantos km você dirige por semana?",
    "Consumo mensal de energia (kWh)?",
    "Qual sua dieta?",
    "Quantos voos de longa distância por ano?",
    "Quantos produtos industrializados você consome por semana?",
    "Quantas refeições você consome fora de casa por semana?",
    "Você recicla lixo regularmente?",
    "Quantas compras de roupas novas você faz por ano?"
]

# Inicializar session state
if 'pagina' not in st.session_state:
    st.session_state.pagina = 0
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

# Botão para reiniciar o questionário
if st.sidebar.button("Calcular Novamente"):
    st.session_state.pagina = 0
    st.session_state.respostas = {}
    st.rerun()

# Exibir perguntas uma por vez
if st.session_state.pagina < len(perguntas):
    pergunta_atual = perguntas[st.session_state.pagina]
    
    if pergunta_atual == "Qual sua dieta?":
        resposta = st.selectbox(pergunta_atual, ["Vegetariana", "Pouca carne", "Consumo médio de carne", "Muita carne"], index=0)
    elif pergunta_atual == "Você recicla lixo regularmente?":
        resposta = st.radio(pergunta_atual, ["Sim", "Não"], index=1)
    else:
        resposta = st.number_input(pergunta_atual, min_value=0, step=1)
    
    if st.button("Próximo"):
        st.session_state.respostas[pergunta_atual] = resposta
        st.session_state.pagina += 1
        st.rerun()
else:
    # Calcular pegada de carbono
    def calcular_pegada(respostas):
        fator_carro = 0.21 * respostas.get("Quantos km você dirige por semana?", 0) * 52
        fator_energia = 0.5 * respostas.get("Consumo mensal de energia (kWh)?", 0) * 12
        fator_voos = respostas.get("Quantos voos de longa distância por ano?", 0) * 1100
        fator_produtos = respostas.get("Quantos produtos industrializados você consome por semana?", 0) * 50
        fator_refeicoes = respostas.get("Quantas refeições você consome fora de casa por semana?", 0) * 75
        fator_roupas = respostas.get("Quantas compras de roupas novas você faz por ano?", 0) * 100
        fator_reciclagem = -500 if respostas.get("Você recicla lixo regularmente?", "Não") == "Sim" else 0
        
        fator_dieta = {"Vegetariana": 1500, "Pouca carne": 2500, "Consumo médio de carne": 3500, "Muita carne": 4500}
        
        pegada_total = (fator_carro + fator_energia + fator_voos + fator_produtos +
                        fator_refeicoes + fator_roupas + fator_reciclagem + fator_dieta[respostas.get("Qual sua dieta?", "Vegetariana")])
        return pegada_total
    
    pegada = calcular_pegada(st.session_state.respostas)
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
    if st.session_state.respostas.get("Quantos km você dirige por semana?", 0) > 50:
        st.write("🚴 **Use bicicleta ou transporte público para trajetos curtos.")
    if st.session_state.respostas.get("Consumo mensal de energia (kWh)?", 0) > 200:
        st.write("💡 **Reduza o consumo de energia com lâmpadas LED e eletrônicos eficientes.")
    if st.session_state.respostas.get("Qual sua dieta?", "Vegetariana") in ["Consumo médio de carne", "Muita carne"]:
        st.write("🥦 **Reduza o consumo de carne e adote mais refeições à base de vegetais.")
    if st.session_state.respostas.get("Quantos voos de longa distância por ano?", 0) > 2:
        st.write("✈️ **Evite voos curtos sempre que possível, priorize transporte terrestre.")
    if st.session_state.respostas.get("Você recicla lixo regularmente?", "Não") == "Não":
        st.write("♻️ **Comece a reciclar para reduzir emissões desnecessárias.")

    st.write("🌿 Pequenas mudanças no dia a dia ajudam a preservar o planeta!")
