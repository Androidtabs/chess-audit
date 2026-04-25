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

# 2. CSS: DESIGN DE DASHBOARD TÉCNICO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -80px !important; background-color: #050505 !important; }
    
    /* REMOVE PADDING PADRÃO */
    .main .block-container { padding: 2rem !important; max-width: 1400px !important; }

    /* ESTILO DO PAINEL LATERAL DE CONTROLE */
    .control-panel {
        background-color: #0f0f0f;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #1a1a1a;
        height: fit-content;
    }

    .label-tech {
        font-size: 10px;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }

    .opening-title {
        color: #D4AF37;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 20px;
        line-height: 1.2;
    }

    /* IMAGEM DO TABULEIRO */
    .board-frame img {
        width: 100%;
        border-radius: 4px;
        border: 1px solid #1a1a1a;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
    }

    /* AJUSTE NOS BOTÕES NATIVOS PARA O LADO DIREITO */
    .stButton > button {
        width: 100% !important;
        background-color: #1a1a1a !important;
        color: #eee !important;
        border: 1px solid #333 !important;
        height: 40px !important;
        transition: 0.3s;
    }
    .stButton > button:hover {
        border-color: #D4AF37 !important;
        color: #D4AF37 !important;
    }

    /* CAIXA DE INSIGHT */
    .insight-card {
        background-color: #080808;
        border-left: 2px solid #D4AF37;
        padding: 20px;
        margin-top: 20px;
        color: #999;
        font-size: 14px;
        line-height: 1.6;
        animation: slideIn 0.4s ease;
    }
    @keyframes slideIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

# Inicialização de Estados
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]
if 'idx' not in st.session_state: st.session_state.idx = 0

# --- LAYOUT PRINCIPAL (COLUNAS) ---
col_board, col_ctrl = st.columns([2, 1], gap="large")

if imgs:
    curr = imgs[st.session_state.idx % len(imgs)]
    nome_abertura = curr.split("_")[0].replace("-", " ").upper()
    
    # ESQUERDA: O TABULEIRO
    with col_board:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div class="board-frame"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)

    # DIREITA: PAINEL DE CONTROLE
    with col_ctrl:
        st.markdown('<p class="label-tech">Protocolo de Auditoria</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="opening-title">{nome_abertura}</div>', unsafe_allow_html=True)
        
        st.markdown('<p class="label-tech">Navegação</p>', unsafe_allow_html=True)
        
        # Botões de navegação verticais ou lado a lado no painel
        c_nav1, c_nav2 = st.columns(2)
        with c_nav1:
            if st.button("‹ ANTERIOR", key="p"):
                st.session_state.idx -= 1
                st.rerun()
        with c_nav2:
            if st.button("PRÓXIMO ›", key="n"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        st.markdown('<p class="label-tech">Insights de Engine</p>', unsafe_allow_html=True)
        
        # O "REVELAR" agora é um Checkbox Estilizado (Toggle)
        revelar = st.toggle("ATIVAR ANÁLISE TÉCNICA", value=False)
        
        if revelar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    conteudo = f.read()
                st.markdown(f'<div class="insight-card">{conteudo}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="insight-card">Sem análise cadastrada.</div>', unsafe_allow_html=True)

        st.write("")
        st.markdown(f'<p style="color:#333; font-size:10px;">REGISTRO ID: {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)

# 4. GESTÃO (DISCRETA NO FINAL)
st.write("---")
with st.expander("⚙️ GERENCIAR BASE DE DADOS"):
    t1, t2 = st.tabs(["CADASTRAR", "EDITAR"])
    with t1:
        n_f = st.text_input("Nome da Variante:")
        u_f = st.file_uploader("Imagem:", type=["jpg", "png"])
        u_t = st.text_area("Texto da Análise:")
        if st.button("SALVAR"):
            if n_f and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                base = os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}")
                with open(f"{base}.jpg", "wb") as f: f.write(u_f.getbuffer())
                with open(f"{base}.txt", "w") as f: f.write(u_t)
                st.rerun()
