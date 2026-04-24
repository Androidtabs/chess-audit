import streamlit as st
import os
from datetime import datetime

# 1. SUA CONFIGURAÇÃO BASE QUE FUNCIONA
st.set_page_config(page_title="Audit", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: SEU CÓDIGO DO TOPO + BOTÕES LATERAIS QUE VOCÊ GOSTOU
st.markdown("""
    <style>
    /* --- SEU FIX DO TOPO (INALTERADO) --- */
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

    /* --- ESTÉTICA E CENTRALIZAÇÃO DA IMAGEM --- */
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

    /* FORÇANDO A CENTRALIZAÇÃO DA IMAGEM */
    img {
        max-height: 65vh !important;
        width: auto !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
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
        text-align: center;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    /* BOTÕES LATERAIS QUE VOC
