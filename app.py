import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress
import whisper
import os

# --- Configuração Inicial ---
st.set_page_config(page_title="DarkViral AI - Core", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff41; }
    .stTextInput > div > div > input { color: #00ff41; background-color: #262730; }
    .stButton > button { background-color: #00ff41; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 DarkViral AI - V.3.0 (Anti-Bloqueio)")
st.markdown("### Teste com Pytubefix")

# --- Função de Download Nova ---
def baixar_audio_pytubefix(url):
    """Usa Pytubefix para burlar o erro 403"""
    
    # Limpa pasta anterior
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    for f in os.listdir("downloads"):
        try: os.remove(os.path.join("downloads", f))
        except: pass

    # Inicia o download
    yt = YouTube(url, on_progress_callback=on_progress)
    st.write(f"🔍 Vídeo encontrado: {yt.title}")
    
    # Pega apenas o áudio para ser leve
    video = yt.streams.get_audio_only()
    
    # Baixa na pasta downloads
    out_file = video.download(output_path="downloads")
    
    # Renomeia para mp3 (opcional, mas ajuda na organização)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    return new_file, yt.title, yt.thumbnail_url

# --- Interface ---
url = st.text_input("🔗 Link do YouTube:")

if st.button("🚀 INICIAR"):
    if not url:
        st.error("Coloque um link!")
    else:
        status = st.status("⚙️ Iniciando...", expanded=True)
        try:
            # 1. Download
            status.write("📥 Baixando com tecnologia Anti-Bloqueio...")
            arquivo, titulo, thumb = baixar_audio_pytubefix(url)
            status.write(f"✅ Sucesso: {titulo}")
            st.image(thumb, width=300)
            
            # 2. Transcrição
            status.write("🧠 Carregando IA...")
            model = whisper.load_model("tiny")
            
            status.write("👂 Transcrevendo...")
            result = model.transcribe(arquivo)
            
            status.update(label="✅ Tudo pronto!", state="complete", expanded=False)
            
            st.success("Download e Transcrição concluídos!")
            st.text_area("Resultado", result["text"], height=300)
            
        except Exception as e:
            status.update(label="❌ Erro", state="error")
            st.error(f"Erro: {e}")
