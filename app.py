import streamlit as st
import os
from datetime import datetime

# 1. Configuração de Página: Wide para amplitude total
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DE "FORÇA BRUTA": Xeque-mate no espaço e design moderno
st.markdown("""
    <style>
    /* ELIMINAÇÃO TOTAL DE ESPAÇOS NO TOPO */
    [data-testid="stHeader"], [data-testid="stDecoration"], header {
        display: none !important;
        height: 0 !important;
    }
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: -90px !important; /* Puxa o conteúdo para o limite físico superior */
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
    }

    /* ESTÉTICA STEALTH (PRETO E DOURADO) */
    html, body, [class*="css"] {
        background-color: #000000;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* TABULEIRO (PROPORÇÃO PROTEGIDA) */
    .stImage img {
        border-radius: 4px;
        border: 1px solid #222;
        max-height: 55vh !important; /* Mantém o tabuleiro visível sem scroll */
        width: auto !important;
        margin: 0 auto;
        display: block;
        box-shadow: 0 20px 50px rgba(0,0,0,1);
    }

    /* BOTÕES LATERAIS TÁTEIS */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid #111 !important;
        color: #444 !important;
        height: 55vh !important; /* Acompanha a altura da imagem */
        width: 100% !important;
        font-size: 40px !important;
        transition: 0.3s;
        border-radius: 8px;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: rgba(212, 175, 55, 0.05) !important;
    }

    /* CARD DE INSIGHT (ELEGÂNCIA TÉCNICA) */
    .analysis-card {
        background-color: #0A0A0A;
        padding: 20px 40px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        margin: 10px auto;
        max-width: 800px;
        text-align: center;
        font-size: 16px;
        color: #CCC;
        line-height: 1.6;
    }

    .system-tag {
        font-size: 9px;
        letter-spacing: 3px;
        color: #333;
        text-align: center;
        margin-bottom: 5px;
        text-transform: uppercase;
    }

    /* Esconde rodapé oficial */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título colado no topo
st.markdown('<div class="system-tag">Strategist Protocol // Opening Study</div>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("SISTEMA AGUARDANDO DADOS...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # --- GRID DE CONTROLE: [BOTÃO] [IMAGEM] [BOTÃO] ---
    c_ant, c_mid, c_prox = st.columns([1, 6, 1])
    
    with c_ant:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with c_mid:
        # Exibição do Tabuleiro Centralizado
        st.image(p_img, use_container_width=True)
        
        # Insight colado embaixo da imagem
        if os.path.exists(p_txt):
            with open(p_txt, "r") as f: texto = f.read()
            st.markdown(f'<div class="analysis-card">{texto}</div>', unsafe_allow_html=True)

    with c_prox:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#111; font-size:10px;'>ENTRY {st.session_state.idx + 1} / {len(imgs)}</p>", unsafe_allow_html=True)

# GESTÃO (Final da página)
with st.expander("TERMINAL DE DADOS"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload Dossier", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight Técnico:")
        if st.button("Executar"):
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
                with open(p_txt, "w") as f: f.write(novo)
                st.rerun()
            if st.button("🗑️ Eliminar"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
