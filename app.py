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

st.write("&nbsp;")
st.subheader("Calculadora de Impacto Ambiental")
st.image("banner.jpg", caption="")
st.write("&nbsp;")

# Criar tabs para as duas calculadoras
tab1, tab2 = st.tabs([" 👣 PEGADA DE CARBONO    ", " 💧 PEGADA HÍDRICA   "])

# Sidebar com botão para reiniciar as perguntas
st.sidebar.header("📋 Configurações")
if st.sidebar.button("🔄 Reiniciar Questionários"):
    st.session_state.respostas_carbono = {}
    st.session_state.respostas_hidrica = {}
    st.session_state.pagina_carbono = 0
    st.session_state.pagina_hidrica = 0
    st.rerun()

# Inicializar session_state para armazenar respostas e páginas de cada aba
if 'respostas_carbono' not in st.session_state:
    st.session_state.respostas_carbono = {}
if 'respostas_hidrica' not in st.session_state:
    st.session_state.respostas_hidrica = {}
if 'pagina_carbono' not in st.session_state:
    st.session_state.pagina_carbono = 0
if 'pagina_hidrica' not in st.session_state:
    st.session_state.pagina_hidrica = 0

### 🔹 **ABA - PEGADA DE CARBONO** ###
with tab1:
    st.write("Descubra sua pegada de carbono e veja como reduzir seu impacto ambiental!")

    perguntas_carbono = [
        "Você usa transporte próprio?",
        "Se usa transporte próprio, qual tipo? (Carro, Moto)",
        "Se usa transporte próprio, quantos km percorre por semana?",
        "Você utiliza transporte coletivo?",
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

    def obter_resposta_carbono(pergunta):
        if pergunta in ["Você usa transporte próprio?", "Você utiliza transporte coletivo?", "Você recicla lixo regularmente?", "Você faz compostagem de restos orgânicos?"]:
            return st.selectbox(pergunta, ["Sim", "Não"])
        elif pergunta == "Se usa transporte próprio, qual tipo? (Carro, Moto)":
            return st.selectbox(pergunta, ["Carro", "Moto"])
        elif pergunta == "Qual sua dieta?":
            return st.selectbox(pergunta, ["Vegetariana", "Pouca carne", "Consumo médio de carne", "Muita carne"])
        else:
            return st.number_input(pergunta, min_value=0, step=1)

    if st.session_state.pagina_carbono < len(perguntas_carbono):
        pergunta_atual = perguntas_carbono[st.session_state.pagina_carbono]
        resposta = obter_resposta_carbono(pergunta_atual)

        if st.button("Próximo", key="proximo_carbono"):
            st.session_state.respostas_carbono[pergunta_atual] = resposta
            st.session_state.pagina_carbono += 1
            st.rerun()
    else:
        st.subheader("📊 Resultado da sua Pegada de Carbono")
        st.write(f"🌍 Sua pegada de carbono: **{sum(st.session_state.respostas_carbono.values())} kg CO2/ano**")

### 🔹 **ABA - PEGADA HÍDRICA** ###
with tab2:
    st.write("Descubra seu consumo de água e veja como reduzir seu impacto hídrico!")

    perguntas_hidrica = [
        "Quantos litros de água você consome por dia?",
        "Quantos banhos você toma por dia?",
        "Qual a duração média do seu banho (em minutos)?",
        "Você usa máquina de lavar roupas? (Sim ou Não)",
        "Quantas vezes por semana você usa a máquina de lavar roupas?",
        "Você lava louça manualmente ou com máquina de lavar louças?",
        "Quantas vezes por dia você lava louça?",
        "Você consome carne regularmente? (Sim ou Não)",
        "Quantas porções de carne você consome por semana?",
        "Quantas xícaras de café você bebe por dia?",
        "Você consome produtos industrializados frequentemente? (Sim ou Não)"
    ]

    def obter_resposta_hidrica(pergunta):
        if pergunta in ["Você usa máquina de lavar roupas? (Sim ou Não)", "Você consome carne regularmente? (Sim ou Não)", "Você consome produtos industrializados frequentemente? (Sim ou Não)"]:
            return st.selectbox(pergunta, ["Sim", "Não"], key=pergunta)
        elif pergunta == "Você lava louça manualmente ou com máquina de lavar louças?":
            return st.selectbox(pergunta, ["Manualmente", "Com Lava-louças"], key=pergunta)
        else:
            return st.number_input(pergunta, min_value=0, step=1, key=pergunta)

    if st.session_state.pagina_hidrica < len(perguntas_hidrica):
        pergunta_atual = perguntas_hidrica[st.session_state.pagina_hidrica]
        resposta = obter_resposta_hidrica(pergunta_atual)

        if st.button("Próximo", key="proximo_hidrica"):
            st.session_state.respostas_hidrica[pergunta_atual] = resposta
            st.session_state.pagina_hidrica += 1
            st.rerun()
    else:
        # Resultados e Comparação
        pegada_original = sum(st.session_state.respostas_hidrica.values())
        media_global = 1240000  # Média global por pessoa
        media_bahia = 950000  # Média ajustada para a Bahia

        st.subheader("📊 Comparação da Pegada Hídrica")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Sua Pegada Atual")
            st.caption(f"🌍 {pegada_original:.0f} litros/ano")
        with col2:
            st.header("Média Global")
            st.caption(f"🌎 {media_global:.0f} litros/ano")
        with col3:
            st.header("Média na Bahia")
            st.caption(f"🏝️ {media_bahia:.0f} litros/ano")

        # Simulação de economia de água
        st.subheader("💧 Simulação: Como Reduzir sua Pegada Hídrica?")
        reduzir_banho = st.checkbox("Reduzir tempo de banho (de 10 para 5 min)")
        reduzir_lavagem_roupa = st.checkbox("Lavar roupas com menos frequência")

        pegada_otimizada = pegada_original
        if reduzir_banho:
            pegada_otimizada -= 5000
        if reduzir_lavagem_roupa:
            pegada_otimizada -= 5000

        # Gráfico atualizado
        st.subheader("📉 Impacto das Mudanças no Consumo de Água")
        fig, ax = plt.subplots()
        ax.bar(["Pegada Atual", "Média Global", "Após Reduções"], [pegada_original, media_global, pegada_otimizada], color=['blue', 'gray', 'green'])
        st.pyplot(fig)
