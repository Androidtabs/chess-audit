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

# 2. CSS: DESIGN PREMIUM E CORREÇÃO DE BOTÕES
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    
    /* AJUSTE DO TOPO PARA REMOVER ESPAÇO EM BRANCO */
    .stApp { margin-top: -85px !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0rem !important; }
    [data-testid="stAppViewBlockContainer"] { padding-top: 0rem !important; }
    .main .block-container { padding-top: 0rem !important; max-width: 1100px !important; }

    /* ESTÉTICA DARK */
    html, body, [class*="css"] { 
        background-color: #080808 !important; 
        color: #E0E0E0 !important; 
        font-family: 'Inter', sans-serif; 
    }

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

    /* CONTAINER DO TABULEIRO */
    .img-display-container { display: flex; justify-content: center; margin-bottom: 15px; }
    .img-display-container img {
        max-height: 58vh; border: 1px solid #222; border-radius: 8px;
        box-shadow: 0 20px 60px rgba(0,0,0,1);
    }

    /* --- ESTILO DAS SETAS (CÍRCULOS) --- */
    .stHorizontalBlock div.stButton > button {
        background-color: transparent !important; 
        color: #444 !important; 
        border: 1px solid #1A1A1A !important;
        height: 55px !important; 
        width: 55px !important; 
        border-radius: 50% !important; 
        margin: 0 auto !important;
        font-size: 22px !important;
    }
    .stHorizontalBlock div.stButton > button:hover { border-color: #D4AF37 !important; color: #D4AF37 !important; }

    /* --- ESTILO DO BOTÃO REVELAR (RETÂNGULO CENTRAL) --- */
    /* Garante que o botão de revelar não vire um círculo esmagado */
    div.stButton > button[kind="secondary"] {
        border-radius: 4px !important;
        width: 320px !important; 
        height: 48px !important;
        margin: 0 auto !important;
        background-color: #111 !important;
        color: #D4AF37 !important;
        border: 1px solid #222 !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        display: block !important;
    }

    /* CAIXA DE ANÁLISE REVELADA */
    .revealed-box {
        background-color: #0A0A0A; padding: 25px; border-left: 3px solid #D4AF37;
        text-align: center; max-width: 650px; margin: 25px auto; color: #BBB;
        font-size: 15px; line-height: 1.6; animation: fadeIn 0.5s ease;
        border-radius: 0 8px 8px 0;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* BOTÕES DENTRO DA GESTÃO */
    .stExpander div.stButton > button {
        border-radius: 4px !important; 
        width: 100% !important; 
        height: 45px !important;
        background-color: #111 !important; 
        color: #D4AF37 !important; 
        border: 1px solid #222 !important;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

# Inicialização de estados
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'revelar' not in st.session_state: st.session_state.revelar = False

# Cabeçalho Premium
st.markdown('<div class="header-container"><p class="header-text">Chess Strategy Lab // Estudo de Aberturas</p></div>', unsafe_allow_html=True)

imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]
aberturas_existentes = sorted(list(set([f.split("_")[0].replace("-", " ") for f in imgs])))

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    nome_exibicao = curr.split("_")[0].replace("-", " ")
    
    st.markdown(f'<p class="record-counter">ESTUDO {st.session_state.idx + 1} DE {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="opening-tag">📂 {nome_exibicao}</span></div>', unsafe_allow_html=True)

    # Exibição da Imagem
    img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="img-display-container"><img src="data:image/jpeg;base64,{img_64}"></div>', unsafe_allow_html=True)
    
    # Botão de Revelação (Centralizado)
    label_btn = "OCULTAR ANÁLISE" if st.session_state.revelar else "REVELAR ANÁLISE"
    if st.button(label_btn, key="btn_revelar"):
        st.session_state.revelar = not st.session_state.revelar
        st.rerun()

    # Conteúdo Revelado
    if st.session_state.revelar:
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        if os.path.exists(path_txt):
            with open(path_txt, "r") as f: conteudo = f.read()
            st.markdown(f'<div class="revealed-box"><b>INSIGHT TÉCNICO:</b><br>{conteudo}</div>', unsafe_allow_html=True)

    # Navegação (Setas)
    st.write("")
    c1, c2, c3, c4 = st.columns([1, 0.08, 0.08, 1])
    with c2:
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.session_state.revelar = False
            st.rerun()
    with c3:
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.session_state.revelar = False
            st.rerun()

# 3. GESTÃO DE DADOS (CADASTRAR E EDITAR)
st.write("")
with st.expander("⚙️ GESTÃO DA BASE DE DADOS"):
    t1, t2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR ATUAL"])
    with t1:
        opcoes = ["-- Selecione --"] + aberturas_existentes + ["[ + NOVA ]"]
        escolha = st.selectbox("Selecione a Abertura:", opcoes)
        nome_f = st.text_input("Nome da Variante:") if escolha == "[ + NOVA ]" else (escolha if escolha != "-- Selecione --" else "")
        up_f = st.file_uploader("Captura:", type=["jpg", "png", "jpeg"])
        up_t = st.text_area("Nota Técnica:")
        if st.button("SALVAR NA BASE"): 
            if up_f and up_t and nome_f:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_limpo = nome_f.replace(" ", "-").strip()
                base = os.path.join(IMG_DIR, f"{nome_limpo}_{ts}")
                with open(f"{base}.jpg", "wb") as f: f.write(up_f.getbuffer())
                with open(f"{base}.txt", "w") as f: f.write(up_t)
                st.rerun()
    with t2:
        if imgs:
            path_txt_edit = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
            txt_atual = ""
            if os.path.exists(path_txt_edit):
                with open(path_txt_edit, "r") as f: txt_atual = f.read()
            edt_t = st.text_area("Editar Análise:", value=txt_atual, key="edit_area")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("ATUALIZAR"):
                    with open(path_txt_edit, "w") as f: f.write(edt_t); st.rerun()
            with c2:
                if st.button("🗑️ DELETAR"):
                    if os.path.exists(os.path.join(IMG_DIR, curr)): os.remove(os.path.join(IMG_DIR, curr))
                    if os.path.exists(path_txt_edit): os.remove(path_txt_edit)
                    st.session_state.idx = 0; st.rerun()
