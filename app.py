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

# 2. CSS: ARQUITETURA TÁTICA (O SEGREDO DO VISUAL)
st.markdown("""
    <style>
    /* 1. RESET TOTAL E FUNDO TÁTICO */
    [data-testid="stHeader"] {display: none !important;}
    .stApp {
        margin-top: -85px !important;
        background-color: #0d0d0d !important;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 30px 30px; /* Grade tática sutil */
    }
    .main .block-container { padding: 1.5rem !important; max-width: 1350px !important; }

    /* 2. HEADER EMOLDURADO */
    .custom-header {
        background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%);
        border: 1px solid #222;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .custom-header h1 {
        font-size: 15px;
        color: #D4AF37;
        text-transform: uppercase;
        letter-spacing: 7px;
        font-weight: 300;
        margin: 0;
    }

    /* 3. PAINEL DE CONTROLE (O "CARD" DA DIREITA) */
    .side-panel {
        background: #111111;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #1a1a1a;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        min-height: 500px;
    }

    .label-small {
        font-size: 10px;
        color: #444;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .gold-value {
        color: #D4AF37;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 25px;
        font-family: 'Courier New', monospace;
    }

    /* 4. TABULEIRO (LIMITADO E ELEGANTE) */
    .img-box {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .img-box img {
        max-width: 80% !important; /* Aqui controlamos o tamanho para não ficar gigante */
        max-height: 58vh !important;
        border: 2px solid #1a1a1a;
        border-radius: 4px;
        box-shadow: 0 40px 100px rgba(0,0,0,1);
    }

    /* 5. BOTÕES "PILL" (ESTILO PLAYER) */
    .stButton > button {
        width: 100% !important;
        background-color: #1a1a1a !important;
        color: #eee !important;
        border: 1px solid #333 !important;
        height: 45px !important;
        border-radius: 25px !important; /* Formato pill */
        font-size: 12px !important;
        transition: 0.3s;
    }
    .stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
        background-color: #1f1f1f !important;
    }

    /* 6. CARD DE INSIGHTS */
    .insight-card {
        background: rgba(0,0,0,0.3);
        border-left: 2px solid #D4AF37;
        padding: 20px;
        margin-top: 25px;
        color: #888;
        font-size: 14px;
        line-height: 1.7;
        border-radius: 0 8px 8px 0;
    }

    /* Toggle Customizado */
    .stToggle { margin-top: 10px; }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]
if 'idx' not in st.session_state: st.session_state.idx = 0

# --- ESTRUTURA VISUAL ---

# Header Superior
st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Estudo de Aberturas</h1></div>', unsafe_allow_html=True)

# Colunas Principais
col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    nome_abertura = curr.split("_")[0].replace("-", " ")
    data_id = curr.split("_")[1].split(".")[0] if "_" in curr else "20260424"

    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div class="img-box"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)

    # DIREITA: Painel de Controle
    with col_right:
        st.markdown('<div class="side-panel">', unsafe_allow_html=True)
        
        st.markdown('<p class="label-small">Protocolo de Auditoria</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="gold-value">{data_id}</div>', unsafe_allow_html=True)
        
        st.markdown('<p class="label-small" style="margin-bottom:15px;">Navegação</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("‹ ANTERIOR", key="prev_btn"):
                st.session_state.idx -= 1
                st.rerun()
        with c2:
            if st.button("PRÓXIMO ›", key="next_btn"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        st.markdown('<p class="label-small">Variante</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#eee; font-size:16px; font-weight:600; margin-bottom:25px;">{nome_abertura.upper()}</p>', unsafe_allow_html=True)

        st.markdown('<p class="label-small">Insights de Engine</p>', unsafe_allow_html=True)
        ativar = st.toggle("ATIVAR ANÁLISE TÉCNICA", value=False)
        
        if ativar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div class="insight-card">{f.read()}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="insight-card">Dados não localizados.</div>', unsafe_allow_html=True)

        st.markdown(f'<p style="color:#222; font-size:10px; margin-top:40px; text-align:right;">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 3. GESTÃO (DISCRETA NO RODAPÉ)
st.write("")
with st.expander("⚙️ MANAGE DATABASE"):
    t1, t2 = st.tabs(["NOVO", "EDITAR"])
    with t1:
        n_f = st.text_input("Nome Variante:")
        u_f = st.file_uploader("Screenshot:", type=["jpg", "png"])
        u_t = st.text_area("Insight:")
        if st.button("SALVAR"):
            if n_f and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.txt"), "w") as f: f.write(u_t)
                st.rerun()
