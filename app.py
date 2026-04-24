import streamlit as st
import os
from datetime import datetime

# Configuração de página para ocupar o máximo de espaço
st.set_page_config(page_title="Audit", layout="wide", initial_sidebar_state="collapsed")

# CSS AGRESSIVO para ganhar espaço no topo e largura
st.markdown("""
    <style>
    /* 1. Elimina o Header e o espaço em branco superior */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 950px !important; /* Aumenta a amplitude lateral */
    }

    /* 2. Título ultra compacto */
    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        letter-spacing: 2px;
        color: #444;
        text-align: left;
        margin-bottom: 5px;
        font-size: 11px;
        text-transform: uppercase;
    }

    /* 3. Imagem Ampla */
    img {
        max-height: 55vh !important; /* Aumenta a altura da imagem */
        width: 100%;
        object-fit: contain;
        border-radius: 8px;
        border: 1px solid #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* 4. Caixa de Insight Ampla e Elegante */
    .insight-box {
        background-color: #161B22;
        padding: 25px;
        border-radius: 8px;
        border-bottom: 3px solid #D4AF37;
        font-size: 16px;
        line-height: 1.6;
        color: #E0E0E0;
        margin-top: 10px;
    }

    /* 5. Botões de Navegação nas Laterais */
    div.stButton > button {
        background-color: rgba(26, 26, 26, 0.5);
        color: #fff;
        border: 1px solid #333;
        height: 400px; /* Botão alto acompanhando a imagem */
        width: 100%;
        font-size: 40px;
        transition: 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
        background-color: #161B22;
    }

    /* Remove Scrollbar lateral desnecessária */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #333; }
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título discreto e posicionado
st.markdown('<p class="header-text">Chess Strategy Lab / Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Aguardando Lançamento...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    p = os.path.join(IMG_DIR, curr)
    t_p = p.replace(".jpg", ".txt")

    # GRID AMPLO
    col_ant, col_mid, col_prox = st.columns([0.4, 6, 0.4])
    
    with col_ant:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with col_mid:
        st.image(p, use_container_width=True)
        if os.path.exists(t_p):
            with open(t_p, "r") as f: texto = f.read()
            st.markdown(f'<div class="insight-box"><b>DETALHES TÉCNICOS:</b><br>{texto}</div>', unsafe_allow_html=True)

    with col_prox:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    st.markdown(f"<p style='text-align:right; color:#333; font-size:10px; margin-right:50px;'>DATA_POINT_{st.session_state.idx + 1}_OF_{len(imgs)}</p>", unsafe_allow_html=True)

# GESTÃO RECOLHIDA NO RODAPÉ
with st.expander("PROPRIEDADES E DADOS"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as file: file.write(f.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(t_p, "w") as file: file.write(novo)
                st.rerun()
            if st.button("Deletar"):
                os.remove(p); os.remove(t_p)
                st.session_state.idx = 0
                st.rerun()
