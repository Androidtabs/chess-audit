import streamlit as st
import os
from datetime import datetime

# 1. SUA CONFIGURAÇÃO BASE (TOPO ZERO)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: SUA BASE FUNCIONAL + ALINHAMENTO "MIRADO" NO CENTRO
st.markdown("""
    <style>
    /* SEU FIX DO TOPO (MANTIDO) */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1200px !important;
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
        font-size: 10px;
        text-transform: uppercase;
        text-align: center;
    }

    /* FORÇANDO A IMAGEM A SER UM BLOCO CENTRALIZADO */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    img {
        max-height: 60vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* BOTÕES DE NAVEGAÇÃO: CENTRALIZAÇÃO TOTAL */
    .stButton {
        display: flex;
        justify-content: center;
    }

    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #222 !important;
        height: 60px !important;
        width: 60px !important;
        font-size: 24px !important;
        transition: 0.2s;
        border-radius: 50% !important;
        margin: 0 10px !important; /* Espaço entre os dois botões */
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
        background-color: rgba(212, 175, 55, 0.05) !important;
    }

    .insight-box {
        background-color: #0E0E0E;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 25px;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Esconde elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título Centralizado
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
    # Usamos colunas largas para centralizar bem a imagem
    _, c_img, _ = st.columns([1, 4, 1])
    with c_img:
        st.image(path_img, use_container_width=True)

    # --- 2. NAVEGAÇÃO (SETAS ABAIXO) ---
    # Usamos 6 colunas para garantir que os botões do meio fiquem bem "juntos" no centro
    _, b1, b2, _ = st.columns([4, 0.6, 0.6, 4])
    
    with b1:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with b2:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    # --- 3. CAIXA DE ANÁLISE ---
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: texto = f.read()
        st.markdown(f'''
            <div class="insight-box">
                <span style="color:#444; font-size:10px; letter-spacing:2px; display:block; margin-bottom:10px;">SYSTEM_ANALYSIS //</span>
                {texto}
            </div>
        ''', unsafe_allow_html=True)

# GESTÃO (Final da página)
st.write("<br>"*3, unsafe_allow_html=True)
with st.expander("TERMINAL DE DADOS"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Novo Registro", type=["jpg", "png", "jpeg"])
        c = st.text_area("Comentário Estratégico:")
        if st.button("Gravar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                p = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(p, "wb") as file: file.write(f.getbuffer())
                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Corrigir Log:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(path_txt, "w") as file: file.write(novo)
                st.rerun()
            if st.button("🗑️ Apagar"):
                os.remove(path_img); os.remove(path_txt)
                st.session_state.idx = 0
                st.rerun()
