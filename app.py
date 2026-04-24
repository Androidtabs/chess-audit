import streamlit as st
import os
from datetime import datetime

# Configuração para ocupar menos espaço e evitar scroll
st.set_page_config(page_title="Audit - Vagner", layout="centered")

# CSS Customizado para compactar a interface
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stImage { border-radius: 10px; border: 2px solid #444; }
    /* Estilo dos botões laterais */
    div.stButton > button {
        height: 100px;
        background-color: #333;
        color: white;
        font-size: 20px;
        border-radius: 10px;
    }
    .insight-box {
        background-color: #262730;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-top: 5px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# --- ESTADO DA SESSÃO ---
if 'idx' not in st.session_state:
    st.session_state.idx = 0

# --- BARRA LATERAL (CADASTRO) ---
with st.sidebar:
    st.header("📥 Novo")
    f = st.file_uploader("Print", type=["jpg", "png", "jpeg"])
    c = st.text_area("Insight:")
    if st.button("Salvar Registro"):
        if f and c:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            p = os.path.join(IMG_DIR, f"{ts}.jpg")
            with open(p, "wb") as file:
                file.write(f.getbuffer())
            with open(p.replace(".jpg", ".txt"), "w") as file:
                file.write(c)
            st.rerun()

# --- ÁREA PRINCIPAL (FLASHCARD) ---
imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Suba um print para começar.")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    p = os.path.join(IMG_DIR, curr)
    t_p = p.replace(".jpg", ".txt")

    # Layout de 3 colunas para navegação lateral
    # [ Ant ] [ Imagem ] [ Prox ]
    col_ant, col_mid, col_prox = st.columns([0.5, 3, 0.5])

    with col_ant:
        st.write("") # Espaço para alinhar ao centro da imagem
        st.write("")
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with col_mid:
        st.image(p, use_container_width=True)
        if os.path.exists(t_p):
            with open(t_p, "r") as file:
                texto = file.read()
            # Exibição do insight em caixa compacta
            st.markdown(f'<div class="insight-box">💡 {texto}</div>', unsafe_allow_html=True)

    with col_prox:
        st.write("") 
        st.write("")
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    # Informação de progresso e gestão escondida
    st.caption(f"Registro {st.session_state.idx + 1} de {total}")
    
    with st.expander("⚙️ Gestão"):
        novo = st.text_area("Editar:", value=texto)
        if st.button("Atualizar"):
            with open(t_p, "w") as file: file.write(novo)
            st.rerun()
        if st.button("🗑️ Excluir"):
            os.remove(p); os.remove(t_p)
            st.rerun()
