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

# 2. CSS: CENTRALIZAÇÃO ABSOLUTA E UNIFICAÇÃO
st.markdown("""
    <style>
    /* RESET DE TOPO */
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -85px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 1100px !important; }

    /* ESTÉTICA DARK */
    html, body, [class*="css"] { 
        background-color: #080808 !important; 
        color: #E0E0E0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    .header-container {
        background: linear-gradient(90deg, rgba(10,10,10,0) 0%, rgba(20,20,20,1) 50%, rgba(10,10,10,0) 100%);
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: 15px 0; margin-bottom: 25px;
    }
    .header-text { font-size: 11px; color: #555; text-transform: uppercase; text-align: center; letter-spacing: 4px; margin: 0; }
    .record-counter { color: #D4AF37; font-size: 11px; font-weight: 600; text-align: center; margin-bottom: 5px; }

    .img-display-container { display: flex; justify-content: center; margin-bottom: 25px; }
    .img-display-container img { max-height: 55vh; border: 1px solid #222; border-radius: 4px; box-shadow: 0 20px 60px rgba(0,0,0,1); }

    /* --- A MÁGICA: BARRA DE CONTROLE UNIFICADA --- */
    /* Esse container força o Streamlit a agrupar tudo no centro sem colunas */
    .nav-control-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-bottom: 30px;
    }

    /* Estilo das Setas */
    .nav-btn div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #1A1A1A !important;
        height: 52px !important;
        width: 52px !important;
        border-radius: 50% !important;
        font-size: 22px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .nav-btn div.stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    /* Estilo do Botão Revelar */
    .reveal-btn div.stButton > button {
        background-color: #111 !important;
        color: #D4AF37 !important;
        border: 1px solid #222 !important;
        width: 200px !important;
        height: 52px !important;
        border-radius: 4px !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }

    .revealed-box {
        background-color: #0A0A0A; padding: 20px; border-left: 3px solid #D4AF37;
        text-align: center; max-width: 620px; margin: 0 auto 25px auto; color: #BBB;
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
aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    
    st.markdown(f'<p class="record-counter">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#111; color:#D4AF37; padding:6px 16px; border-radius:4px; border:1px solid #222; font-weight:bold; font-size:13px;">📂 {curr.split("_")[0].replace("-", " ").upper()}</span></div>', unsafe_allow_html=True)

    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="img-display-container"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)
    
    # --- BARRA DE CONTROLE CENTRALIZADA ---
    # Usamos o container para forçar o agrupamento
    st.markdown('<div class="nav-control-bar">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([0.1, 0.2, 0.1], gap="small")
    
    with c1:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.session_state.revelar = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="reveal-btn">', unsafe_allow_html=True)
        if st.button("REVELAR" if not st.session_state.revelar else "OCULTAR", key="btn_rev"):
            st.session_state.revelar = not st.session_state.revelar
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.session_state.revelar = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.revelar:
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f:
                st.markdown(f'<div class="revealed-box">{f.read()}</div>', unsafe_allow_html=True)

# 4. GESTÃO
st.write("")
with st.expander("⚙️ GESTÃO"):
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
    with t2:
        if imgs:
            path_txt_edit = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            txt_at = ""
            if os.path.exists(path_txt_edit):
                with open(path_txt_edit, "r") as f: txt_at = f.read()
            edt_t = st.text_area("Editar:", value=txt_at, key="edit_area")
            if st.button("ATUALIZAR"):
                with open(path_txt_edit, "w") as f: f.write(edt_t); st.rerun()
