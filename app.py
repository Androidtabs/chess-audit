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

# 2. CSS: DESIGN DE ALTA FIDELIDADE (CÉDULA DE COMANDO)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -85px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 1000px !important; }

    html, body, [class*="css"] { 
        background-color: #050505 !important; 
        color: #E0E0E0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* BARRA SUPERIOR */
    .header-bar {
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid #1a1a1a;
        margin-bottom: 30px;
        background: linear-gradient(180deg, #0a0a0a 0%, #050505 100%);
    }
    .header-title { font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 5px; margin: 0; }

    /* TABULEIRO */
    .board-container { display: flex; justify-content: center; margin-bottom: 30px; }
    .board-container img { 
        max-height: 58vh; border: 2px solid #1a1a1a; border-radius: 6px; 
        box-shadow: 0 40px 100px rgba(0,0,0,1); 
    }

    /* --- A BARRA DE COMANDO (ESTILO DASHBOARD) --- */
    .control-deck {
        display: flex;
        justify-content: center;
        align-items: center;
        background: #0f0f0f;
        border: 1px solid #222;
        border-radius: 50px;
        padding: 8px 15px;
        width: fit-content;
        margin: 0 auto 30px auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Botões de Seta */
    .deck-btn-side div.stButton > button {
        background: transparent !important;
        color: #D4AF37 !important;
        border: none !important;
        font-size: 28px !important;
        height: 45px !important;
        width: 45px !important;
        padding: 0 !important;
        transition: 0.3s;
    }
    .deck-btn-side div.stButton > button:hover { transform: scale(1.2); color: #fff !important; }

    /* Botão Central (Revelar) */
    .deck-btn-main div.stButton > button {
        background: linear-gradient(180deg, #1a1a1a 0%, #111 100%) !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
        border-radius: 30px !important;
        width: 180px !important;
        height: 40px !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        margin: 0 10px !important;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.05);
    }
    .deck-btn-main div.stButton > button:hover { border-color: #D4AF37 !important; box-shadow: 0 0 15px rgba(212, 175, 55, 0.2); }

    /* CAIXA DE ANÁLISE PROFISSIONAL */
    .analysis-card {
        background: #0a0a0a;
        border-top: 1px solid #D4AF37;
        padding: 25px;
        max-width: 600px;
        margin: 0 auto 40px auto;
        text-align: center;
        font-size: 15px;
        line-height: 1.7;
        color: #999;
        border-radius: 0 0 10px 10px;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'revelar' not in st.session_state: st.session_state.revelar = False

st.markdown('<div class="header-bar"><p class="header-title">Chess Strategy Lab // Estudo de Aberturas</p></div>', unsafe_allow_html=True)

imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    nome = curr.split("_")[0].replace("-", " ").upper()
    
    st.markdown(f'<p style="text-align:center; color:#555; font-size:11px; margin-bottom:5px;">{st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-bottom:20px;"><span style="color:#D4AF37; font-weight:800; letter-spacing:2px; font-size:14px;">{nome}</span></div>', unsafe_allow_html=True)

    # Imagem do Tabuleiro
    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="board-container"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)
    
    # --- O DECK DE CONTROLE (UNIFICADO) ---
    st.markdown('<div class="control-deck">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        st.markdown('<div class="deck-btn-side">', unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx -= 1
            st.session_state.revelar = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="deck-btn-main">', unsafe_allow_html=True)
        label = "OCULTAR" if st.session_state.revelar else "VER ANÁLISE"
        if st.button(label, key="btn_rev"):
            st.session_state.revelar = not st.session_state.revelar
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="deck-btn-side">', unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx += 1
            st.session_state.revelar = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.revelar:
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f:
                st.markdown(f'<div class="analysis-card">{f.read()}</div>', unsafe_allow_html=True)

# 4. GESTÃO (SIMPLIFICADA NO VISUAL)
st.write("")
with st.expander("⚙️ CONFIGURAÇÕES DA BASE"):
    # Código de gestão mantido
    st.markdown("<small>Área de administração para novos registros.</small>", unsafe_allow_html=True)
    # ... (o código de cadastro e edição continua aqui abaixo)
