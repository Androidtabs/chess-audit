import streamlit as st
import os
from datetime import datetime

# 1. CONFIGURAÇÃO BASE (TOPO ZERO)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: SEU FIX DE TOPO + AJUSTE DE CENTRALIZAÇÃO
st.markdown("""
    <style>
    /* --- SEU FIX DO TOPO (MANTIDO INTEGRALMENTE) --- */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1100px !important;
    }
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container {
        padding-top: 0rem !important;
    }

    /* ESTÉTICA DARK */
    html, body, [class*="css"] {
        background-color: #080808 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    .header-text {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        letter-spacing: 2px;
        color: #444;
        margin-top: 0px !important;
        margin-bottom: 10px;
        font-size: 10px;
        text-transform: uppercase;
        text-align: center;
    }

    /* CENTRALIZAÇÃO DO CONTEÚDO */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    img {
        max-height: 60vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #333;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    /* BOTÕES CIRCULARES CENTRALIZADOS ABAIXO */
    div.stButton > button {
        background-color: transparent !important;
        color: #666 !important;
        border: 1px solid #222 !important;
        height: 60px !important;
        width: 60px !important;
        font-size: 25px !important;
        transition: 0.2s;
        border-radius: 50% !important;
        display: block;
        margin: 0 auto !important; /* Centraliza na coluninha */
    }
    
    div.stButton > button:hover {
        border-color: #D4AF37;
        color: #D4AF37;
    }

    .insight-box {
        background-color: #161B22;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 15px;
        text-align: center;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título
st.markdown('<p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(
