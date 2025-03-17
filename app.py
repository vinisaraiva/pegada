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
st.image("banner.jpg", caption="", use_column_width="auto")
st.write("&nbsp;")
tab1, tab2 = st.tabs([" 👣 PEGADA DE CARBONO    ", " 💧 PEGADA HIDRÍCA   "])
with tab1:
    st.write("Descubra sua pegada de carbono e veja como reduzir seu impacto ambiental!")

    # Inicializar session_state para armazenar respostas
    if 'respostas' not in st.session_state:
        st.session_state.respostas = {}
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 0

    # Perguntas ao usuário (passo a passo)
    st.sidebar.header("📋 Questionário")
    perguntas = [
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

    def obter_resposta(pergunta):
        if pergunta in ["Você usa transporte próprio?", "Você utiliza transporte coletivo?", "Você recicla lixo regularmente?", "Você faz compostagem de restos orgânicos?"]:
            return st.selectbox(pergunta, ["Sim", "Não"])
        elif pergunta == "Se usa transporte próprio, qual tipo? (Carro, Moto)":
            return st.selectbox(pergunta, ["Carro", "Moto"])
        elif pergunta == "Qual sua dieta?":
            return st.selectbox(pergunta, ["Vegetariana", "Pouca carne", "Consumo médio de carne", "Muita carne"])
        else:
            return st.number_input(pergunta, min_value=0, step=1)

    # Exibir perguntas passo a passo
    if st.session_state.pagina < len(perguntas):
        pergunta_atual = perguntas[st.session_state.pagina]
        resposta = obter_resposta(pergunta_atual)
        
        if st.button("Próximo"):
            st.session_state.respostas[pergunta_atual] = resposta
            st.session_state.pagina += 1
            st.rerun()
    else:
        # Calcular pegada de carbono
        def calcular_pegada(respostas):
            fator_carro = 0
            fator_moto = 0
            fator_onibus = 0
            
            if respostas.get("Você usa transporte próprio?") == "Sim":
                if respostas.get("Se usa transporte próprio, qual tipo? (Carro, Moto)") == "Carro":
                    fator_carro = 0.18 * respostas.get("Se usa transporte próprio, quantos km percorre por semana?", 0) * 52
                elif respostas.get("Se usa transporte próprio, qual tipo? (Carro, Moto)") == "Moto":
                    fator_moto = 0.08 * respostas.get("Se usa transporte próprio, quantos km percorre por semana?", 0) * 52
            
            if respostas.get("Você utiliza transporte coletivo?") == "Sim":
                fator_onibus = 0.06 * respostas.get("Se usa transporte coletivo, quantos dias por semana?", 0) * 52
            
            fator_energia = 0.35 * respostas.get("Consumo mensal de energia (kWh)?", 0) * 12
            fator_voos = respostas.get("Quantos voos de longa distância por ano?", 0) * 1100
            fator_produtos = respostas.get("Quantos produtos industrializados você consome por semana?", 0) * 50
            fator_refeicoes = respostas.get("Quantas refeições você consome fora de casa por semana?", 0) * 75
            fator_roupas = respostas.get("Quantas compras de roupas novas você faz por ano?", 0) * 100
            fator_reciclagem = -500 if respostas.get("Você recicla lixo regularmente?", "Não") == "Sim" else 0
            fator_compostagem = -300 if respostas.get("Você faz compostagem de restos orgânicos?", "Não") == "Sim" else 0
            
            fator_dieta = {"Vegetariana": 1500, "Pouca carne": 2500, "Consumo médio de carne": 3500, "Muita carne": 4500}
            
            pegada_total = (fator_carro + fator_moto + fator_onibus + fator_energia + fator_voos + fator_produtos +
                            fator_refeicoes + fator_roupas + fator_reciclagem + fator_compostagem + fator_dieta[respostas.get("Qual sua dieta?", "Consumo médio de carne")])
            return pegada_total
        
        pegada = calcular_pegada(st.session_state.respostas)
        media_global = 4800  # Média global de emissão per capita
        restauracao_por_arvore = 25  # Cada árvore absorve 22kg de CO2/ano
        arvores_necessarias = pegada / restauracao_por_arvore
        
        st.subheader("📊 Resultado da sua Pegada de Carbono")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Sua Pegada de Carbono", value=f"{pegada:.2f} kg CO2")
        with col2:
            st.metric(label="Média Global", value=f"{media_global:.2f} kg CO2")
        
        st.write(f"🌳 Para equilibrar sua emissão, seria necessário restaurar **{arvores_necessarias:.0f} árvores**!")
        st.write(f"Isso equivale aproximadamente a:")
        st.write(f"🌱 **{arvores_necessarias / 4:.0f} mudas de Pau-Brasil**")
        st.write(f"🌿 **{arvores_necessarias / 4:.0f} mudas de Ipê-Amarelo**")
        st.write(f"🌳 **{arvores_necessarias / 4:.0f} mudas de Ingá**")
        st.write(f"🌲 **{arvores_necessarias / 4:.0f} mudas de Jacarandá**")
        
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
        if st.session_state.respostas.get("Se usa transporte próprio, quantos km percorre por semana?", 0) > 50:
            st.write("🚴 **Use bicicleta ou transporte público para trajetos curtos.")
        if st.session_state.respostas.get("Consumo mensal de energia (kWh)?", 0) > 200:
            st.write("💡 **Reduza o consumo de energia com lâmpadas LED e eletrônicos eficientes.")
        if st.session_state.respostas.get("Qual sua dieta?", "Consumo médio de carne") in ["Consumo médio de carne", "Muita carne"]:
            st.write("🥦 **Reduza o consumo de carne e adote mais refeições à base de vegetais.")
        
        st.write("🌿 Pequenas mudanças no dia a dia ajudam a preservar o planeta!")

with tab2:
    st.write("Descubra seu consumo de água e veja como reduzir seu impacto hídrico!")

    # Inicializar session_state para armazenar respostas
    if 'respostas' not in st.session_state:
        st.session_state.respostas = {}
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 0

    # Perguntas ao usuário (passo a passo)
    st.sidebar.header("📋 Questionário")
    perguntas = [
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

    def obter_resposta(pergunta):
        if pergunta in ["Você usa máquina de lavar roupas? (Sim ou Não)", "Você consome carne regularmente? (Sim ou Não)", "Você consome produtos industrializados frequentemente? (Sim ou Não)"]:
            return st.selectbox(pergunta, ["Sim", "Não"])
        else:
            return st.number_input(pergunta, min_value=0, step=1)

    # Exibir perguntas passo a passo
    if st.session_state.pagina < len(perguntas):
        pergunta_atual = perguntas[st.session_state.pagina]
        resposta = obter_resposta(pergunta_atual)
        
        if st.button("Próximo"):
            st.session_state.respostas[pergunta_atual] = resposta
            st.session_state.pagina += 1
            st.rerun()
    else:
        # Calcular pegada hídrica
        def calcular_pegada_hidrica(respostas):
            fator_banho = 8 * respostas.get("Qual a duração média do seu banho (em minutos)?", 0) * respostas.get("Quantos banhos você toma por dia?", 0) * 365  # Média reduzida considerando uso frequente de chuveiros elétricos econômicos na região  # Banho médio na Bahia consome menos água devido ao uso de chuveiros elétricos econômicos
            fator_lavar_roupas = 100 * respostas.get("Quantas vezes por semana você usa a máquina de lavar roupas?", 0) * 52  # Redução devido ao uso de tanques e lavagem manual comum na região  # Média reduzida por lavagem a frio e uso de tanques if respostas.get("Você usa máquina de lavar roupas? (Sim ou Não)") == "Sim" else 0
            fator_lavar_louca = 12 * respostas.get("Quantas vezes por dia você lava louça?", 0) * 365  # Uso frequente de bacias e reutilização de água  # Uso de bacias e reutilização de água para enxágue
            fator_carne = 15400 * respostas.get("Quantas porções de carne você consome por semana?", 0) * 52 if respostas.get("Você consome carne regularmente? (Sim ou Não)") == "Sim" else 0
            fator_cafe = 90 * respostas.get("Quantas xícaras de café você bebe por dia?", 0) * 365  # Consumo menor devido à preferência por outras bebidas como sucos tropicais  # Consumo local de café pode ser ligeiramente menor
            fator_produtos = 5000 if respostas.get("Você consome produtos industrializados frequentemente? (Sim ou Não)") == "Sim" else 0
            
            pegada_total = (fator_banho + fator_lavar_roupas + fator_lavar_louca + fator_carne + fator_cafe + fator_produtos)
            return pegada_total
        
        pegada = calcular_pegada_hidrica(st.session_state.respostas)
        media_global = 950000  # Média regional estimada para a Bahia/Sul da Bahia (litros/ano)  # Média global de pegada hídrica per capita (litros/ano)  # Média regional estimada para a Bahia (litros/ano)  # Média global de pegada hídrica (litros/ano)
        
        st.subheader("📊 Resultado da sua Pegada Hídrica")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Sua Pegada Hídrica", value=f"{pegada:.0f} litros/ano")
        with col2:
            st.metric(label="Média Global", value=f"{media_global:.0f} litros/ano")
        
        # Gráfico comparativo
        fig, ax = plt.subplots()
        categorias = ['Sua Pegada', 'Média Global']
        valores = [pegada, media_global]
        ax.bar(categorias, valores, color=['blue', 'gray'])
        ax.set_ylabel("Litros de água por ano")
        ax.set_title("Comparação com a Média Global")
        st.pyplot(fig)
        
        # Sugestões para redução
        st.subheader("💡 Dicas para Reduzir Sua Pegada Hídrica")
        if respostas.get("Qual a duração média do seu banho (em minutos)?", 0) > 10:
            st.write("🚿 **Reduza o tempo do banho para economizar água.")
        if respostas.get("Quantas vezes por semana você usa a máquina de lavar roupas?", 0) > 3:
            st.write("👕 **Lave roupas com carga completa para reduzir o consumo de água.")
        if respostas.get("Você consome carne regularmente? (Sim ou Não)") == "Sim":
            st.write("🥩 **Diminuir o consumo de carne pode reduzir sua pegada hídrica.")
        if respostas.get("Quantas xícaras de café você bebe por dia?", 0) > 3:
            st.write("☕ **Reduzir o consumo de café ajuda a economizar água indiretamente.")
        
        st.write("💙 Pequenas mudanças no dia a dia ajudam a preservar os recursos hídricos!")
