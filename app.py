import streamlit as st
import os
from datetime import datetime

# 1. Configuração de Página (Layout centralizado protege a proporção do tabuleiro)
st.set_page_config(page_title="Audit", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS "GOD MODE" para eliminar o topo e estilizar a interface
st.markdown("""
    <style>
    /* Mata o cabeçalho e qualquer reserva de espaço superior */
    [data-testid="stHeader"], header { display: none !important; }
    
    /* Zera o container de visão do app */
    [data-testid="stAppViewContainer"] { padding-top: 0 !important; }
    
    /* Puxa o conteúdo até o limite físico da aba do navegador */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -85px !important; /* Ajuste agressivo para colar no topo */
        max-width: 600px !important; /* Mantém o tabuleiro em tamanho real/nítido */
    }

    /* Estética Dark Profissional */
    html, body, [class*="css"] {
        background-color: #000000;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    .system-label {
        text-align: center;
        font-size: 9px;
        letter-spacing: 4px;
        color: #333;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* Tabuleiro com brilho e borda fina */
    .stImage img {
        border-radius: 4px;
        border: 1px solid #111;
        box-shadow: 0 15px 40px rgba(0,0,0,1);
        max-height: 420px !important;
        object-fit: contain !important;
    }

    /* Caixa de Insight (Estilo Dossier Técnico) */
    .analysis-card {
        background-color: #050505;
        padding: 20px;
        border: 1px solid #111;
        border-top: 2px solid #FFFFFF;
        margin-top: 15px;
    }
    .analysis-text {
        font-size: 15px;
        color: #BBB;
        line-height: 1.6;
    }

    /* Botões de Navegação Slim e Lado a Lado */
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid #111 !important;
        color: #444 !important;
        height: 45px !important;
        font-size: 14px !important;
        transition: 0.2s;
        border-radius: 4px;
    }
    div.stButton > button:hover {
        border-color: #FFF !important;
        color: #FFF !important;
        background-color: #0A0A0A !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Header Técnico (Colado no topo)
st.markdown('<p class="system-label">Strategy Protocol // Audit Session</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("AUDITORIA VAZIA // AGUARDANDO INPUT.")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # Área do Tabuleiro
    st.image(p_img, use_container_width=True)

    # Navegação Slim abaixo do tabuleiro
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Anterior", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()
    with c2:
        if st.button("Próximo", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    # Insight do Registro Atual
    if os.path.exists(p_txt):
        with open(p_txt, "r") as f: texto = f.read()
        st.markdown(f'''
            <div class="analysis-card">
                <div class="analysis-text">{texto}</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown(f"<p style='text-align:center; color:#111; font-size:10px; margin-top:20px;'>RECORD {st.session_state.idx + 1} OF {len(imgs)}</p>", unsafe_allow_html=True)

# Gestão de Dados (Recolhido no final)
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("TERMINAL"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
        c = st.text_area("Comentário:")
        if st.button("Gravar"):
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
            if st.button("Apagar"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
