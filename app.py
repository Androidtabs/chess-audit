import streamlit as st
import os
from datetime import datetime

# 1. SUA CONFIGURAÇÃO BASE (TOPO ZERO)
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: SUA BASE FUNCIONAL + AJUSTE DE ALINHAMENTO DAS COLUNAS
st.markdown("""
    <style>
    /* SEU FIX DO TOPO (INALTERADO) */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
        max-width: 1200px !important;
    }
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
        padding-top: 0rem !important;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container {
        padding-top: 0rem !important;
    }

    /* ESTÉTICA DARK E CENTRALIZAÇÃO */
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

    /* FORÇANDO A IMAGEM A SER UM BLOCO CENTRALIZADO */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    img {
        max-height: 62vh !important;
        width: auto !important;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }

    .insight-box {
        background-color: #0E0E0E;
        padding: 20px;
        border-radius: 4px;
        border-bottom: 2px solid #D4AF37;
        font-size: 15px;
        color: #E0E0E0;
        margin-top: 15px;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* BOTÕES LATERAIS CIRCULARES */
    div.stButton > button {
        background-color: transparent !important;
        color: #555 !important;
        border: 1px solid #1A1A1A !important;
        height: 70px !important;
        width: 70px !important;
        font-size: 25px !important;
        transition: 0.2s;
        border-radius: 50% !important;
        margin-top: 200px;
        display: block;
    }
    
    /* AJUSTE DE PROXIMIDADE: Empurra o botão da esquerda para a direita e o da direita para a esquerda */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlock"] {
        align-items: flex-end !important;
    }
    [data-testid="column"]:nth-of-type(3) [data-testid="stVerticalBlock"] {
        align-items: flex-start !important;
    }

    div.stButton > button:hover {
