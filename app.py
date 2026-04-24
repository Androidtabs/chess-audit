import streamlit as st
import os
from datetime import datetime

# Configuração de página
st.set_page_config(page_title="Audit", layout="wide", initial_sidebar_state="collapsed")

# CSS "HARDCORE" para eliminar espaços fantasmas no topo
st.markdown("""
    <style>
    /* 1. Alvo principal: O container de visualização e o header */
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
        margin-top: -50px !important; /* Puxa o conteúdo para cima de forma agressiva */
    }
    
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 1000px !important;
    }

    /* 2. Estilo do Título e Header */
    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        letter-spacing: 2px;
        color: #444;
        text-align: left;
        margin-top: 0px !important;
        margin-bottom: 5px;
        font-size: 11px;
        text-transform: uppercase;
    }

    /* 3. Imagem e Proporções */
    img {
        max-height: 60vh !important;
        width: 100%;
        object-fit: contain;
        border-radius: 4px;
        border: 1px solid #333;
    }

    /* 4. Caixa de Insight */
    .insight-box {
        background-color: #161B22;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        line-height: 1.5;
        color: #E0E0E0;
        margin-top: 5px;
    }

    /* 5. Navegação Lateral (Botões) */
    div.stButton > button {
        background-color: rgba(26, 26, 26, 0.3);
        color: #555;
        border: 1px solid #222;
        height: 450px;
        width: 100%;
        font-size: 30px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
    }

    /* Esconde elementos de sistema adicionais */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título colado no topo
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

    # Colunas principais
    c_ant, c_mid, c_prox = st.columns([0.4, 6, 0.4])
    
    with c_ant:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()

    with c_mid:
        st.image(p, use_container_width=True)
        if os.path.exists(t_p):
            with open(t_p, "r") as f: texto = f.read()
            st.markdown(f'<div class="insight-box"><b>DETALHES:</b> {texto}</div>', unsafe_allow_html=True)

    with c_prox:
        st.write("<br>"*2, unsafe_allow_html=True)
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

# Rodapé de Gestão
with st.expander("PROPRIEDADES"):
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
