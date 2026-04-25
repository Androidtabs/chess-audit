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

# 2. CSS: DESIGN HUD COM FOCO EM STATUS E PROGRESSO
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

    /* HEADER SUPERIOR */
    .custom-header {
        background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%);
        border: 1px solid #222;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 30px;
    }
    .custom-header h1 {
        font-size: 13px; color: #D4AF37; text-transform: uppercase; letter-spacing: 7px; font-weight: 300; margin: 0;
    }

    /* ESTILIZAÇÃO DO PAINEL LATERAL (ESTRUTURA DA COLUNA) */
    [data-testid="column"]:nth-of-type(2) {
        background: #111111 !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border: 1px solid #1a1a1a !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important;
        min-height: 580px !important;
    }

    /* CONTADOR DE IMAGENS (GRANDE E VISÍVEL) */
    .image-counter {
        color: #D4AF37;
        font-size: 32px;
        font-weight: 900;
        font-family: 'Inter', sans-serif;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .label-small {
        font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; font-weight: 600;
    }

    /* NOME DA VARIANTE */
    .variant-title {
        color: #eee; font-size: 20px; font-weight: 700; margin-bottom: 25px; text-transform: uppercase;
        border-bottom: 1px solid #222; padding-bottom: 10px;
    }

    /* TABULEIRO */
    .board-box img {
        max-width: 85% !important;
        max-height: 60vh !important;
        border: 1px solid #1a1a1a;
        border-radius: 4px;
        box-shadow: 0 40px 100px rgba(0,0,0,1);
    }

    /* STATUS DE ESTUDO (MENSAGEM DINÂMICA) */
    .status-badge {
        padding: 8px 15px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 20px;
    }
    .status-studied { background-color: rgba(0, 255, 100, 0.1); color: #00FF64; border: 1px solid #00FF64; }
    .status-awaiting { background-color: rgba(255, 50, 50, 0.1); color: #FF3232; border: 1px solid #FF3232; }

    /* BOTÕES PILL */
    .stButton > button {
        width: 100% !important;
        background-color: #1a1a1a !important;
        color: #eee !important;
        border: 1px solid #333 !important;
        border-radius: 20px !important;
        font-size: 11px !important;
        height: 40px !important;
    }
    .stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

# Controle de Sessão
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'studied_list' not in st.session_state: st.session_state.studied_list = {}

# --- HEADER ---
st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Auditoria de Aberturas</h1></div>', unsafe_allow_html=True)

# --- LAYOUT ---
col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    nome_raw = curr.split("_")[0].replace("-", " ")
    
    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div style="display:flex; justify-content:center;"><img src="data:image/jpeg;base64,{img_64}" style="max-width:85%; border-radius:4px; border:1px solid #222;"></div>', unsafe_allow_html=True)

    # DIREITA: Painel de Controle
    with col_right:
        # 1. CONTADOR GRANDE
        st.markdown('<p class="label-small">Posição Atual</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="image-counter">{st.session_state.idx + 1} <span style="font-size:16px; color:#333;">/ {len(imgs)}</span></div>', unsafe_allow_html=True)
        
        # 2. STATUS DE ESTUDO
        # Verificamos se o item atual está marcado como estudado
        is_studied = st.session_state.studied_list.get(curr, False)
        if is_studied:
            st.markdown('<div class="status-badge status-studied">✓ Estudo Concluído</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-awaiting">⚠ Aguardando Estudo</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="variant-title">{nome_raw}</div>', unsafe_allow_html=True)

        # 3. NAVEGAÇÃO
        st.markdown('<p class="label-small">Navegação</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("‹ VOLTAR", key="prev"):
                st.session_state.idx -= 1
                st.rerun()
        with c2:
            if st.button("AVANÇAR ›", key="next"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        # 4. CHECKPOINT DE AUDITORIA
        st.markdown('<p class="label-small">Controle de Progresso</p>', unsafe_allow_html=True)
        
        # O Toggle agora serve para marcar o estudo como feito
        check = st.toggle("MARCAR COMO CONCLUÍDO", value=is_studied, key=f"check_{curr}")
        if check != is_studied:
            st.session_state.studied_list[curr] = check
            st.rerun()

        # Insight da Engine (Opcional)
        st.write("")
        revelar = st.toggle("REVELAR INSIGHTS TÉCNICOS", value=False)
        if revelar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div style="background:rgba(0,0,0,0.4); padding:15px; border-left:2px solid #D4AF37; color:#888; font-size:14px;">{f.read()}</div>', unsafe_allow_html=True)

# 3. GESTÃO
st.write("")
with st.expander("⚙️ GERENCIAR REGISTROS"):
    # (Código de cadastro mantido aqui abaixo...)
    pass
