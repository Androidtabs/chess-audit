import streamlit as st
import os
from datetime import datetime

# Configurações de Interface
st.set_page_config(page_title="Chess Audit", layout="centered", initial_sidebar_state="collapsed")

# CSS: Elegância Austera v1.5
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B0E11;
        color: #B9BBBE;
    }

    .main .block-container {
        padding-top: 3rem;
        max-width: 650px;
    }

    /* Título Minimalista */
    .header-title {
        font-weight: 200;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 40px;
        font-size: 22px;
    }

    /* Tabuleiro / Imagem */
    .stImage {
        border-radius: 2px;
        border: 1px solid #2F3336;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    /* Box de Insight: Estilo Dark Minimal */
    .insight-container {
        background-color: #161B22;
        padding: 18px;
        border-radius: 4px;
        border-top: 1px solid #30363D;
        margin-top: 20px;
        font-size: 15px;
        line-height: 1.6;
        color: #D1D5DA;
    }

    /* Navegação Invisível / Botões Limpos */
    div.stButton > button {
        background-color: transparent;
        color: #586069;
        border: 1px solid #30363D;
        height: 50px;
        width: 50px;
        transition: 0.2s;
        font-size: 20px;
        border-radius: 4px;
    }

    div.stButton > button:hover {
        border-color: #58a6ff;
        color: #58a6ff;
        background-color: #161B22;
    }

    /* Esconder Sidebar e Menus */
    [data-testid="stSidebar"] { display: none; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Header
st.markdown('<h1 class="header-title">ESTUDO DE ABERTURAS</h1>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Sistema pronto. Aguardando dados de abertura.")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    p = os.path.join(IMG_DIR, curr)
    t_p = p.replace(".jpg", ".txt")

    # Interface de Análise
    col_ant, col_mid, col_prox = st.columns([0.4, 4, 0.4])
    
    with col_ant:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with col_mid:
        st.image(p, use_container_width=True)
        if os.path.exists(t_p):
            with open(t_p, "r") as file: texto = file.read()
            st.markdown(f'<div class="insight-container">{texto}</div>', unsafe_allow_html=True)

    with col_prox:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#30363D; font-size:11px; margin-top:10px;'>{st.session_state.idx + 1} / {total}</p>", unsafe_allow_html=True)

st.write("<br>"*4, unsafe_allow_html=True)

# Área de Gestão (Discreta no final da página)
with st.expander("Gereneciamento de Dados"):
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Novo Lançamento")
        f = st.file_uploader("Arquivo", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight Técnico:")
        if st.button("Salvar Registro"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as file: file.write(f.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        st.caption("Edição de Fluxo")
        if imgs:
            novo = st.text_area("Corrigir Texto:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(t_p, "w") as file: file.write(novo)
                st.rerun()
            if st.button("Deletar"):
                os.remove(p); os.remove(t_p)
                st.session_state.idx = 0
                st.rerun()
