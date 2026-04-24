import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (SUA VERSÃO DE OURO)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: TOPO ZERO + NAVEGAÇÃO CENTRAL + GESTÃO BLINDADA
st.markdown("""
    <style>
    /* --- ZERANDO O TOPO (FIX DEFINITIVO) --- */
    [data-testid="stHeader"] {display: none !important;}
    
    .main .block-container { 
        padding-top: 0.5rem !important; 
        padding-bottom: 0rem !important; 
        margin-top: -50px !important; /* Puxa o conteúdo para o limite superior */
        max-width: 1100px !important; 
    }
    
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
    }

    /* ESTÉTICA DARK */
    html, body, [class*="css"] { 
        background-color: #080808 !important; 
        color: #E0E0E0 !important; 
        font-family: 'Inter', sans-serif;
    }
    
    .header-text { 
        font-size: 11px; 
        color: #444; 
        text-transform: uppercase; 
        text-align: center; 
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    
    .record-counter { color: #D4AF37; font-size: 12px; font-weight: 600; text-align: center; margin-bottom: 5px; }
    
    .opening-tag {
        background-color: #1A1A1A;
        color: #D4AF37;
        padding: 5px 15px;
        border-radius: 4px;
        border: 1px solid #333;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }

    .centered-image-container { display: flex; justify-content: center; margin-bottom: 20px; }
    .centered-image-container img { max-height: 58vh; border: 1px solid #222; box-shadow: 0 20px 50px rgba(0,0,0,0.9); }
    
    /* --- SETAS DE NAVEGAÇÃO (CÍRCULOS) --- */
    /* Seletor específico para as setas de cima não afetar os botões de baixo */
    .main [data-testid="column"] div.stButton > button { 
        background: transparent !important; 
        color: #666 !important; 
        border: 1px solid #222 !important; 
        height: 55px !important; 
        width: 55px !important; 
        border-radius: 50% !important; 
        font-size: 22px !important;
        display: block;
        margin: 0 auto !important;
    }
    .main [data-testid="column"] div.stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    /* --- FIX DOS BOTÕES DE GESTÃO NO EXPANDER --- */
    .stExpander div.stButton > button {
        border-radius: 4px !important;
        width: 100% !important;
        height: 45px !important;
        font-size: 14px !important;
        background-color: #1A1A1A !important;
        text-transform: uppercase !important;
        border: 1px solid #333 !important;
    }

    .insight-box { background: #111; padding: 15px; border-bottom: 2px solid #D4AF37; text-align: center; max-width: 600px; margin: 10px auto 15px auto; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título colado
st.markdown('<p class="header-text">Chess Strategy Lab // Sistema de Auditoria</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort()

# Lista dinâmica de aberturas
aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    nome_exibicao = curr.split("_")[0].replace("-", " ")
    
    st.markdown(f'<p class="record-counter">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="opening-tag">📂 {nome_exibicao}</span></div>', unsafe_allow_html=True)

    img_base64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>', unsafe_allow_html=True)

    # NAVEGAÇÃO CENTRALIZADA
    c1, c2, c3, c4 = st.columns([1, 0.08, 0.08, 1])
    with c2:
        if st.button("‹", key="prev"): 
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()
    with c3:
        if st.button("›", key="next"): 
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: 
            st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {f.read()}</div>', unsafe_allow_html=True)

st.write("")
with st.expander("⚙️ GESTÃO DE DADOS (CADASTRAR ABERTURAS)"):
    t1, t2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR ATUAL"])
    with t1:
        opcoes = ["-- Selecione uma existente --"] + aberturas_existentes + ["[ + CADASTRAR NOVA ]"]
        escolha = st.selectbox("Escolha a Abertura do Adversário:", opcoes)
        nome_final = st.text_input("Nome da Nova Abertura:") if escolha == "[ + CADASTRAR NOVA ]" else (escolha if escolha != "-- Selecione uma existente --" else "")
        n_f = st.file_uploader("Imagem:", type=["jpg", "png", "jpeg"])
        n_t = st.text_area("Insight:")
        if st.button("SALVAR REGISTRO"): 
            if n_f and n_t and nome_final:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_limpo = nome_final.replace(" ", "-").strip()
                base = os.path.join(IMG_DIR, f"{nome_limpo}_{ts}")
                with open(f"{base}.jpg", "wb") as f: f.write(n_f.getbuffer())
                with open(f"{base}.txt", "w") as f: f.write(n_t)
                st.rerun()
    with t2:
        if imgs:
            edt_t = st.text_area("Alterar Insight:", value="", key="edit_area")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("ATUALIZAR DADOS"):
                    with open(os.path.join(IMG_DIR, curr.replace(".jpg", ".txt")), "w") as f: f.write(edt_t)
                    st.rerun()
            with c2:
                if st.button("🗑️ DELETAR"):
                    os.remove(os.path.join(IMG_DIR, curr))
                    os.remove(os.path.join(IMG_DIR, curr.replace(".jpg", ".txt")))
                    st.session_state.idx = 0
                    st.rerun()
