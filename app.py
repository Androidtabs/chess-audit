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

# 2. CSS: DESIGN PREMIUM + LÓGICA DE HOVER NA ANÁLISE
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* ZERA O VÁCUO DO TOPO */
    .stApp { margin-top: -85px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    [data-testid="stAppViewBlockContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 1100px !important; }

    /* ESTÉTICA DARK GERAL */
    html, body, [class*="css"] {
        background-color: #080808 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    .header-container {
        background: linear-gradient(90deg, rgba(10,10,10,0) 0%, rgba(20,20,20,1) 50%, rgba(10,10,10,0) 100%);
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: 15px 0;
        margin-bottom: 25px;
        width: 100%;
    }

    .header-text {
        font-size: 12px; color: #888; text-transform: uppercase; text-align: center; letter-spacing: 4px; font-weight: 300; margin: 0;
    }

    .record-counter { color: #D4AF37; font-size: 12px; font-weight: 600; text-align: center; margin-bottom: 5px; }

    .opening-tag {
        background-color: #111; color: #D4AF37; padding: 5px 18px; border-radius: 2px; border: 1px solid #222;
        font-size: 13px; display: inline-block; margin-bottom: 20px; font-weight: bold; letter-spacing: 1px;
    }

    /* --- CONTAINER DA IMAGEM + LÓGICA DE HOVER --- */
    .image-wrapper {
        position: relative;
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
        cursor: pointer;
    }

    .image-wrapper img {
        max-height: 58vh !important;
        border: 1px solid #222;
        box-shadow: 0 20px 60px rgba(0,0,0,1);
        transition: filter 0.3s ease;
    }

    /* Esconde a caixa de análise por padrão */
    .hover-analysis {
        position: absolute;
        bottom: 0;
        background: rgba(0, 0, 0, 0.85);
        color: #D4AF37;
        width: 100%;
        max-width: 58vh; /* Mesma largura aproximada do tabuleiro */
        padding: 20px;
        text-align: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        border-top: 2px solid #D4AF37;
        pointer-events: none;
        font-size: 14px;
        line-height: 1.5;
        backdrop-filter: blur(5px);
    }

    /* Quando passar o mouse no wrapper da imagem, mostra a análise */
    .image-wrapper:hover .hover-analysis {
        opacity: 1;
    }
    
    .image-wrapper:hover img {
        filter: brightness(0.4); /* Escurece um pouco o tabuleiro para o texto brilhar */
    }

    /* SETAS CIRCULARES */
    div.stButton > button {
        background-color: transparent !important;
        color: #444 !important;
        border: 1px solid #1A1A1A !important;
        height: 55px !important;
        width: 55px !important;
        border-radius: 50% !important;
        margin: 0 auto !important;
    }
    div.stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

st.markdown('<div class="header-container"><p class="header-text">Chess Strategy Lab // Sistema de Auditoria</p></div>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort()
aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    nome_exibicao = curr.split("_")[0].replace("-", " ")
    
    st.markdown(f'<p class="record-counter">ESTUDO {st.session_state.idx + 1} DE {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="opening-tag">📂 {nome_exibicao}</span></div>', unsafe_allow_html=True)

    # Lógica de Imagem e Análise (Texto só aparece no Hover)
    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    analise_texto = ""
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f:
            analise_texto = f.read()

    # Montando o HTML com o efeito de Hover
    st.markdown(f"""
        <div class="image-wrapper">
            <img src="data:image/jpeg;base64,{img_64}">
            <div class="hover-analysis">
                <b>ANÁLISE TÉCNICA:</b><br>{analise_texto}
            </div>
        </div>
    """, unsafe_allow_html=True)

    _, col2, col3, _ = st.columns([1, 0.08, 0.08, 1])
    with col2:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs); st.rerun()
    with col3:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs); st.rerun()

st.write("")
with st.expander("⚙️ GESTÃO DA BASE DE DADOS"):
    t1, t2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR ATUAL"])
    with t1:
        opcoes = ["-- Selecione --"] + aberturas_existentes + ["[ + NOVA ]"]
        escolha = st.selectbox("Selecione a Abertura:", opcoes)
        nome_f = st.text_input("Nome da Variante:") if escolha == "[ + NOVA ]" else (escolha if escolha != "-- Selecione --" else "")
        up_f = st.file_uploader("Captura da Posição:", type=["jpg", "png", "jpeg"])
        up_t = st.text_area("Nota Técnica / Análise da Engine:")
        if st.button("SALVAR NA BASE"): 
            if up_f and up_t and nome_f:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_limpo = nome_f.replace(" ", "-").strip()
                base = os.path.join(IMG_DIR, f"{nome_limpo}_{ts}")
                with open(f"{base}.jpg", "wb") as f: f.write(up_f.getbuffer())
                with open(f"{base}.txt", "w") as f: f.write(up_t)
                st.rerun()
    with t2:
        if imgs:
            edt_t = st.text_area("Editar Análise:", value=analise_texto, key="edit_area")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("ATUALIZAR"):
                    with open(os.path.join(IMG_DIR, curr.replace(".jpg", ".txt")), "w") as f: f.write(edt_t); st.rerun()
            with c2:
                if st.button("🗑️ ELIMINAR"):
                    os.remove(os.path.join(IMG_DIR, curr))
                    os.remove(os.path.join(IMG_DIR, curr.replace(".jpg", ".txt")))
                    st.session_state.idx = 0; st.rerun()
