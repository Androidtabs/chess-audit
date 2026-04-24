import streamlit as st
import os
from datetime import datetime

# Configuração de página - MANTENDO SEU LAYOUT ORIGINAL
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# CSS: MANTENDO SEUS SELETORES QUE FUNCIONAM + REFINAMENTO ESTÉTICO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap');

    /* 1. SEUS FIXES DE TOPO - NÃO MEXER */
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

    /* 2. ESTÉTICA MODERNA (DEEP BLACK) */
    html, body, [class*="css"] {
        background-color: #050505 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Título Elegante */
    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        letter-spacing: 5px;
        color: #FFFFFF;
        margin-top: 0px !important;
        margin-bottom: 15px;
        font-size: 12px;
        text-transform: uppercase;
        text-align: center;
        opacity: 0.6;
    }

    /* Imagem (Destaque Profissional) */
    img {
        max-height: 62vh !important;
        width: auto !important;
        margin: 0 auto;
        display: block;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 15px 40px rgba(0,0,0,0.8);
    }

    /* Box de Insight Estilo Terminal */
    .insight-box {
        background-color: #0E0E0E;
        padding: 25px;
        border-radius: 4px;
        border-left: 3px solid #D4AF37; /* Detalhe em Ouro */
        font-size: 15px;
        color: #CCCCCC;
        margin-top: 15px;
        line-height: 1.6;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }

    /* Botões Laterais (Mais finos e integrados) */
    div.stButton > button {
        background-color: transparent !important;
        color: #333 !important;
        border: 1px solid #111 !important;
        height: 500px !important;
        width: 100% !important;
        font-size: 30px !important;
        transition: 0.4s ease;
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: rgba(212, 175, 55, 0.02) !important;
    }

    /* Rodapé e Menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título Original
st.markdown('<p class="header-text">Chess Protocol // Estudo de Aberturas</p>', unsafe_allow_html=True)

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

    # MANTENDO SEU DISPLAY CENTRAL DE 3 COLUNAS
    c_ant, c_mid, c_prox = st.columns([0.5, 8, 0.5])
    
    with c_ant:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with c_mid:
        st.image(path_img, use_container_width=True)
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f: texto = f.read()
            st.markdown(f'''
                <div class="insight-box">
                    <span style="font-family:'JetBrains Mono'; font-size:10px; color:#D4AF37; letter-spacing:2px;">ANÁLISE TÉCNICA //</span><br>
                    {texto}
                </div>
            ''', unsafe_allow_html=True)

    with c_prox:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

# Gestão Oculta Original
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
