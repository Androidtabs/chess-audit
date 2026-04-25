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

# 2. CSS: DESIGN HUD E INPUTS CUSTOMIZADOS
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
        padding: 15px;
        text-align: center;
        margin-bottom: 30px;
    }
    .custom-header h1 {
        font-size: 13px; color: #D4AF37; text-transform: uppercase; letter-spacing: 7px; font-weight: 300; margin: 0;
    }

    /* ESTILIZAÇÃO DO PAINEL HUD (COLUNA 2) */
    [data-testid="column"]:nth-of-type(2) {
        background: #111111 !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border: 1px solid #1a1a1a !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important;
        min-height: 600px !important;
    }

    /* CONTADOR E JUMP BOX */
    .image-counter {
        color: #D4AF37;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: -1px;
    }
    .label-small {
        font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; font-weight: 600;
    }

    /* ESTILO DO CAMPO DE SALTO (INPUT) */
    .stNumberInput input {
        background-color: #1a1a1a !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
        font-weight: bold !important;
    }

    /* NOME DA VARIANTE (DE VOLTA) */
    .variant-box {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 25px;
    }
    .variant-title {
        color: #D4AF37; font-size: 18px; font-weight: 800; text-transform: uppercase; margin: 0;
    }

    /* STATUS DE ESTUDO */
    .status-badge {
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 15px;
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

st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Auditoria de Aberturas</h1></div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    # Lógica de Salto (Jump)
    def update_jump():
        st.session_state.idx = st.session_state.jump_val - 1

    curr = imgs[st.session_state.idx % len(imgs)]
    nome_raw = curr.split("_")[0].replace("-", " ")
    
    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div style="display:flex; justify-content:center;"><img src="data:image/jpeg;base64,{img_64}" style="max-width:85%; border-radius:4px; border:1px solid #222; box-shadow: 0 40px 100px rgba(0,0,0,1);"></div>', unsafe_allow_html=True)

    # DIREITA: Painel HUD
    with col_right:
        # 1. CONTADOR E SALTO RÁPIDO
        c_count, c_jump = st.columns([1, 1])
        with c_count:
            st.markdown('<p class="label-small">Posição Atual</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="image-counter">{st.session_state.idx + 1} <span style="font-size:16px; color:#333;">/ {len(imgs)}</span></div>', unsafe_allow_html=True)
        
        with c_jump:
            st.markdown('<p class="label-small">Salto Rápido</p>', unsafe_allow_html=True)
            st.number_input("Ir para:", min_value=1, max_value=len(imgs), value=st.session_state.idx + 1, key="jump_val", on_change=update_jump, label_visibility="collapsed")

        # 2. STATUS DE ESTUDO
        is_studied = st.session_state.studied_list.get(curr, False)
        if is_studied:
            st.markdown('<div class="status-badge status-studied">✓ Estudo Concluído</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-awaiting">⚠ Aguardando Estudo</div>', unsafe_allow_html=True)

        # 3. VARIANTE (RECOLOCADA)
        st.markdown('<p class="label-small">Variante do Adversário</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="variant-box"><p class="variant-title">{nome_raw}</p></div>', unsafe_allow_html=True)

        # 4. NAVEGAÇÃO
        st.markdown('<p class="label-small">Navegação Sequencial</p>', unsafe_allow_html=True)
        c_nav1, c_nav2 = st.columns(2)
        with c_nav1:
            if st.button("‹ VOLTAR", key="prev"):
                st.session_state.idx -= 1
                st.rerun()
        with c_nav2:
            if st.button("AVANÇAR ›", key="next"):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        # 5. CHECKPOINT E INSIGHTS
        st.markdown('<p class="label-small">Controle de Progresso</p>', unsafe_allow_html=True)
        check = st.toggle("CONCLUIR ESTUDO DA POSIÇÃO", value=is_studied, key=f"chk_{curr}")
        if check != is_studied:
            st.session_state.studied_list[curr] = check
            st.rerun()

        revelar = st.toggle("REVELAR REFUTAÇÃO TÉCNICA", value=False)
        if revelar:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div style="background:rgba(0,0,0,0.4); padding:20px; border-left:2px solid #D4AF37; color:#bbb; font-size:14px; line-height:1.6;">{f.read()}</div>', unsafe_allow_html=True)

# 3. GESTÃO
st.write("")
with st.expander("⚙️ MANAGE DATABASE"):
    t1, t2 = st.tabs(["NOVO", "EDITAR"])
    with t1:
        n_f = st.text_input("Abertura/Variante:")
        u_f = st.file_uploader("Screenshot:", type=["jpg", "png"])
        u_t = st.text_area("Insight da Engine:")
        if st.button("SALVAR REGISTRO"):
            if n_f and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{n_f.replace(' ', '-')}_{ts}.txt"), "w") as f: f.write(u_t)
                st.rerun()
