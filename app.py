import streamlit as st
import os
from datetime import datetime

# 1. Configuração de Página (Mantendo o seu layout wide que funcionou)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: Estrutura que você validou + Estética Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&family=JetBrains+Mono&display=swap');

    /* O SEU FIX DE TOPO */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -35px !important;
        max-width: 1100px !important;
    }
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
    }

    /* ESTÉTICA MODERNA */
    html, body, [class*="css"] {
        background-color: #050505 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Título Elegante */
    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 200;
        letter-spacing: 6px;
        color: #FFFFFF;
        margin-bottom: 15px;
        font-size: 14px;
        text-transform: uppercase;
        text-align: center;
        opacity: 0.8;
    }

    /* Imagem (Destaque sem distorção) */
    img {
        max-height: 60vh !important;
        width: auto !important;
        margin: 0 auto;
        display: block;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
    }

    /* Box de Análise Organizada */
    .insight-card {
        background-color: #0A0A0A;
        padding: 25px 40px;
        border-radius: 4px;
        border: 1px solid #161616;
        border-top: 2px solid #D4AF37; /* Detalhe em Dourado */
        margin: 15px auto;
        max-width: 850px;
    }
    .insight-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #D4AF37;
        margin-bottom: 8px;
        letter-spacing: 2px;
    }
    .insight-content {
        font-size: 16px;
        line-height: 1.7;
        color: #CCCCCC;
    }

    /* Botões Laterais (Minimalistas) */
    div.stButton > button {
        background-color: transparent !important;
        color: #333 !important;
        border: 1px solid #111 !important;
        height: 500px !important;
        width: 100% !important;
        font-size: 30px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Header
st.markdown('<p class="header-text">Chess Protocol // Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Sistema Online // Aguardando Lançamento de Dados")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr)
    p_txt = p_img.replace(".jpg", ".txt")

    # Layout Principal
    c_ant, c_mid, c_prox = st.columns([0.6, 8, 0.6])
    
    with c_ant:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with c_mid:
        st.image(p_img, use_container_width=True)
        if os.path.exists(p_txt):
            with open(p_txt, "r") as f: texto = f.read()
            st.markdown(f'''
                <div class="insight-card">
                    <div class="insight-label">ANÁLISE TÉCNICA //</div>
                    <div class="insight-content">{texto}</div>
                </div>
            ''', unsafe_allow_html=True)

    with c_prox:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

# Gestão Oculta no Rodapé
st.write("<br>"*3, unsafe_allow_html=True)
with st.expander("TERMINAL DE DADOS"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Novo Registro", type=["jpg", "png", "jpeg"])
        c = st.text_area("Comentário da Engine:")
        if st.button("Salvar Registro"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as file: file.write(f.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar Atual:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar Dados"):
                with open(p_txt, "w") as file: file.write(novo)
                st.rerun()
            if st.button("🗑️ Deletar Registro"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
