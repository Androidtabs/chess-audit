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

# 2. CSS: DESIGN HUD E NAVEGAÇÃO INTEGRADA
st.markdown("""
    <style>
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
        border: 1px solid #222; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 30px;
    }
    .custom-header h1 {
        font-size: 13px; color: #D4AF37; text-transform: uppercase; letter-spacing: 7px; font-weight: 300; margin: 0;
    }

    /* PAINEL HUD (COLUNA 2) */
    [data-testid="column"]:nth-of-type(2) {
        background: #111111 !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border: 1px solid #1a1a1a !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important;
        min-height: 600px !important;
    }

    /* ESTILO DO INPUT DE NAVEGAÇÃO (X / Y) */
    .nav-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    .total-display {
        color: #333; font-size: 24px; font-weight: 900; margin-top: 5px;
    }
    
    /* Customizando o Number Input para sumir com label e bordas excessivas */
    .stNumberInput div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        width: 100px !important;
    }
    .stNumberInput input {
        color: #D4AF37 !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        padding: 0 !important;
        text-align: left !important;
    }

    /* VARIANTE DO ADVERSÁRIO */
    .variant-box {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 15px; border-radius: 6px; margin-bottom: 25px;
    }
    .variant-title {
        color: #D4AF37; font-size: 18px; font-weight: 800; text-transform: uppercase; margin: 0;
    }

    /* STATUS BADGE */
    .status-badge {
        padding: 6px 12px; border-radius: 4px; font-size: 10px; font-weight: bold;
        text-transform: uppercase; display: inline-block; margin-bottom: 15px;
    }
    .status-studied { background-color: rgba(0, 255, 100, 0.1); color: #00FF64; border: 1px solid #00FF64; }
    .status-awaiting { background-color: rgba(255, 50, 50, 0.1); color: #FF3232; border: 1px solid #FF3232; }

    /* BOTÕES PILL */
    .stButton > button {
        width: 100% !important; background-color: #1a1a1a !important; color: #eee !important;
        border: 1px solid #333 !important; border-radius: 20px !important; font-size: 11px !important; height: 40px !important;
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

st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Auditoria de Aberturas</h1></div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    # Lógica de Salto (Editável direto no X / Y)
    def handle_jump():
        st.session_state.idx = st.session_state.nav_input - 1

    curr = imgs[st.session_state.idx % len(imgs)]
    nome_raw = curr.split("_")[0].replace("-", " ")
    
    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div style="display:flex; justify-content:center;"><img src="data:image/jpeg;base64,{img_64}" style="max-width:85%; border-radius:4px; border:1px solid #222; box-shadow: 0 40px 100px rgba(0,0,0,1);"></div>', unsafe_allow_html=True)

    # DIREITA: Painel HUD
    with col_right:
        # NAVEGAÇÃO INTEGRADA (O "X / Y" editável)
        st.markdown('<p style="font-size:10px; color:#444; text-transform:uppercase; letter-spacing:2px; margin-bottom:0;">Posição</p>', unsafe_allow_html=True)
        
        c_input, c_total = st.columns([0.4, 1])
        with c_input:
            # Campo editável para o X
            st.number_input("Pos", min_value=1, max_value=len(imgs), value=st.session_state.idx + 1, 
                            key="nav_input", on_change=handle_jump, label_visibility="collapsed")
        with c_total:
            # Exibição do / Y
            st.markdown(f'<div class="total-display">/ {len(imgs)}</div>', unsafe_allow_html=True)

        # STATUS DE ESTUDO
        is_studied = st.session_state.studied_list.get(curr, False)
        if is_studied:
            st.markdown('<div class="status-badge status-studied">✓ Estudo Concluído</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-awaiting">⚠ Aguardando Estudo</div>', unsafe_allow_html=True)

        # VARIANTE
        st.markdown('<p style="font-size:10px; color:#444; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; font-weight:600;">Variante do Adversário</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="variant-box"><p class="variant-title">{nome_raw}</p></div>', unsafe_allow_html=True)

        # NAVEGAÇÃO SEQUENCIAL
        c_prev, c_next = st.columns(2)
        with c_prev:
            if st.button("‹ VOLTAR"):
                st.session_state.idx -= 1
                st.rerun()
        with c_next:
            if st.button("AVANÇAR ›"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        # CHECKPOINT E INSIGHTS
        st.markdown('<p style="font-size:10px; color:#444; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; font-weight:600;">Controle de Auditoria</p>', unsafe_allow_html=True)
        check = st.toggle("CONCLUIR ESTUDO", value=is_studied, key=f"chk_{curr}")
        if check != is_studied:
            st.session_state.studied_list[curr] = check
            st.rerun()

        revelar = st.toggle("REVELAR REFUTAÇÃO", value=False)
        if revelar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div style="background:rgba(0,0,0,0.4); padding:20px; border-left:2px solid #D4AF37; color:#bbb; font-size:14px; line-height:1.6;">{f.read()}</div>', unsafe_allow_html=True)

# 3. GESTÃO
st.write("")
with st.expander("⚙️ BASE DE DADOS"):
    # Código de gestão mantido...
    pass
