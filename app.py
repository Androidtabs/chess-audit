import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: FUNDO TÁTICO + DASHBOARD REFINADO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* FUNDO COM TEXTURA DE MICRO-XADREZ / CARBONO */
    .stApp {
        margin-top: -80px !important;
        background-color: #0a0a0a !important;
        background-image:  linear-gradient(#0f0f0f 1.1px, transparent 1.1px), linear-gradient(90deg, #0f0f0f 1.1px, transparent 1.1px);
        background-size: 22px 22px; /* O padrão sutil de grade */
    }
    
    .main .block-container { padding: 2rem !important; max-width: 1300px !important; }

    /* CABEÇALHO DASHBOARD */
    .dashboard-header {
        background: rgba(15, 15, 15, 0.9);
        border: 1px solid #222;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .dashboard-header h1 {
        font-size: 14px;
        color: #D4AF37;
        text-transform: uppercase;
        letter-spacing: 6px;
        margin: 0;
    }

    /* PAINEL DE CONTROLE LATERAL */
    .control-panel {
        background: rgba(12, 12, 12, 0.95);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #1a1a1a;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        backdrop-filter: blur(10px);
    }

    .label-tech {
        font-size: 10px;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .opening-title {
        color: #D4AF37;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 20px;
        border-bottom: 1px solid #222;
        padding-bottom: 10px;
    }

    /* AJUSTE DO TABULEIRO (IMAGEM MENOR E CENTRALIZADA) */
    .board-frame {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .board-frame img {
        max-width: 85% !important; /* Reduz o tamanho do tabuleiro */
        max-height: 55vh !important;
        border: 2px solid #1a1a1a;
        border-radius: 6px;
        box-shadow: 0 40px 80px rgba(0,0,0,0.9);
    }

    /* BOTÕES TÁTICOS */
    .stButton > button {
        width: 100% !important;
        background-color: #1a1a1a !important;
        color: #aaa !important;
        border: 1px solid #333 !important;
        height: 42px !important;
        border-radius: 6px !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
    }
    .stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
    }

    /* CARD DE INSIGHTS */
    .insight-card {
        background: rgba(5, 5, 5, 0.6);
        border-left: 3px solid #D4AF37;
        padding: 20px;
        margin-top: 20px;
        color: #999;
        font-size: 14px;
        line-height: 1.6;
        font-style: italic;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

# Lógica de Dados
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]
if 'idx' not in st.session_state: st.session_state.idx = 0

# 1. HEADER DO DASHBOARD
st.markdown('<div class="dashboard-header"><h1>Chess Strategy Lab // Estudo de Aberturas</h1></div>', unsafe_allow_html=True)

# 2. LAYOUT PRINCIPAL (TABULEIRO : PAINEL)
col_board, col_ctrl = st.columns([1.6, 1], gap="large")

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    nome_abertura = curr.split("_")[0].replace("-", " ").upper()
    
    # ESQUERDA: O TABULEIRO CENTRALIZADO
    with col_board:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div class="board-frame"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)

    # DIREITA: O PAINEL DE COMANDO
    with col_ctrl:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
        st.markdown('<p class="label-tech">Variante em Estudo</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="opening-title">{nome_abertura}</div>', unsafe_allow_html=True)
        
        # Navegação
        st.markdown('<p class="label-tech">Navegação da Base</p>', unsafe_allow_html=True)
        c_n1, c_n2 = st.columns(2)
        with c_n1:
            if st.button("‹ ANTERIOR", key="p"):
                st.session_state.idx -= 1
                st.rerun()
        with c_n2:
            if st.button("PRÓXIMO ›", key="n"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        st.markdown('<p class="label-tech">Motor de Análise</p>', unsafe_allow_html=True)
        
        # Toggle de Análise
        revelar = st.toggle("ATIVAR FEEDBACK TÉCNICO", value=False)
        
        if revelar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    conteudo = f.read()
                st.markdown(f'<div class="insight-card">{conteudo}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="insight-card">Nenhum dado de engine disponível para esta posição.</div>', unsafe_allow_html=True)

        st.markdown(f'<p style="color:#333; font-size:10px; margin-top:20px; text-align:right;">DATA_ID: {curr.split("_")[1].split(".")[0] if "_" in curr else "000"}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 3. GESTÃO DE DADOS (ABAIXO)
st.write("")
with st.expander("⚙️ GERENCIAR REGISTROS"):
    t1, t2 = st.tabs(["CADASTRAR POSIÇÃO", "EDITAR ANÁLISE"])
    with t1:
        n_f = st.text_input("Nome da Variante (ex: Taimanov):")
        u_f = st.file_uploader("Screenshot do Tabuleiro:", type=["jpg", "png"])
        u_t = st.text_area("Insight da Engine:")
        if st.button("SALVAR REGISTRO"):
            if n_f and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                base = os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}")
                with open(f"{base}.jpg", "wb") as f: f.write(u_f.getbuffer())
                with open(f"{base}.txt", "w") as f: f.write(u_t)
                st.rerun()
    with t2:
        if imgs:
            path_txt_edit = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            txt_at = ""
            if os.path.exists(path_txt_edit):
                with open(path_txt_edit, "r") as f: txt_at = f.read()
            edt_t = st.text_area("Editar Texto:", value=txt_at)
            if st.button("ATUALIZAR DADOS"):
                with open(path_txt_edit, "w") as f: f.write(edt_t); st.rerun()
