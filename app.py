import streamlit as st
import os
from datetime import datetime

# Configuração de Página: Centralizado para proteger a proporção da imagem
st.set_page_config(page_title="Audit", layout="centered", initial_sidebar_state="collapsed")

# CSS: Design de Interface de Alta Performance
st.markdown("""
    <style>
    /* 1. Reset Total de Topo e Margens */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        max-width: 650px !important; /* Tamanho ideal para não distorcer */
        margin-top: -40px !important;
    }
    html, body, [class*="css"] {
        background-color: #080808;
        color: #B0B0B0;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Título "Minimal" */
    .system-label {
        text-align: center;
        font-size: 10px;
        letter-spacing: 5px;
        color: #333;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* 3. O Tabuleiro (Sem distorção) */
    .stImage img {
        border-radius: 8px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 30px 60px rgba(0,0,0,0.7);
        max-height: 450px !important; /* Protege contra scroll */
        object-fit: contain !important;
    }

    /* 4. Caixa de Insight (Design 'Dossier') */
    .analysis-container {
        background-color: #0F0F0F;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #1A1A1A;
        border-left: 3px solid #D4AF37;
        margin-top: 20px;
    }
    .analysis-header {
        font-size: 10px;
        color: #D4AF37;
        margin-bottom: 10px;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .analysis-body {
        font-size: 16px;
        color: #E0E0E0;
        line-height: 1.6;
    }

    /* 5. Navegação nas Laterais (Sem esticar) */
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid #1A1A1A !important;
        color: #444 !important;
        height: 450px !important; /* Acompanha a imagem */
        width: 100% !important;
        font-size: 20px !important;
        transition: 0.3s;
        border-radius: 8px;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: #111 !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

st.markdown('<p class="system-label">Strategist Protocol // Opening Audit</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("SISTEMA AGUARDANDO DADOS...")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # Layout: [Botão] [Imagem] [Botão]
    # Usamos uma proporção que não "estica" o centro
    c_prev, c_main, c_next = st.columns([1, 8, 1])
    
    with c_prev:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with c_main:
        # A imagem aqui NÃO vai esticar pois o layout é centralizado (650px)
        st.image(p_img, use_container_width=True)
        
        if os.path.exists(p_txt):
            with open(p_txt, "r") as f: texto = f.read()
            st.markdown(f'''
                <div class="analysis-container">
                    <div class="analysis-header">SYSTEM ANALYSIS // ID_{curr_img[:8]}</div>
                    <div class="analysis-body">{texto}</div>
                </div>
            ''', unsafe_allow_html=True)

    with c_next:
        st.write("<br>"*5, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

# Espaço e Gestão discreta
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("TERMINAL DE DADOS"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight:")
        if st.button("Gravar Registro"):
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
            if st.button("Eliminar"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
