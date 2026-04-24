import streamlit as st
import os
from datetime import datetime

# Configuração de página para ocupar o máximo de espaço útil
st.set_page_config(page_title="Audit", layout="centered", initial_sidebar_state="collapsed")

# CSS Avançado para remover espaços em branco e fixar o layout
st.markdown("""
    <style>
    /* Remove o cabeçalho oficial do Streamlit e o espaço no topo */
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 550px;
    }

    /* Título Minimalista e Colado no Topo */
    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 200;
        letter-spacing: 3px;
        color: #666;
        text-align: center;
        margin-bottom: 10px;
        font-size: 14px;
        text-transform: uppercase;
    }

    /* Ajuste da Imagem para caber na tela sem scroll */
    img {
        max-height: 45vh; /* Limita a imagem a 45% da altura da tela */
        object-fit: contain;
        border-radius: 5px;
        border: 1px solid #333;
    }

    /* Box de Insight Compacto */
    .insight-box {
        background-color: #161B22;
        padding: 12px;
        border-radius: 0 0 8px 8px;
        border-bottom: 2px solid #D4AF37;
        font-size: 14px;
        color: #D1D5DA;
        margin-top: -5px; /* Cola na imagem */
    }

    /* Botões de Navegação Ultra-Slim */
    div.stButton > button {
        background-color: #1a1a1a;
        color: #fff;
        border: 1px solid #333;
        height: 100%;
        min-height: 250px; /* Botão alto para facilitar o toque no celular */
        width: 100%;
        font-size: 30px;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
    }

    /* Esconde elementos de sistema */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título discreto
st.markdown('<p class="header-text">Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Aguardando dados...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    p = os.path.join(IMG_DIR, curr)
    t_p = p.replace(".jpg", ".txt")

    # Grid de navegação lateral colado na imagem
    col_ant, col_mid, col_prox = st.columns([0.4, 4, 0.4])
    
    with col_ant:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with col_mid:
        st.image(p, use_container_width=True)
        if os.path.exists(t_p):
            with open(t_p, "r") as f: texto = f.read()
            st.markdown(f'<div class="insight-box">{texto}</div>', unsafe_allow_html=True)

    with col_prox:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#444; font-size:10px; margin-top:5px;'>{st.session_state.idx + 1} / {len(imgs)}</p>", unsafe_allow_html=True)

# Rodapé minimalista para gestão
with st.expander("🛠 GESTÃO"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Novo Print", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as file: file.write(f.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar Texto:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(t_p, "w") as file: file.write(novo)
                st.rerun()
            if st.button("Deletar"):
                os.remove(p); os.remove(t_p)
                st.session_state.idx = 0
                st.rerun()
