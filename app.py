import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (TOPO ZERO - MANTIDO INTEGRALMENTE)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# Função para converter imagem em base64
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 2. CSS: SEU FIX DE TOPO + TRAVA DE EIXO PARA AS SETAS
st.markdown("""
    <style>
    /* --- SEU FIX DO TOPO (INALTEÁVEL) --- */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1100px !important;
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
        margin-bottom: 20px;
        font-size: 11px;
        text-transform: uppercase;
        text-align: center;
    }

    /* --- CENTRALIZAÇÃO ABSOLUTA DA IMAGEM --- */
    .centered-image-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-bottom: 20px;
    }
    
    .centered-image-container img {
        max-height: 60vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #222;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* BOTÕES CENTRALIZADOS E TRAVADOS NO EIXO */
    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #222 !important;
        height: 55px !important;
        width: 55px !important;
        font-size: 22px !important;
        transition: 0.2s;
        border-radius: 50% !important;
        display: block;
        margin: 0 auto !important;
    }
    
    /* ESTE AJUSTE GARANTE QUE AS COLUNAS NÃO PASSEM DA LARGURA DA IMAGEM */
    div[data-testid="stHorizontalBlock"] {
        max-width: 1100px !important;
        margin: 0 auto !important;
    }

    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
    }

    .insight-box {
        background-color: #111;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 20px;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

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

    # --- 1. TABULEIRO ---
    img_base64 = get_image_base64(path_img)
    st.markdown(
        f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>',
        unsafe_allow_html=True
    )

    # --- 2. CONTROLES (SETAS) ABAIXO ---
    # Agora travados no mesmo eixo de 1100px
    _, b1, b2, _ = st.columns([1, 0.15, 0.15, 1])
    with b1:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()
    with b2:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    # --- 3. ANÁLISE ---
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: texto = f.read()
        st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto}</div>', unsafe_allow_html=True)

# GESTÃO OCULTA
st.write("<br>"*3, unsafe_allow_html=True)
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
