import streamlit as st
import os
from datetime import datetime

# 1. SUA CONFIGURAÇÃO BASE (TOPO ZERO)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: SUA BASE FUNCIONAL + AJUSTE DE PROXIMIDADE "COLADA"
st.markdown("""
    <style>
    /* SEU FIX DO TOPO (MANTIDO) */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 900px !important; /* REDUZIDO PARA COLAR AS SETAS */
    }
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container {
        padding-top: 0rem !important;
    }

    /* ESTÉTICA DARK */
    html, body, [class*="css"] {
        background-color: #080808 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        letter-spacing: 2px;
        color: #444;
        margin-top: 0px !important;
        margin-bottom: 10px;
        font-size: 10px;
        text-transform: uppercase;
        text-align: center;
    }

    /* IMAGEM CENTRALIZADA */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    img {
        max-height: 62vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    .insight-box {
        background-color: #0E0E0E;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 15px;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* BOTÕES LATERAIS CIRCULARES */
    div.stButton > button {
        background-color: transparent !important;
        color: #555 !important;
        border: 1px solid #1A1A1A !important;
        height: 60px !important;
        width: 60px !important;
        font-size: 22px !important;
        transition: 0.2s;
        border-radius: 50% !important;
        margin-top: 180px;
        display: block;
    }
    
    /* XEQUE-MATE NA DISTÂNCIA: Cola as setas na imagem */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] {
        align-items: flex-end !important;
    }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] {
        align-items: flex-start !important;
    }

    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
    }

    /* Limpeza de UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título
st.markdown('<p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Aguardando input...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    path_img = os.path.join(IMG_DIR, curr)
    path_txt = path_img.replace(".jpg", ".txt")

    # PROPORÇÃO COMPACTA: [1 lateral, 5 centro, 1 lateral]
    c_ant, c_mid, c_prox = st.columns([1, 5, 1], gap="small")
    
    with c_ant:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with c_mid:
        st.image(path_img, use_container_width=True)
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f: texto = f.read()
            st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto}</div>', unsafe_allow_html=True)

    with c_prox:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

# Gestão Oculta
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("DADOS E PROPRIEDADES"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Novo Registro", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight da Engine:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                p = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(p, "wb") as file: file.write(f.getbuffer())
                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar Texto:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(path_txt, "w") as file: file.write(novo)
                st.rerun()
            if st.button("🗑️ Deletar"):
                os.remove(path_img); os.remove(path_txt)
                st.session_state.idx = 0
                st.rerun()
