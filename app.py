import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (TOPO ZERO - MANTIDO INTEGRALMENTE)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: TOPO PERFEITO + COMPACTAÇÃO DO RODAPÉ
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
        margin-bottom: 10px;
        font-size: 11px;
        text-transform: uppercase;
        text-align: center;
    }

    .record-counter {
        font-family: 'Inter', sans-serif;
        color: #D4AF37;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 10px;
    }

    /* CENTRALIZAÇÃO DO TABULEIRO */
    .centered-image-container {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-bottom: 20px;
    }
    .centered-image-container img {
        max-height: 58vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #222;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* SETAS DE NAVEGAÇÃO */
    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #222 !important;
        height: 55px !important;
        width: 55px !important;
        font-size: 22px !important;
        border-radius: 50% !important;
        display: block;
        margin: 0 auto !important;
    }
    div.stButton > button:hover { border-color: #D4AF37; color: #D4AF37; }

    /* --- COMPACTAÇÃO DA GESTÃO --- */
    .stExpander {
        margin-top: -15px !important; /* Puxa o expander para cima */
        border: 1px solid #1A1A1A !important;
    }

    .stExpander div.stButton > button {
        border-radius: 4px !important;
        width: 100% !important;
        height: auto !important;
        padding: 8px !important;
        font-size: 14px !important;
        background-color: #1A1A1A !important;
        border: 1px solid #333 !important;
    }

    .insight-box {
        background-color: #111;
        padding: 15px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 10px;
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
imgs.sort()

texto_atual = ""
if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    current_number = st.session_state.idx + 1
    
    curr = imgs[st.session_state.idx]
    path_img = os.path.join(IMG_DIR, curr)
    path_txt = path_img.replace(".jpg", ".txt")

    st.markdown(f'<p class="record-counter">REGISTRO {current_number} / {total}</p>', unsafe_allow_html=True)

    img_base64 = get_image_base64(path_img)
    st.markdown(f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>', unsafe_allow_html=True)

    _, b1, b2, _ = st.columns([1, 0.15, 0.15, 1])
    with b1:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()
    with b2:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: texto_atual = f.read()
        st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto_atual}</div>', unsafe_allow_html=True)

# GESTÃO COMPACTADA
st.write("<br>", unsafe_allow_html=True) # Apenas um pulo de linha simples
with st.expander("⚙️ GESTÃO DE DADOS (ADICIONAR / REMOVER / EDITAR)"):
    tab1, tab2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR OU REMOVER ATUAL"])
    
    with tab1:
        novo_f = st.file_uploader("Upload da Imagem", type=["jpg", "png", "jpeg"], key="up_novo")
        novo_t = st.text_area("Insight da Engine:", height=80, key="txt_novo")
        if st.button("SALVAR NOVO REGISTRO", key="btn_salvar"): 
            if novo_f and novo_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                base = os.path.join(IMG_DIR, f"{ts}")
                with open(f"{base}.jpg", "wb") as file: file.write(novo_f.getbuffer())
                with open(f"{base}.txt", "w") as file: file.write(novo_t)
                st.rerun()
    
    with tab2:
        if imgs:
            st.warning(f"Você está editando o Registro {st.session_state.idx + 1}")
            novo_texto = st.text_area("Alterar Texto:", value=texto_atual, key="edit_texto")
            c_e, c_d = st.columns(2)
            with c_e:
                if st.button("ATUALIZAR DADOS", key="btn_update"):
                    with open(path_txt, "w") as file: file.write(novo_texto)
                    st.rerun()
            with c_d:
                if st.button("🗑️ DELETAR ESTE REGISTRO", key="btn_delete"):
                    os.remove(path_img)
                    if os.path.exists(path_txt): os.remove(path_txt)
                    st.session_state.idx = 0
                    st.rerun()
