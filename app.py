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

# 2. CSS: DESIGN DE INTERFACE PROFISSIONAL (HUD STYLE)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -85px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 1200px !important; }

    html, body, [class*="css"] { background-color: #080808 !important; color: #E0E0E0 !important; }

    /* CABEÇALHO SUTIL */
    .header-container {
        background: linear-gradient(90deg, rgba(10,10,10,0) 0%, rgba(20,20,20,1) 50%, rgba(10,10,10,0) 100%);
        border-bottom: 1px solid rgba(212, 175, 55, 0.1);
        padding: 10px 0; margin-bottom: 20px;
    }
    .header-text { font-size: 11px; color: #444; text-transform: uppercase; text-align: center; letter-spacing: 3px; margin: 0; }

    /* CONTAINER PRINCIPAL DO TABULEIRO COM NAVEGAÇÃO */
    .main-board-area {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }

    .board-img {
        max-height: 60vh;
        border: 1px solid #222;
        border-radius: 4px;
        box-shadow: 0 30px 80px rgba(0,0,0,1);
    }

    /* ESTILO DAS SETAS LATERAIS */
    .side-nav div.stButton > button {
        background-color: rgba(20, 20, 20, 0.5) !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
        height: 60px !important;
        width: 40px !important;
        border-radius: 4px !important;
        font-size: 20px !important;
        transition: 0.3s;
    }
    .side-nav div.stButton > button:hover {
        background-color: #D4AF37 !important;
        color: #000 !important;
        border-color: #D4AF37 !important;
    }

    /* BOTÃO REVELAR (SOZINHO E CENTRALIZADO) */
    .reveal-btn-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .reveal-btn-container div.stButton > button {
        width: 300px !important;
        height: 45px !important;
        background-color: #111 !important;
        color: #D4AF37 !important;
        border: 1px solid #222 !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* CAIXA DE ANÁLISE */
    .analysis-box {
        background-color: #0A0A0A;
        padding: 20px;
        border-left: 3px solid #D4AF37;
        max-width: 600px;
        margin: 0 auto 30px auto;
        text-align: center;
        font-size: 15px;
        color: #BBB;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'revelar' not in st.session_state: st.session_state.revelar = False

st.markdown('<div class="header-container"><p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p></div>', unsafe_allow_html=True)

imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    
    # ESTRUTURA DE NAVEGAÇÃO: SETA | IMAGEM | SETA
    col_l, col_img, col_r = st.columns([1, 4, 1])
    
    with col_l:
        st.write("<div style='height: 25vh;'></div>", unsafe_allow_html=True) # Alinha a seta no meio da altura da imagem
        st.markdown('<div class="side-nav">', unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx -= 1
            st.session_state.revelar = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_img:
        st.markdown(f'<p style="text-align:center; color:#D4AF37; font-size:12px; font-weight:bold; margin-bottom:10px;">{curr.split("_")[0].replace("-", " ").upper()} ({st.session_state.idx + 1}/{len(imgs)})</p>', unsafe_allow_html=True)
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div style="display:flex; justify-content:center;"><img src="data:image/jpeg;base64,{img_64}" class="board-img"></div>', unsafe_allow_html=True)

    with col_r:
        st.write("<div style='height: 25vh;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="side-nav">', unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx += 1
            st.session_state.revelar = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # BOTÃO REVELAR CENTRALIZADO ABAIXO
    st.markdown('<div class="reveal-btn-container">', unsafe_allow_html=True)
    if st.button("REVELAR ANÁLISE" if not st.session_state.revelar else "OCULTAR", key="btn_rev"):
        st.session_state.revelar = not st.session_state.revelar
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.revelar:
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f:
                st.markdown(f'<div class="analysis-box">{f.read()}</div>', unsafe_allow_html=True)

# 4. GESTÃO
st.write("")
with st.expander("⚙️ GESTÃO"):
    # (Mantendo seu código de gestão de dados intacto aqui)
    aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))
    t1, t2 = st.tabs(["➕ NOVO", "📝 EDITAR"])
    with t1:
        escolha = st.selectbox("Abertura:", ["-- Selecione --"] + aberturas_existentes + ["[ + NOVA ]"])
        n_f = st.text_input("Variante:") if escolha == "[ + NOVA ]" else (escolha if escolha != "-- Selecione --" else "")
        u_f = st.file_uploader("Captura:", type=["jpg", "png", "jpeg"])
        u_t = st.text_area("Análise:")
        if st.button("SALVAR"): 
            if u_f and u_t and n_f:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.txt"), "w") as f: f.write(u_t)
                st.rerun()
