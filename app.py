import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (TOPO ZERO - MANTIDO)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: TOPO PERFEITO + CONTADOR + ESTILO DE BOTÕES
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1100px !important;
    }

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
        margin-bottom: 5px;
        font-size: 11px;
        text-transform: uppercase;
        text-align: center;
    }

    .record-counter {
        font-family: 'Inter', sans-serif;
        color: #D4AF37;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    .centered-image-container {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin-bottom: 20px;
    }
    .centered-image-container img {
        max-height: 60vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #222;
    }

    /* SETAS DE NAVEGAÇÃO */
    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #222 !important;
        height: 55px !important;
        width: 55px !important;
        font-size: 22px !important;
        border-radius: 50% !important;
        display: block;
        margin: 0 auto !important;
    }

    /* BOTÕES DE GESTÃO (RETANGULARES) */
    .stExpander button {
        border-radius: 4px !important;
        width: 100% !important;
        height: 45px !important;
        background-color: #1A1A1A !important;
        font-weight: bold !important;
    }

    /* DESTAQUE PARA O BOTÃO REMOVER */
    [data-testid="column"]:nth-of-type(2) .stButton button {
        border-color: #ff4b4b !important;
        color: #ff4b4b !important;
    }

    .insight-box {
        background-color: #111;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        text-align: center;
        max-width: 600px;
        margin: 20px auto;
    }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

st.markdown('<p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort()

texto_atual = ""
if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    current_number = st.session_state.idx + 1
    
    curr = imgs[st.session_state.idx]
    path_img = os.path.join(IMG_DIR, curr)
    path_txt = path_img.replace(".jpg", ".txt")

    st.markdown(f'<p class="record-counter">REGISTRO {current_number} / {total}</p>', unsafe_allow_html=True)

    # 1. VISUALIZAÇÃO
    img_64 = get_image_base64(path_img)
    st.markdown(f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)

    # 2. NAVEGAÇÃO
    _, b1, b2, _ = st.columns([1, 0.15, 0.15, 1])
    with b1:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()
    with b2:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    # 3. TEXTO
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: texto_atual = f.read()
        st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto_atual}</div>', unsafe_allow_html=True)

# CENTRAL DE GESTÃO
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("⚙️ GESTÃO DE DADOS (ADICIONAR / REMOVER / EDITAR)"):
    tab1, tab2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR OU REMOVER"])
    
    with tab1:
        novo_f = st.file_uploader("Selecione a imagem:", type=["jpg", "png", "jpeg"], key="up_novo")
        novo_t = st.text_area("Análise da engine:", height=100, key="txt_novo")
        if st.button("SALVAR NOVO REGISTRO"):
            if novo_f and novo_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                base = os.path.join(IMG_DIR, f"{ts}")
                with open(f"{base}.jpg", "wb") as f: f.write(novo_f.getbuffer())
                with open(f"{base}.txt", "w") as f: f.write(novo_t)
                st.rerun()

    with tab2:
        if imgs:
            st.warning(f"Atenção: Você está editando o Registro {st.session_state.idx + 1}")
            edt_t = st.text_area("Alterar análise:", value=texto_atual, key="txt_edit")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("ATUALIZAR TEXTO"):
                    with open(path_txt, "w") as f: f.write(edt_t)
                    st.success("Texto atualizado!")
                    st.rerun()
            with col_b:
                if st.button("REMOVER ESTE REGISTRO"):
                    os.remove(path_img)
                    if os.path.exists(path_txt): os.remove(path_txt)
                    st.session_state.idx = 0 # Volta para o início após remover
                    st.rerun()
        else:
            st.write("Nenhum dado disponível para editar ou remover.")
