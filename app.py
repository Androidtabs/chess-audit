import streamlit as st
import os
from datetime import datetime

# 1. Configuração de Página: Layout Wide para as colunas funcionarem bem
st.set_page_config(page_title="Audit", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DE FORÇA BRUTA: Zera tudo e organiza os botões laterais
st.markdown("""
    <style>
    /* 1. MATA O TOPO COMPLETAMENTE */
    [data-testid="stHeader"], header, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 2. PUXA O CONTEÚDO PARA O LIMITE FÍSICO DA TELA */
    .main .block-container {
        padding-top: 0px !important;
        margin-top: -60px !important; /* Move tudo para cima do cabeçalho invisível */
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* 3. DESIGN MODERNO (DEEP BLACK & GOLD) */
    html, body, [class*="css"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
    }

    /* 4. TABULEIRO (PROPORÇÃO PROTEGIDA) */
    .stImage img {
        border: 1px solid #1A1A1A;
        border-radius: 4px;
        max-height: 450px !important;
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        display: block;
    }

    /* 5. BOTÕES LATERAIS (FIXADOS NA ALTURA DA IMAGEM) */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid #1A1A1A !important;
        color: #444 !important;
        height: 450px !important; /* Mesma altura do tabuleiro */
        width: 100% !important;
        font-size: 40px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: #0A0A0A !important;
    }

    /* 6. CAIXA DE TEXTO ELEGANTE */
    .analysis-box {
        background-color: #050505;
        padding: 20px;
        border-top: 1px solid #1A1A1A;
        border-bottom: 2px solid #D4AF37;
        margin-top: 10px;
        font-size: 16px;
        color: #CCC;
        line-height: 1.6;
        text-align: center;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("SISTEMA AGUARDANDO DADOS...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # --- LAYOUT DE ELITE: [BOTÃO] [TABULEIRO] [BOTÃO] ---
    # Usamos 3 colunas onde a do meio é a maior
    c_prev, c_main, c_next = st.columns([1, 6, 1])
    
    with c_prev:
        st.write("<br>"*2, unsafe_allow_html=True) # Alinhamento sutil
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with c_main:
        # Tabuleiro Central
        st.image(p_img, use_container_width=True)
        
        # Insight colado embaixo da imagem
        if os.path.exists(p_txt):
            with open(p_txt, "r") as f: texto = f.read()
            st.markdown(f'<div class="analysis-box">{texto}</div>', unsafe_allow_html=True)

    with c_next:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    st.markdown(f"<p style='text-align:center; color:#111; font-size:10px; margin-top:20px;'>RECORD {st.session_state.idx + 1} / {len(imgs)}</p>", unsafe_allow_html=True)

# GESTÃO (No fim da página, bem discreta)
with st.expander("TERMINAL DE COMANDO"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight Técnico:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                p = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(p, "wb") as file: file.write(f.getbuffer())
                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(p_txt, "w") as f: f.write(novo)
                st.rerun()
            if st.button("Eliminar Registro"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
