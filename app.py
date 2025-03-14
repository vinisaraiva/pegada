import os
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from PIL import Image
import io
import requests
import base64
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_VISION_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
PLANT_ID_API_KEY = "9K6WxFaBrABOOln0YFgUAOLybbu1X7wYZnQULogKAujDYXjntx"
PLANT_ID_API_URL = "https://plant.id/api/v3/psforest"

# Carregar a base de dados
df = pd.read_csv("especies_mata_atlantica_expandido.csv")

# Configuração da Página
st.set_page_config(page_title="Guia Virtual RA - Mata Atlântica", layout="wide")
st.title("🌱 Guia Virtual RA - Mata Atlântica")
st.write("Explore as espécies nativas da Mata Atlântica em Porto Seguro!")

# Barra Lateral para Filtragem
st.sidebar.header("🔍 Filtro de Espécies")
grupo_selecionado = st.sidebar.selectbox("Selecione o grupo:", ["Todos"] + list(df["Grupo"].unique()))
nome_selecionado = st.sidebar.text_input("Busque pelo nome:")

# Filtrar dados conforme seleção
if grupo_selecionado != "Todos":
    df_filtrado = df[df["Grupo"] == grupo_selecionado]
else:
    df_filtrado = df
if nome_selecionado:
    df_filtrado = df_filtrado[df_filtrado["Nome Comum"].str.contains(nome_selecionado, case=False)]

# Exibir tabela de espécies
st.subheader("📜 Lista de Espécies")
st.dataframe(df_filtrado)

# Mapa Interativo com Folium
st.subheader("🗺️ Mapa de Distribuição")
m = folium.Map(location=[-16.446, -39.065], zoom_start=10)
folium.Marker([-16.446, -39.065], popup="Parque Nacional do Pau-Brasil").add_to(m)
folium_static(m)

# Upload de Imagem para Identificação
st.subheader("📷 Identifique uma Espécie")
uploaded_file = st.file_uploader("Envie uma imagem para identificar a espécie:", type=["jpg", "png", "jpeg"])

def identificar_planta(image_bytes):
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": PLANT_ID_API_KEY,
        "images": [encoded_image],
        "modifiers": ["similar_images"],
        "plant_details": ["common_names", "url", "wiki_description"]
    }
    
    try:
        response = requests.post(PLANT_ID_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Lança erro se a resposta for inválida
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a API Plant.id: {str(e)}")
        return None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_container_width=True)
    
    # Botão para análise da imagem
    if st.button("🔍 Analisar Planta"):
        with st.spinner("Analisando a imagem..."):
            # Converte a imagem para bytes
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes = image_bytes.getvalue()
            
            # Enviar para Plant.id API
            result = identificar_planta(image_bytes)
            
            if result and "suggestions" in result and result["suggestions"]:
                best_match = result["suggestions"][0]
                nome_cientifico = best_match["plant_name"]
                st.success(f"✅ Planta identificada: **{nome_cientifico}**")
                
                # Buscar informações na base de dados interna
                especie_info = df[df["Nome Científico"].str.lower() == nome_cientifico.lower()]
                if not especie_info.empty:
                    st.write("🌿 **Nome Comum:**", especie_info.iloc[0]["Nome Comum"])
                    st.write("📌 **Habitat:**", especie_info.iloc[0]["Habitat"])
                    st.write("⚠️ **Status de Conservação:**", especie_info.iloc[0]["Status de Conservação"])
                    st.write("📖 **Curiosidades:**", especie_info.iloc[0]["Curiosidades"])
                else:
                    st.warning("🔍 Nenhuma informação detalhada encontrada na base de dados interna.")
            else:
                st.warning("⚠️ Não foi possível identificar a planta na imagem.")

st.write("Desenvolvido para auxiliar na identificação e preservação da biodiversidade da Mata Atlântica.")
