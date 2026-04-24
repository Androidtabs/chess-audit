import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Auditoria Xadrez - Vagner", layout="centered")

# Estilo visual limpo
st.markdown("""
    <style>
    .stImage { border-radius: 15px; border: 2px solid #444; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("♟️ Auditoria: Rumo aos +400")

# Pasta para as imagens
IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# Barra Lateral para Upload
with st.sidebar:
    st.header("📥 Novo Registro")
    uploaded_file = st.file_uploader("Print do Erro", type=["jpg", "png", "jpeg"])
    comentario = st.text_area("Insight da Engine / Lição aprendida:")
    
    if st.button("Salvar na Auditoria"):
        if uploaded_file and comentario:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = os.path.join(IMG_DIR, f"{ts}.jpg")
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with open(img_path.replace(".jpg", ".txt"), "w") as f:
                f.write(comentario)
            st.success("Registrado!")
            st.rerun()

# Feed Principal (O "Rolo" de imagens que você pediu)
st.subheader("Seu Feed de Evolução (Scroll)")

if os.path.exists(IMG_DIR):
    images = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
    images.sort(reverse=True) # Mais recentes primeiro

    if not images:
        st.info("Nenhuma jogada auditada ainda. Suba seus prints pela barra lateral!")

    for img in images:
        path = os.path.join(IMG_DIR, img)
        txt_path = path.replace(".jpg", ".txt")
        
        st.image(path, use_container_width=True)
        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                st.warning(f"**Insight:** {f.read()}")
        st.write("---")
