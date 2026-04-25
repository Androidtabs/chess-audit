import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE
st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: DESIGN DARK + ESTILO DA REVELAÇÃO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -85px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 1100px !important; }

    html, body, [class*="css"] { background-color: #080808 !important; color: #E0E0E0 !important; font-family: 'Inter', sans-serif; }

    .header-container {
        background: linear-gradient(90deg, rgba(10,10,10,0) 0%, rgba(20,20,20,1) 50%, rgba(10,10,10,0) 100%);
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        padding: 15px 0; margin-bottom: 25px; width: 100%;
    }

    .header-text { font-size: 12px; color: #888; text-transform: uppercase; text-align: center; letter-spacing: 4px; font-weight: 300; margin: 0; }
    .record-counter { color: #D4AF37; font-size: 12px; font-weight: 600; text-align: center; margin-bottom: 5px; }

    .opening-tag {
        background-color: #111; color: #D4AF37; padding: 5px 18px; border-radius: 2px; border: 1px solid #222;
        font-size: 13px; display: inline-block; margin-bottom: 20px; font-weight: bold; letter-spacing: 1px;
    }

    /* ESTILO DA CAIXA DE ANÁLISE REVELADA */
    .revealed-analysis {
        background: rgba(10, 10, 10, 0.95);
        color: #D4AF37;
        padding: 20px;
        text-align: center;
        border-top: 2px solid #D4AF37;
        font-size: 14px;
        line-height: 1.6;
        margin-top: -25px;
        margin-bottom: 25px;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        animation: fadeIn 0.4s ease;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

    /* BOTÕES NAVEGAÇÃO */
    div.stButton > button {
        background-color: transparent !important;
        color: #444 !important;
        border: 1px solid #1A1A1A !important;
        height: 55px !important; width: 55px !important;
        border-radius: 50% !important; margin: 0 auto !important;
    }
    div.stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

# Inicializa estados de sessão
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'show_analysis' not in st.session_state: st.session_state.show_analysis = False

st.markdown('<div class="header-container"><p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p></div>', unsafe_allow_html=True)

imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]
aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    nome_exibicao = curr.split("_")[0].replace("-", " ")
    
    st.markdown(f'<p class="record-counter">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="opening-tag">📂 {nome_exibicao}</span></div>', unsafe_allow_html=True)

    # Lógica de Imagem como Botão de Revelação
    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    
    # Criamos um container centralizado e colocamos a imagem dentro de um st.button customizado
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        # A imagem funciona como o gatilho
        if st.button("", key="img_click", help="Clique na imagem para revelar/esconder a análise"):
            st.session_state.show_analysis = not st.session_state.show_analysis
            st.rerun()
        
        # Inserimos a imagem visualmente "por cima" do botão ou logo acima
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: -75px; pointer-events: none;">
                <img src="data:image/jpeg;base64,{img_64}" style="max-height: 58vh; border: 1px solid #222; border-radius: 8px 8px 0 0;">
            </div>
        """, unsafe_allow_html=True)

        # Se o estado for 'True', mostramos a análise
        if st.session_state.show_analysis:
            path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    analise_texto = f.read()
                st.markdown(f'<div class="revealed-analysis"><b>ANÁLISE REVELADA:</b><br>{analise_texto}</div>', unsafe_allow_html=True)

    # Navegação (Reseta a visualização da análise ao mudar de registro)
    _, col2, col3, _ = st.columns([1, 0.08, 0.08, 1])
    with col2:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.session_state.show_analysis = False
            st.rerun()
    with col3:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.session_state.show_analysis = False
            st.rerun()

st.write("")
with st.expander("⚙️ GESTÃO DA BASE DE DADOS"):
    # ... (O código de gestão continua o mesmo, apenas removi para encurtar a resposta)
