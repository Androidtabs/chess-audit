import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE
st.set_page_config(page_title="Strategy Lab", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: DESIGN TÁTICO COMPACTO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { 
        margin-top: -95px !important; 
        background-color: #0d0d0d !important; 
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px); 
        background-size: 30px 30px; 
    }
    .main .block-container { padding: 1rem !important; max-width: 1300px !important; }
    
    /* HEADER COMPACTO */
    .custom-header { 
        background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%); 
        border: 1px solid #222; border-radius: 8px; padding: 8px; text-align: center; margin-bottom: 15px; 
    }
    .custom-header h1 { font-size: 11px; color: #D4AF37; text-transform: uppercase; letter-spacing: 5px; font-weight: 300; margin: 0; }

    /* PAINEL HUD COMPACTO */
    [data-testid="column"]:nth-of-type(2) { 
        background: #111111 !important; 
        padding: 18px !important; 
        border-radius: 12px !important; 
        border: 1px solid #1a1a1a !important; 
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important; 
    }
    
    /* AJUSTE DO TABULEIRO PARA CABER NA TELA */
    .board-container img {
        max-width: 75% !important;
        max-height: 50vh !important; /* Limita a 50% da altura da tela */
        border-radius: 4px;
        border: 1px solid #222;
        box-shadow: 0 20px 60px rgba(0,0,0,1);
    }

    .label-tech { font-size: 9px; color: #444; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; font-weight: 600; }
    
    .data-display-box { 
        background: rgba(255, 255, 255, 0.02); 
        padding: 10px; border-radius: 6px; margin-bottom: 12px; border: 1px solid #1a1a1a; 
    }
    .my-line-text { color: #D4AF37; font-size: 16px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .opp-line-text { color: #eee; font-size: 13px; font-weight: 600; text-transform: uppercase; margin: 0; }
    
    .total-display { color: #333; font-size: 20px; font-weight: 900; margin-top: 5px; }
    .stNumberInput input { color: #D4AF37 !important; font-size: 28px !important; font-weight: 900 !important; }

    .status-badge { padding: 4px 10px; border-radius: 4px; font-size: 9px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; }
    .status-studied { background-color: rgba(0, 255, 100, 0.05); color: #00FF64; border: 1px solid #00FF64; }
    .status-awaiting { background-color: rgba(255, 50, 50, 0.05); color: #FF3232; border: 1px solid #FF3232; }

    .stButton > button { height: 35px !important; font-size: 10px !important; border-radius: 15px !important; }
    
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. LOGICA DE ARQUIVOS
IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'studied_list' not in st.session_state: st.session_state.studied_list = {}

st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Estudo de Aberturas</h1></div>', unsafe_allow_html=True)
col_left, col_right = st.columns([1.3, 1], gap="medium")

if imgs:
    st.session_state.idx = max(0, min(st.session_state.idx, len(imgs) - 1))
    curr = imgs[st.session_state.idx]
    path_jpg = os.path.join(IMG_DIR, curr)
    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    path_op = os.path.join(IMG_DIR, curr.replace(".jpg", "_op.txt"))

    # ESQUERDA: Tabuleiro Redimensionado
    with col_left:
        img_64 = get_image_base64(path_jpg)
        st.markdown(f'''
            <div class="board-container" style="display:flex; justify-content:center; align-items:center; height:60vh;">
                <img src="data:image/jpeg;base64,{img_64}">
            </div>
        ''', unsafe_allow_html=True)

    # DIREITA: Painel
    with col_right:
        st.markdown('<p class="label-tech">Navegação</p>', unsafe_allow_html=True)
        c_in, c_tot = st.columns([0.4, 1])
        with c_in:
            v_input = st.number_input("Pos", min_value=1, max_value=len(imgs), value=st.session_state.idx + 1, key=f"nav_{st.session_state.idx}", label_visibility="collapsed")
            if v_input != st.session_state.idx + 1:
                st.session_state.idx = v_input - 1
                st.rerun()
        with c_tot: st.markdown(f'<div class="total-display">/ {len(imgs)}</div>', unsafe_allow_html=True)

        is_studied = st.session_state.studied_list.get(curr, False)
        st.markdown(f'<div class="status-badge {"status-studied" if is_studied else "status-awaiting"}">{"✓ Estudo Concluído" if is_studied else "⚠ Aguardando Estudo"}</div>', unsafe_allow_html=True)

        my_opening = "NÃO INFORMADA"
        if os.path.exists(path_op):
            with open(path_op, "r") as f: my_opening = f.read()

        st.markdown('<p class="label-tech">Minha Abertura</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-display-box" style="border-left: 3px solid #D4AF37;"><p class="my-line-text">{my_opening}</p></div>', unsafe_allow_html=True)

        st.markdown('<p class="label-tech">Variante do Adversário</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-display-box"><p class="opp-line-text">{curr.split("_")[0].replace("-", " ")}</p></div>', unsafe_allow_html=True)

        c_p, c_n = st.columns(2)
        with c_p: 
            if st.button("‹ VOLTAR", disabled=(st.session_state.idx <= 0)):
                st.session_state.idx -= 1
                st.rerun()
        with c_n: 
            if st.button("AVANÇAR ›", disabled=(st.session_state.idx >= len(imgs) - 1)):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        check = st.toggle("CONCLUIR REVISÃO", value=is_studied, key=f"chk_{curr}")
        if check != is_studied:
            st.session_state.studied_list[curr] = check
            st.rerun()

        if st.toggle("REVELAR ANÁLISE DA ABERTURA", value=False):
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div style="background:rgba(0,0,0,0.4); padding:15px; border-left:2px solid #D4AF37; color:#bbb; font-size:13px; line-height:1.4;">{f.read()}</div>', unsafe_allow_html=True)

# 4. GESTÃO
st.write("")
with st.expander("⚙️ BASE DE DADOS"):
    t1, t2, t3 = st.tabs(["NOVO", "EDITAR", "EXCLUIR"])
    # ... (lógica das abas mantida igual à anterior)
