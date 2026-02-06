import streamlit as st
import yt_dlp
import whisper
import os
import time

# --- Configuração Inicial ---
st.set_page_config(page_title="DarkViral AI - Core", page_icon="🧠", layout="wide")

# Estilos Hacker
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff41; }
    .stTextInput > div > div > input { color: #00ff41; background-color: #262730; }
    .stButton > button { background-color: #00ff41; color: black; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 DarkViral AI - O Cérebro")
st.markdown("### V.2.0: Download Real + Transcrição Neural")

# Criar pastas temporárias se não existirem
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# --- Funções do Backend ---

@st.cache_resource
def carregar_modelo_whisper():
    """Carrega o modelo de IA na memória (só faz isso uma vez)"""
    print("Carregando modelo Whisper...")
    return whisper.load_model("tiny") # Usando 'tiny' para não explodir a RAM do servidor grátis

def baixar_audio(url):
    """Baixa e encontra o arquivo real na pasta, não importa a extensão"""
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        # Removemos a conversão forçada para evitar erros se o FFmpeg demorar
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.youtube.com/',
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'geo_bypass': True,
    }
    
    # 1. Limpa a pasta downloads antes de começar (para não misturar arquivos antigos)
    for f in os.listdir("downloads"):
        os.remove(os.path.join("downloads", f))

    # 2. Baixa
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info['id']
        titulo = info['title']
        thumb = info['thumbnail']
        
        # 3. CAÇADOR DE ARQUIVOS: Procura qual arquivo foi gerado
        for arquivo in os.listdir("downloads"):
            if video_id in arquivo:
                caminho_completo = os.path.join("downloads", arquivo)
                return caminho_completo, titulo, thumb
                
        raise Exception("O download parece ter funcionado, mas não achei o arquivo na pasta!")
# --- Interface do Usuário ---

url = st.text_input("🔗 Link do YouTube (Teste com vídeos curtos < 10min):")

if st.button("🚀 INICIAR ANÁLISE REAL"):
    if not url:
        st.error("Coloque um link!")
    else:
        status = st.status("⚙️ Iniciando motores...", expanded=True)
        
        try:
            # 1. Download
            status.write("📥 Baixando áudio do YouTube...")
            arquivo_audio, titulo, thumb = baixar_audio(url)
            status.write(f"✅ Download concluído: {titulo}")
            st.image(thumb, width=300)
            
            # 2. Transcrição (IA)
            status.write("🧠 Carregando IA (Whisper)...")
            model = carregar_modelo_whisper()
            
            status.write("👂 A IA está ouvindo o vídeo (Isso pode demorar)...")
            result = model.transcribe(arquivo_audio)
            texto_completo = result["text"]
            
            status.update(label="✅ Processo Concluído!", state="complete", expanded=False)
            
            # 3. Mostrar Resultado
            st.success("Transcrição Realizada com Sucesso!")
            st.subheader("📝 O que a IA ouviu:")
            st.text_area("Texto Transcrito", value=texto_completo, height=300)
            
            # Aqui é onde entrará o passo 3: Enviar esse texto para o GPT encontrar os cortes
            st.info("Próximo passo: Conectar GPT-4 para encontrar os momentos virais neste texto.")
            
        except Exception as e:
            status.update(label="❌ Erro Crítico", state="error")
            st.error(f"Ocorreu um erro: {e}")


