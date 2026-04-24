import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (SUA VERSÃO PREFERIDA - INALTERADA)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: TOPO PERFEITO + ESTILIZAÇÃO DAS ABAS E BOTÕES
st.markdown("""
    <style>
    /* --- SEU FIX DO TOPO (INALTEÁVEL) --- */
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
        margin-bottom: 20px;
        font-size: 11px;
        text-transform: uppercase;
        text-align: center;
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

    /* FIX DOS BOTÕES DENTRO DO EXPANDER (RETANGULARES) */
    .stExpander div.stButton > button {
        border-radius: 4px !important;
        width: 100% !important;
        height: auto !important;
        padding: 10px !important;
        font-size: 14px !important;
        background-color: #1A1A1A !important;
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
imgs.sort(reverse=True)

texto_atual = ""
if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    path_img = os.path.join(IMG_DIR, curr)
    path_txt = path_img.replace(".jpg", ".txt")

    # 1. TABULEIRO (CENTRALIZADO)
    img_64 = get_image_base64(path_img)
    st.markdown(f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)

    # 2. CONTROLES (SETAS)
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

# GESTÃO (TABS PARA NÃO CONFUNDIR)
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("CENTRAL DE COMANDO"):
    aba_add, aba_edit = st.tabs(["➕ ADICIONAR NOVO", "📝 EDITAR ATUAL"])
    
    with aba_add:
        st.markdown("### Criar Nova Entrada")
        f_novo = st.file_uploader("Upload da Imagem", type=["jpg", "png", "jpeg"], key="upload_novo")
        c_novo = st.text_area("Insight da Engine:", key="texto_novo")
        if st.button("SALVAR NOVO REGISTRO", key="btn_salvar"):
            if f_novo and c_novo:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                p = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(p, "wb") as file: file.write(f_novo.getbuffer())
                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c_novo)
                st.success("Salvo com sucesso!")
                st.rerun()
    
    with aba_edit:
        if imgs:
            st.markdown(f"### Editando: `{curr}`")
            novo_texto = st.text_area("Alterar Análise:", value=texto_atual, key="edit_texto")
            
            c_edit1, c_edit2 = st.columns(2)
            with c_edit1:
                if st.button("ATUALIZAR MUDANÇAS", key="btn_update"):
                    with open(path_txt, "w") as file: file.write(novo_texto)
                    st.rerun()
            with c_edit2:
                if st.button("🗑️ DELETAR ESTE REGISTRO", key="btn_delete"):
                    os.remove(path_img)
                    os.remove(path_txt)
                    st.session_state.idx = 0
                    st.rerun()
        else:
            st.warning("Nenhum dado para editar.")
