import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Auditoria Xadrez - Vagner", layout="centered")

st.markdown("""
    <style>
    .stImage { border-radius: 15px; border: 2px solid #444; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("♟️ Auditoria: Rumo aos +400")

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# --- BARRA LATERAL: NOVO REGISTRO ---
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

# --- FEED PRINCIPAL: SCROLL COM GESTÃO ---
st.subheader("Seu Feed de Evolução")

images = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
images.sort(reverse=True)

if not images:
    st.info("Nenhuma jogada auditada ainda.")

for img in images:
    path = os.path.join(IMG_DIR, img)
    txt_path = path.replace(".jpg", ".txt")
    
    # Exibe a imagem
    st.image(path, use_container_width=True)
    
    # Lógica de Edição e Exclusão
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            texto_atual = f.read()
        
        # Campo de edição simples
        novo_texto = st.text_area("Editar Insight:", value=texto_atual, key=f"edit_{img}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Atualizar Texto", key=f"btn_edit_{img}"):
                with open(txt_path, "w") as f:
                    f.write(novo_texto)
                st.success("Texto atualizado!")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Excluir Registro", key=f"del_{img}"):
                os.remove(path)
                os.remove(txt_path)
                st.warning("Registro removido.")
                st.rerun()
    
    st.write("---")
