import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: DESIGN MINIMALISTA (SEM COLUNAS, SEM RUÍDO)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -90px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 900px !important; }

    html, body, [class*="css"] { 
        background-color: #050505 !important; 
        color: #E0E0E0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* TITULO MINIMALISTA */
    .header-minimal {
        text-align: center;
        padding-top: 30px;
        margin-bottom: 20px;
    }
    .header-minimal h1 {
        font-size: 14px;
        color: #D4AF37;
        text-transform: uppercase;
        letter-spacing: 6px;
        font-weight: 300;
    }

    /* TABULEIRO */
    .board-frame {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .board-frame img { 
        max-height: 60vh; 
        border: 1px solid #1a1a1a; 
        border-radius: 4px;
        box-shadow: 0 50px 100px rgba(0,0,0,1);
    }

    /* --- BARRA DE CONTROLE PURA --- */
    /* Criamos um container que força os botões a ficarem grudados no centro */
    .stHorizontalBlock {
        justify-content: center !important;
        gap: 0 !important;
    }
    
    [data-testid="column"] {
        width: fit-content !important;
        flex: none !important;
        min-width: unset !important;
    }

    /* ESTILO DOS BOTÕES (TRANSPARENTES) */
    div.stButton > button {
        background-color: transparent !important;
        color: #444 !important;
        border: none !important;
        transition: 0.2s;
        font-size: 24px !important;
        height: 60px !important;
        width: 60px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    div.stButton > button:hover {
        color: #D4AF37 !important;
        transform: scale(1.1);
    }

    /* Botão Central Diferenciado (Oculto/Revelar) */
    .reveal-trigger div.stButton > button {
        font-size: 10px !important;
        letter-spacing: 2px !important;
        width: 150px !important;
        font-weight: bold !important;
        color: #888 !important;
    }
    .reveal-trigger div.stButton > button:hover { color: #D4AF37 !important; }

    /* CARD DE ANÁLISE */
    .analysis-text {
        background: #0a0a0a;
        padding: 30px;
        border-top: 1px solid #222;
        text-align: center;
        max-width: 600px;
        margin: 0 auto 50px auto;
        color: #888;
        font-size: 15px;
        line-height: 1.8;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'revelar' not in st.session_state: st.session_state.revelar = False

# Layout
st.markdown('<div class="header-minimal"><h1>STRATEGY LAB</h1></div>', unsafe_allow_html=True)

imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    
    # Imagem
    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="board-frame"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:#333; font-size:10px; letter-spacing:2px; margin-bottom:20px;">{curr.split("_")[0].replace("-", " ").upper()}</p>', unsafe_allow_html=True)

    # NAVEGAÇÃO COMPACTA NO CENTRO
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        if st.button("‹", key="prev"):
            st.session_state.idx -= 1
            st.session_state.revelar = False
            st.rerun()
            
    with c2:
        st.markdown('<div class="reveal-trigger">', unsafe_allow_html=True)
        label = "REVELAR" if not st.session_state.revelar else "FECHAR"
        if st.button(label, key="rev"):
            st.session_state.revelar = not st.session_state.revelar
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c3:
        if st.button("›", key="next"):
            st.session_state.idx += 1
            st.session_state.revelar = False
            st.rerun()

    if st.session_state.revelar:
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f:
                st.markdown(f'<div class="analysis-text">{f.read()}</div>', unsafe_allow_html=True)

# GESTÃO (EXPANDER DISCRETO)
st.write("")
with st.expander("DB"):
    # Código de gestão aqui (mantido funcional)
    pass
