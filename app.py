import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="Strategy Lab", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: ESTILIZAÇÃO DIRETA DA COLUNA (SISTEMA HUD)
st.markdown("""
    <style>
    /* FUNDO TÁTICO */
    [data-testid="stHeader"] {display: none !important;}
    .stApp {
        margin-top: -85px !important;
        background-color: #0d0d0d !important;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 30px 30px;
    }
    .main .block-container { padding: 1.5rem !important; max-width: 1350px !important; }

    /* HEADER */
    .custom-header {
        background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%);
        border: 1px solid #222;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        margin-bottom: 30px;
    }
    .custom-header h1 {
        font-size: 15px; color: #D4AF37; text-transform: uppercase; letter-spacing: 7px; font-weight: 300; margin: 0;
    }

    /* O SEGREDO: ESTILIZAR A COLUNA DA DIREITA DIRETAMENTE */
    [data-testid="column"]:nth-of-type(2) {
        background: #111111 !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border: 1px solid #1a1a1a !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important;
        min-height: 550px !important;
    }

    /* LABELS E TEXTOS */
    .label-small {
        font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; font-weight: 600;
    }
    .gold-id {
        color: #D4AF37; font-size: 24px; font-weight: 800; margin-bottom: 20px; font-family: monospace;
    }
    .opening-name {
        color: #eee; font-size: 18px; font-weight: 700; margin-bottom: 25px; text-transform: uppercase;
    }

    /* TABULEIRO EQUILIBRADO */
    .board-box { display: flex; justify-content: center; align-items: center; }
    .board-box img {
        max-width: 90% !important;
        max-height: 60vh !important;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
        box-shadow: 0 40px 100px rgba(0,0,0,1);
    }

    /* BOTÕES PILL */
    .stButton > button {
        width: 100% !important;
        background-color: #1a1a1a !important;
        color: #eee !important;
        border: 1px solid #333 !important;
        border-radius: 20px !important;
        font-size: 11px !important;
        height: 40px !important;
        transition: 0.3s;
    }
    .stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    /* CARD DE ANÁLISE DENTRO DO PAINEL */
    .insight-card {
        background: rgba(0,0,0,0.4);
        border-left: 3px solid #D4AF37;
        padding: 15px;
        margin-top: 20px;
        color: #999;
        font-size: 14px;
        line-height: 1.6;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]
if 'idx' not in st.session_state: st.session_state.idx = 0

# --- HEADER ---
st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Estudo de Aberturas</h1></div>', unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL ---
col_left, col_right = st.columns([1.5, 1], gap="medium")

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    # Extração de dados segura
    nome_raw = curr.split("_")[0].replace("-", " ")
    data_id = curr.split("_")[1].split(".")[0] if "_" in curr else "20260424"

    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div class="board-box"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)

    # DIREITA: Painel de Controle (Tudo aqui dentro agora aparece no box escuro)
    with col_right:
        st.markdown('<p class="label-small">Protocolo de Auditoria</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="gold-id">{data_id}</div>', unsafe_allow_html=True)
        
        st.markdown('<p class="label-small">Navegação</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("‹ ANTERIOR", key="p_btn"):
                st.session_state.idx -= 1
                st.rerun()
        with c2:
            if st.button("PRÓXIMO ›", key="n_btn"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        st.markdown('<p class="label-small">Variante Ativa</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="opening-name">{nome_raw}</div>', unsafe_allow_html=True)

        st.markdown('<p class="label-small">Análise de Engine</p>', unsafe_allow_html=True)
        ativar = st.toggle("REVELAR INSIGHTS", value=False)
        
        if ativar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div class="insight-card">{f.read()}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="insight-card">Nenhum dado cadastrado.</div>', unsafe_allow_html=True)

        st.markdown(f'<p style="color:#222; font-size:10px; margin-top:50px; text-align:right;">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)

# --- GESTÃO ---
st.write("")
with st.expander("⚙️ MANAGE DATABASE"):
    t1, t2 = st.tabs(["NOVO", "EDITAR"])
    with t1:
        n_f = st.text_input("Nome Variante:")
        u_f = st.file_uploader("Screenshot:", type=["jpg", "png"])
        u_t = st.text_area("Insight:")
        if st.button("SALVAR REGISTRO"):
            if n_f and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.txt"), "w") as f: f.write(u_t)
                st.rerun()
