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
    """Versão Camuflagem Android: Tenta enganar o bloqueio simulando um celular"""
    
    # 1. Limpeza Garantida
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    for f in os.listdir("downloads"):
        try:
            os.remove(os.path.join("downloads", f))
        except:
            pass

    # 2. Configuração Especial para 'Pular o Muro'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': False, # Liguei o barulho para vermos erros no log se precisar
        
        # --- O TRUQUE DO ANDROID ---
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'], # Diz que é um Android
            }
        },
        
        'nocheckcertificate': True,
        'ignoreerrors': False, # Desliguei isso para vermos o erro real se falhar
        'geo_bypass': True,
    }
    
    # 3. Tenta baixar
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info['title']
            thumb = info['thumbnail']
            
    except Exception as e:
        # Se der erro aqui, vamos mostrar na tela
        raise Exception(f"O YouTube bloqueou a conexão. Detalhe do erro: {e}")

    # 4. Verifica se baixou
    arquivos_na_pasta = os.listdir("downloads")
    if not arquivos_na_pasta:
        raise Exception("Ainda bloqueado. O arquivo não apareceu na pasta.")
        
    # Pega o arquivo
    arquivo_encontrado = arquivos_na_pasta[0]
    return os.path.join("downloads", arquivo_encontrado), titulo, thumb
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




