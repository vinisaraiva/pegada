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
st.markdown("<h2 style='color: teal; font-size: 23px;'>Calculadora de Impacto Ambiental</h2>", 
            unsafe_allow_html=True)
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
            return st.selectbox(pergunta, ["Sim", "Não"], key=pergunta)
        elif pergunta == "Se usa transporte próprio, qual tipo? (Carro, Moto)":
            return st.selectbox(pergunta, ["Carro", "Moto"], key=pergunta)
        elif pergunta == "Qual sua dieta?":
            return st.selectbox(pergunta, ["Vegetariana", "Pouca carne", "Consumo médio de carne", "Muita carne"], key=pergunta)
        else:
            return st.number_input(pergunta, min_value=0, step=1, key=pergunta)

    if st.session_state.pagina_carbono < len(perguntas_carbono):
        pergunta_atual = perguntas_carbono[st.session_state.pagina_carbono]
        resposta = obter_resposta_carbono(pergunta_atual)

        if st.button("Próximo", key="proximo_carbono"):
            st.session_state.respostas_carbono[pergunta_atual] = resposta
            st.session_state.pagina_carbono += 1
            st.rerun()
    else:
        # All the carbon footprint calculation and display code should be here
        # 🛠️ **Correção para evitar erro de soma**
        pegada_total = sum(
            float(v) for v in st.session_state.respostas_carbono.values()
            if isinstance(v, (int, float)) or str(v).replace('.', '', 1).isdigit()
        )

        st.markdown("<h2 style='color: teal; font-size: 20px;'>📊 Comparação da Pegada de Carbono</h2>", 
                unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color: green; font-size: 18px;'>Sua Pegada de Carbono:</h4>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='color: black; font-size: 22px; font-weight: bold;'>{pegada_total:.2f} kg CO2/ano</p>", unsafe_allow_html=True)
    
        # 🔹 **Simulação da Pegada de Carbono**
        st.markdown("<h2 style='color: teal; font-size: 23px;'>♻️ Simulação: Como Reduzir sua Pegada de Carbono?</h2>", 
                unsafe_allow_html=True)
        reduzir_transporte = st.checkbox("Reduzir uso de transporte próprio")
        reduzir_energia = st.checkbox("Economizar energia elétrica")
        reduzir_dieta = st.checkbox("Reduzir consumo de carne")
        reduzir_industrializados = st.checkbox("Consumir menos produtos industrializados")
    
        pegada_otimizada = pegada_total
        st.markdown("<h2 style='color: teal; font-size: 23px;'>Impactos Esperados</h2>", 
                unsafe_allow_html=True)  
        if reduzir_transporte:
            pegada_otimizada -= 500
            st.write("🚗 **Optar por transporte público ou bicicleta pode reduzir sua pegada de carbono em até 500 kg CO2/ano.**")
        if reduzir_energia:
            pegada_otimizada -= 400
            st.write("💡 **Reduzir o consumo de eletricidade pode diminuir em até 400 kg CO2/ano.**")
        if reduzir_dieta:
            pegada_otimizada -= 600
            st.write("🥩 **Diminuir o consumo de carne reduz o impacto ambiental e economiza 600 kg CO2/ano.**")
        if reduzir_industrializados:
            pegada_otimizada -= 300
            st.write("🏭 **Menos produtos industrializados significa menor pegada de carbono: economia de até 300 kg CO2/ano.**")
    
        # 🔹 **Exibição do resultado após reduções**
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<h4 style='color: teal; font-size: 23px;'>Após Reduções:</h4>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<p style='color: green; font-size: 20px; font-weight: bold;'>{pegada_otimizada:.2f} kg CO2/ano</p>", unsafe_allow_html=True)
    
        
    
# Inicializar session_state para armazenar respostas e páginas de cada aba
if 'respostas_hidrica' not in st.session_state:
    st.session_state.respostas_hidrica = {}
if 'pagina_hidrica' not in st.session_state:
    st.session_state.pagina_hidrica = 0

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
        # Cálculo da Pegada Hídrica - Convertendo todas as respostas corretamente
        consumo_diario = st.session_state.respostas_hidrica.get("Quantos litros de água você consome por dia?", 0) * 365
        fator_banho = st.session_state.respostas_hidrica.get("Qual a duração média do seu banho (em minutos)?", 0) * st.session_state.respostas_hidrica.get("Quantos banhos você toma por dia?", 0) * 8 * 365
        fator_lavar_roupas = 100 * st.session_state.respostas_hidrica.get("Quantas vezes por semana você usa a máquina de lavar roupas?", 0) * 52 if st.session_state.respostas_hidrica.get("Você usa máquina de lavar roupas? (Sim ou Não)") == "Sim" else 0
        fator_lavar_louca = 12 * st.session_state.respostas_hidrica.get("Quantas vezes por dia você lava louça?", 0) * 365 if st.session_state.respostas_hidrica.get("Você lava louça manualmente ou com máquina de lavar louças?") == "Manualmente" else 9 * st.session_state.respostas_hidrica.get("Quantas vezes por dia você lava louça?", 0) * 365
        fator_carne = 15400 * st.session_state.respostas_hidrica.get("Quantas porções de carne você consome por semana?", 0) * 52 if st.session_state.respostas_hidrica.get("Você consome carne regularmente? (Sim ou Não)") == "Sim" else 0
        fator_cafe = 90 * st.session_state.respostas_hidrica.get("Quantas xícaras de café você bebe por dia?", 0) * 365
        fator_produtos = 5000 if st.session_state.respostas_hidrica.get("Você consome produtos industrializados frequentemente? (Sim ou Não)") == "Sim" else 0

        pegada_original = consumo_diario + fator_banho + fator_lavar_roupas + fator_lavar_louca + fator_carne + fator_cafe + fator_produtos

        media_global = 1240000  # Média global
        media_bahia = 950000  # Média Bahia

        # Exibição dos valores
        st.markdown("<h2 style='color: teal; font-size: 20px;'>Comparação da Pegada Hídrica</h2>", 
            unsafe_allow_html=True)
        col1, col2, col3, col4  = st.columns([1, 2, 1, 2])
        with col1:
            st.markdown("<h2 style='color: green; font-size: 16px;'>Sua Pegada Atual</h2>", 
            unsafe_allow_html=True)
            st.caption(f"🌍 {pegada_original:.0f} litros/ano")
        with col2:
            st.markdown("<h2 style='color: green; font-size: 16px;'>Média Global</h2>", 
            unsafe_allow_html=True)
            st.caption(f"🌎 {media_global:.0f} litros/ano")
        
        with col3:
            st.markdown("<h2 style='color: green; font-size: 16px;'>Média Bahia</h2>", 
            unsafe_allow_html=True)
            st.caption(f"🏝️ {media_bahia:.0f} litros/ano")
        
        with col4:
            st.markdown("<h2 style='color: green; font-size: 16px;'>Média Bahia</h2>", 
            unsafe_allow_html=True)
            st.caption(f"🏝️ {media_bahia:.0f} litros/ano")

        # 🔹 Simulação da Pegada Hídrica
        st.markdown("<h2 style='color: teal; font-size: 20px;'>💧 Simulação: Como Reduzir sua Pegada Hídrica?</h2>", 
            unsafe_allow_html=True)
        reduzir_banho = st.checkbox("Reduzir tempo de banho")
        reduzir_lavagem = st.checkbox("Lavar roupas com menos frequência")
        reduzir_carne = st.checkbox("Diminuir consumo de carne")
        reduzir_cafe = st.checkbox("Beber menos café")

        st.markdown("<h2 style='color: teal; font-size: 20px;'>Impacto das Mudanças no Consumo de Água</h2>", 
            unsafe_allow_html=True)

        pegada_otimizada = pegada_original
        if reduzir_banho:
            pegada_otimizada -= 15000
            st.write("🚿 **Reduzir o tempo de banho pode economizar 15.000 litros/ano.**")
        if reduzir_lavagem:
            pegada_otimizada -= 10000
            st.write("👕 **Lavar roupas com menos frequência pode economizar 10.000 litros/ano.**")
        if reduzir_carne:
            pegada_otimizada -= 25000
            st.write("🥩 **Diminuir o consumo de carne reduz sua pegada hídrica em até 25.000 litros/ano.**")
        if reduzir_cafe:
            pegada_otimizada -= 8000
            st.write("☕ **Menos café significa economia de 8.000 litros de água/ano.**")

        # Gráfico atualizado
        fig, ax = plt.subplots()

        categorias = ["Pegada Atual", "Média Global", "Média Bahia", "Após Reduções"]
        valores = [pegada_original, media_global, media_bahia, pegada_otimizada]

        ax.bar(categorias, valores, color=['blue', 'gray', 'orange', 'green'])
        for i, v in enumerate(valores):
            ax.text(i, v + 50000, f"{v:.0f}L", ha='center', fontsize=10, fontweight='bold')

        ax.set_ylabel("Litros de água por ano")
        ax.set_title("Comparação da Pegada Hídrica")
        ax.set_ylim(0, max(valores) * 1.2) 

        st.pyplot(fig)

        st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <h4 style='color: teal; font-size: 20px; margin-right: 2px;'>Após Reduções:</h4>
            <p style='color: teal; font-size: 22px; font-weight: bold; margin: 0;'>{pegada_otimizada:.0f} litros/ano</p>
        </div>
        """,
        unsafe_allow_html=True
        )
