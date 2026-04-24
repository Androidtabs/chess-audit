import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (SUA VERSÃO PREFERIDA - INALTERADA)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# Função para converter imagem em base64 (Sua base de sucesso)
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 2. CSS: SEU FIX DE TOPO + RESTAURAÇÃO DO TERMINAL
st.markdown("""
    <style>
    /* --- SEU FIX DO TOPO (EXATAMENTE COMO VOCÊ QUERIA) --- */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1100px !important;
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
        margin-bottom: 10px; /* Reduzi um pouco para colar o contador */
        font-size: 11px;
        text-transform: uppercase;
        text-align: center;
    }

    /* --- CONTADOR DE REGISTRO (AMARELO) --- */
    .record-counter {
        font-family: 'Inter', sans-serif;
        color: #D4AF37; /* Dourado para destaque */
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    /* CENTRALIZAÇÃO ABSOLUTA DA IMAGEM */
    .centered-image-container {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-bottom: 20px;
    }
    .centered-image-container img {
        max-height: 60vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #222;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* ESTILO DAS SETAS (CÍRCULOS) */
    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #222 !important;
        height: 55px !important;
        width: 55px !important;
        font-size: 22px !important;
        transition: 0.2s;
        border-radius: 50% !important;
        display: block;
        margin: 0 auto !important;
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
    }

    /* --- FIX DO TERMINAL DE GESTÃO (SEM VERMELHO, SÓ AMARELO) --- */
    /* Remove a borda vermelha e mantém apenas a amarela dourada */
    .stExpander div.stButton > button {
        border-radius: 4px !important;
        width: 100% !important;
        height: auto !important;
        padding: 10px !important;
        font-size: 14px !important;
        background-color: #1A1A1A !important;
        border: 1px solid #333 !important; /* Borda sutil */
        color: #EEE !important;
    }

    /* Remove qualquer contaminação vermelha nas colunas de baixo */
    [data-testid="column"] div.stButton button {
        border-color: #333 !important;
        color: #EEE !important;
    }

    .insight-box {
        background-color: #111;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 20px;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título
st.markdown('<p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort() # Ordenação padrão para a numeração fazer sentido

texto_atual = ""
if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    current_number = st.session_state.idx + 1 # Contador Humano
    
    curr = imgs[st.session_state.idx]
    path_img = os.path.join(IMG_DIR, curr)
    path_txt = path_img.replace(".jpg", ".txt")

    # --- CONTADOR DE REGISTRO (AMARELO) ---
    st.markdown(f'<p class="record-counter">REGISTRO {current_number} / {total}</p>', unsafe_allow_html=True)

    # 1. TABULEIRO
    img_base64 = get_image_base64(path_img)
    st.markdown(
        f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>',
        unsafe_allow_html=True
    )

    # 2. CONTROLES (SETAS) ABAIXO
    _, b1, b2, _ = st.columns([1, 0.15, 0.15, 1])
    with b1:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()
    with b2:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    # 3. ANÁLISE
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: texto_atual = f.read()
        st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto_atual}</div>', unsafe_allow_html=True)

# GESTÃO OCULTA (TERMINAL CORRIGIDO)
st.write("<br>"*3, unsafe_allow_html=True)
with st.expander("⚙️ GESTÃO DE DADOS (ADICIONAR / REMOVER / EDITAR)"):
    tab1, tab2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR OU REMOVER ATUAL"])
    
    with tab1:
        novo_f = st.file_uploader("Upload da Imagem", type=["jpg", "png", "jpeg"], key="up_novo")
        novo_t = st.text_area("Insight da Engine:", height=100, key="txt_novo")
        if st.button("SALVAR NOVO REGISTRO", key="btn_salvar"): 
            if novo_f and novo_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                base = os.path.join(IMG_DIR, f"{ts}")
                with open(f"{base}.jpg", "wb") as file: file.write(novo_f.getbuffer())
                with open(f"{base}.txt", "w") as file: file.write(novo_t)
                st.rerun()
    
    with tab2:
        if imgs:
            st.warning(f"Você está editando o Registro {st.session_state.idx + 1}")
            novo_texto = st.text_area("Alterar Texto:", value=texto_atual, key="edit_texto")
            
            col_edit, col_del = st.columns(2)
            with col_edit:
                if st.button("ATUALIZAR DADOS", key="btn_update"):
                    with open(path_txt, "w") as file: file.write(novo_texto)
                    st.rerun()
            with col_del:
                if st.button("🗑️ DELETAR ESTE REGISTRO", key="btn_delete"):
                    os.remove(path_img)
                    if os.path.exists(path_txt): os.remove(path_txt)
                    st.session_state.idx = 0
                    st.rerun()
