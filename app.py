import streamlit as st

import os

from datetime import datetime



# Configuração de página

st.set_page_config(page_title="Audit", layout="wide", initial_sidebar_state="collapsed")



# CSS AGRESSIVO: Alvos específicos para zerar o topo

st.markdown("""

    <style>

    /* 1. Remove o Header e o botão de menu */

    [data-testid="stHeader"] {display: none !important;}

    

    /* 2. Zera o padding de todos os containers principais */

    .main .block-container {

        padding-top: 0rem !important;

        padding-bottom: 0rem !important;

        margin-top: -30px !important;

        max-width: 1100px !important;

    }

    

    /* 3. Ataca a estrutura interna do Streamlit que gera o vácuo */

    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {

        padding-top: 0rem !important;

    }

    

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container {

        padding-top: 0rem !important;

    }



    /* Estilo do Título - Agora como uma linha de sistema no topo */

    .header-text {

        font-family: 'Inter', sans-serif;

        font-weight: 400;

        letter-spacing: 2px;

        color: #444;

        margin-top: 0px !important;

        margin-bottom: 10px;

        font-size: 10px;

        text-transform: uppercase;

    }



    /* Imagem e Display */

    img {

        max-height: 65vh !important;

        width: 100%;

        object-fit: contain;

        border-radius: 4px;

        border: 1px solid #333;

    }



    .insight-box {

        background-color: #161B22;

        padding: 20px;

        border-radius: 4px;

        border-bottom: 2px solid #D4AF37;

        font-size: 15px;

        color: #E0E0E0;

        margin-top: 10px;

    }



    /* Botões Laterais Táteis */

    div.stButton > button {

        background-color: rgba(26, 26, 26, 0.2);

        color: #666;

        border: 1px solid #222;

        height: 500px;

        width: 100%;

        font-size: 35px;

        transition: 0.2s;

    }

    

    div.stButton > button:hover {

        border-color: #D4AF37;

        color: #D4AF37;

    }



    /* Limpeza de UI */

    #MainMenu {visibility: hidden;}

    footer {visibility: hidden;}

    </style>

    """, unsafe_allow_html=True)



IMG_DIR = "jogadas"

if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

if 'idx' not in st.session_state: st.session_state.idx = 0



# Título colado no limite superior

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



    # Display Central

    c_ant, c_mid, c_prox = st.columns([0.5, 8, 0.5])

    

    with c_ant:

        st.write("<br>"*5, unsafe_allow_html=True)

        if st.button("‹", key="prev"):

            st.session_state.idx = (st.session_state.idx - 1) % total

            st.rerun()



    with c_mid:

        st.image(path_img, use_container_width=True)

        if os.path.exists(path_txt):

            with open(path_txt, "r") as f: texto = f.read()

            st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {texto}</div>', unsafe_allow_html=True)



    with c_prox:

        st.write("<br>"*5, unsafe_allow_html=True)

        if st.button("›", key="next"):

            st.session_state.idx = (st.session_state.idx + 1) % total

            st.rerun()



# Gestão Oculta

st.write("<br>"*2, unsafe_allow_html=True)

with st.expander("DADOS E PROPRIEDADES"):

    c1, c2 = st.columns(2)

    with c1:

        f = st.file_uploader("Novo Registro", type=["jpg", "png", "jpeg"])

        c = st.text_area("Insight da Engine:")

        if st.button("Salvar"):

            if f and c:

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                p = os.path.join(IMG_DIR, f"{ts}.jpg")

                with open(p, "wb") as file: file.write(f.getbuffer())

                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c)

                st.rerun()

    with c2:

        if imgs:

            novo = st.text_area("Editar Texto:", value=texto if 'texto' in locals() else "")

            if st.button("Atualizar"):

                with open(path_txt, "w") as file: file.write(novo)

                st.rerun()

            if st.button("🗑️ Deletar"):

                os.remove(path_img); os.remove(path_txt)

                st.session_state.idx = 0

                st.rerun()
