import streamlit as st
import os
from datetime import datetime

# 1. Configuração de Página
st.set_page_config(page_title="Audit", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS AGRESSIVO: Xeque-mate no espaço em branco
st.markdown("""
    <style>
    /* Esconde absolutamente tudo que o Streamlit coloca no topo */
    [data-testid="stHeader"], header, .stAppHeader { display: none !important; }
    
    /* Zera os containers internos e remove o vácuo */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -100px !important; /* Puxa o conteúdo para cima do limite */
        max-width: 600px !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
    }

    /* Estética de Luxo / Minimalista */
    html, body, [class*="css"] {
        background-color: #050505;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Título Estilo 'Selo de Sistema' */
    .system-seal {
        text-align: left;
        font-size: 9px;
        letter-spacing: 5px;
        color: #333;
        text-transform: uppercase;
        margin-bottom: 5px;
        border-bottom: 1px solid #111;
        padding-bottom: 5px;
    }

    /* Tabuleiro com Proporção Protegida */
    .stImage img {
        border-radius: 2px;
        border: 1px solid #1A1A1A;
        max-height: 400px !important;
        object-fit: contain !important;
        box-shadow: 0 20px 50px rgba(0,0,0,1);
    }

    /* Caixa de Insight Estilo Terminal de Auditoria */
    .audit-card {
        background-color: #0A0A0A;
        padding: 20px;
        border-left: 3px solid #D4AF37;
        margin-top: 10px;
    }
    .audit-label {
        font-size: 10px;
        color: #D4AF37;
        font-weight: bold;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .audit-text {
        font-size: 15px;
        color: #DDD;
        line-height: 1.6;
    }

    /* Navegação Minimalista */
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid #1A1A1A !important;
        color: #555 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# UI - Topo do Sistema
st.markdown('<div class="system-seal">STRATEGY_AUDIT_LOG // V_2.5</div>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("SISTEMA_OFFLINE // AGUARDANDO_DADOS")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # Display do Tabuleiro
    st.image(p_img, use_container_width=True)

    # Navegação Horizontal Slim
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("PREV", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()
    with c2:
        st.markdown(f"<p style='text-align:center; color:#222; font-size:10px; margin-top:10px;'>RECORD_{st.session_state.idx + 1}_{len(imgs)}</p>", unsafe_allow_html=True)
    with c3:
        if st.button("NEXT", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    # Insight do Registro
    if os.path.exists(p_txt):
        with open(p_txt, "r") as f: texto = f.read()
        st.markdown(f'''
            <div class="audit-card">
                <div class="audit-label">Análise Técnica //</div>
                <div class="audit-text">{texto}</div>
            </div>
        ''', unsafe_allow_html=True)

# Gestão de Dados (Final)
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("CONSOLE_DE_GERENCIAMENTO"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight:")
        if st.button("Salvar Registro"):
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
