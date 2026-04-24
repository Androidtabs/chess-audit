import streamlit as st
import os

st.set_page_config(page_title="Flashcards Xadrez - Vagner", layout="centered")

# Estilo para focar na imagem central
st.markdown("""
    <style>
    .stImage { border-radius: 15px; border: 3px solid #444; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("♟️ Auditoria Flashcards")

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# --- GESTÃO DE ESTADO (INDEX) ---
if 'idx' not in st.session_state:
    st.session_state.idx = 0

# --- BARRA LATERAL: UPLOAD ---
with st.sidebar:
    st.header("📥 Novo Registro")
    uploaded_file = st.file_uploader("Subir Print", type=["jpg", "png", "jpeg"])
    comentario = st.text_area("Insight da Engine:")
    if st.button("Salvar na Auditoria"):
        if uploaded_file and comentario:
            from datetime import datetime
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = os.path.join(IMG_DIR, f"{ts}.jpg")
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with open(img_path.replace(".jpg", ".txt"), "w") as f:
                f.write(comentario)
            st.success("Registrado!")
            st.rerun()

# --- ÁREA DE ESTUDO (O CARROSSEL) ---
images = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
images.sort(reverse=True)

if not images:
    st.info("Nenhuma jogada cadastrada.")
else:
    # Ajustar o index se ele ficar fora dos limites (após exclusão)
    if st.session_state.idx >= len(images):
        st.session_state.idx = 0

    total = len(images)
    current_img = images[st.session_state.idx]
    path = os.path.join(IMG_DIR, current_img)
    txt_path = path.replace(".jpg", ".txt")

    # Contador de progresso
    st.write(f"**Analisando erro {st.session_state.idx + 1} de {total}**")

    # Exibe a Imagem Principal
    st.image(path, use_container_width=True)

    # Exibe o Insight
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            texto = f.read()
        st.warning(f"💡 {texto}")

    # Navegação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Anterior"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()
    with col2:
        if st.button("Próximo ➡️"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    # Gestão do Registro Atual
    with st.expander("⚙️ Opções do Registro"):
        novo_texto = st.text_area("Editar Insight:", value=texto)
        if st.button("Atualizar Texto"):
            with open(txt_path, "w") as f:
                f.write(novo_texto)
            st.success("Atualizado!")
            st.rerun()
        
        if st.button("🗑️ Excluir esta imagem"):
            os.remove(path)
            os.remove(txt_path)
            st.session_state.idx = 0
            st.rerun()
