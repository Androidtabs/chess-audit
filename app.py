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

# 2. CSS: FOCO EM ESTABILIDADE E ALINHAMENTO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -85px !important; }
    
    html, body, [class*="css"] { 
        background-color: #080808 !important; 
        color: #E0E0E0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* TITULO */
    .header-box {
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid #1a1a1a;
        margin-bottom: 20px;
    }
    .header-box h1 {
        font-size: 12px;
        color: #444;
        text-transform: uppercase;
        letter-spacing: 5px;
    }

    /* TABULEIRO */
    .board-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-height: 60vh;
        border: 1px solid #222;
        border-radius: 4px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }

    /* CENTRALIZAÇÃO DOS BOTÕES */
    .stButton > button {
        width: 100% !important;
        background-color: #111 !important;
        color: #D4AF37 !important;
        border: 1px solid #222 !important;
        border-radius: 4px !important;
        height: 45px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
    }
    .stButton > button:hover {
        border-color: #D4AF37 !important;
        background-color: #161616 !important;
    }

    /* TEXTO DA ANÁLISE */
    .analysis-container {
        background-color: #0a0a0a;
        padding: 20px;
        border-left: 3px solid #D4AF37;
        margin-top: 20px;
        text-align: center;
        color: #999;
        font-size: 15px;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'revelar' not in st.session_state: st.session_state.revelar = False

# Layout do Topo
st.markdown('<div class="header-box"><h1>CHESS STRATEGY LAB</h1></div>', unsafe_allow_html=True)

imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    
    # Nome da Abertura
    st.markdown(f'<p style="text-align:center; color:#D4AF37; font-weight:bold; letter-spacing:1px;">📂 {curr.split("_")[0].replace("-", " ").upper()}</p>', unsafe_allow_html=True)

    # Imagem
    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<img src="data:image/jpeg;base64,{img_64}" class="board-img">', unsafe_allow_html=True)
    
    st.write("") # Espaçador

    # NAVEGAÇÃO (3 COLUNAS SIMPLES E ESTÁVEIS)
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        if st.button("‹ ANTERIOR"):
            st.session_state.idx -= 1
            st.session_state.revelar = False
            st.rerun()
            
    with c2:
        label = "REVELAR ANÁLISE" if not st.session_state.revelar else "OCULTAR"
        if st.button(label):
            st.session_state.revelar = not st.session_state.revelar
            st.rerun()
        
    with c3:
        if st.button("PRÓXIMO ›"):
            st.session_state.idx += 1
            st.session_state.revelar = False
            st.rerun()

    # Mostrar Análise
    if st.session_state.revelar:
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f:
                st.markdown(f'<div class="analysis-container">{f.read()}</div>', unsafe_allow_html=True)

# GESTÃO
st.write("---")
with st.expander("⚙️ GESTÃO DE DADOS"):
    aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))
    t1, t2 = st.tabs(["➕ NOVO", "📝 EDITAR"])
    with t1:
        escolha = st.selectbox("Abertura:", ["-- Selecione --"] + aberturas_existentes + ["[ + NOVA ]"])
        n_f = st.text_input("Variante:") if escolha == "[ + NOVA ]" else (escolha if escolha != "-- Selecione --" else "")
        u_f = st.file_uploader("Imagem:", type=["jpg", "png", "jpeg"])
        u_t = st.text_area("Análise:")
        if st.button("SALVAR REGISTRO"): 
            if u_f and u_t and n_f:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.txt"), "w") as f: f.write(u_t)
                st.rerun()
    with t2:
        if imgs:
            path_txt_edit = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            txt_at = ""
            if os.path.exists(path_txt_edit):
                with open(path_txt_edit, "r") as f: txt_at = f.read()
            edt_t = st.text_area("Editar Análise:", value=txt_at)
            if st.button("ATUALIZAR"):
                with open(path_txt_edit, "w") as f: f.write(edt_t); st.rerun()
