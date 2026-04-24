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

# 2. CSS: DESIGN DARK COM FOCO NA TAG DE ABERTURA
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container { padding-top: 0rem !important; margin-top: -30px !important; max-width: 1100px !important; }
    html, body, [class*="css"] { background-color: #080808 !important; color: #E0E0E0 !important; }
    
    .header-text { font-size: 11px; color: #444; text-transform: uppercase; text-align: center; letter-spacing: 2px; }
    .record-counter { color: #D4AF37; font-size: 12px; font-weight: 600; text-align: center; margin-bottom: 5px; }
    
    /* ESTILO DA TAG DE ABERTURA */
    .opening-tag {
        background-color: #1A1A1A;
        color: #D4AF37;
        padding: 5px 15px;
        border-radius: 4px;
        border: 1px solid #333;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }

    .centered-image-container { display: flex; justify-content: center; margin-bottom: 20px; }
    .centered-image-container img { max-height: 58vh; border: 1px solid #222; box-shadow: 0 20px 50px rgba(0,0,0,0.9); }
    
    div.stButton > button { background: transparent; color: #666; border: 1px solid #222; height: 55px; width: 55px; border-radius: 50%; display: block; margin: 0 auto !important; }
    div.stButton > button:hover { border-color: #D4AF37; color: #D4AF37; }

    .insight-box { background: #111; padding: 15px; border-bottom: 2px solid #D4AF37; text-align: center; max-width: 600px; margin: 10px auto 15px auto; }
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

st.markdown('<p class="header-text">Chess Strategy Lab // Sistema de Auditoria</p>', unsafe_allow_html=True)

# Lógica de leitura de arquivos
imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort()

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    
    # Extrai o nome da abertura removendo o timestamp final
    # Ex: Siciliana-Taimanov_20260424.jpg -> Siciliana Taimanov
    nome_exibicao = curr.split("_")[0].replace("-", " ")
    
    st.markdown(f'<p class="record-counter">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="opening-tag">📂 {nome_exibicao}</span></div>', unsafe_allow_html=True)

    img_base64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>', unsafe_allow_html=True)

    _, b1, b2, _ = st.columns([1, 0.08, 0.08, 1])
    with b1:
        if st.button("‹", key="prev"): st.session_state.idx = (st.session_state.idx - 1) % len(imgs); st.rerun()
    with b2:
        if st.button("›", key="next"): st.session_state.idx = (st.session_state.idx + 1) % len(imgs); st.rerun()

    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: 
            st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {f.read()}</div>', unsafe_allow_html=True)

st.write("")
with st.expander("⚙️ GESTÃO DE DADOS (CADASTRAR ABERTURAS)"):
    t1, t2 = st.tabs(["➕ NOVO REGISTRO", "📝 EDITAR ATUAL"])
    
    with t1:
        # CAMPO DE CADASTRO QUE VOCÊ PEDIU
        nome_abertura = st.text_input("Nome da Abertura / Variante:", placeholder="Ex: Siciliana Taimanov")
        novo_f = st.file_uploader("Upload da Posição:", type=["jpg", "png", "jpeg"])
        novo_t = st.text_area("Insight da Engine / Estudo:")
        
        if st.button("SALVAR REGISTRO"): 
            if novo_f and novo_t and nome_abertura:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Limpa o nome para evitar erro de arquivo
                nome_limpo = nome_abertura.replace(" ", "-").strip()
                base = os.path.join(IMG_DIR, f"{nome_limpo}_{ts}")
                
                with open(f"{base}.jpg", "wb") as file: file.write(novo_f.getbuffer())
                with open(f"{base}.txt", "w") as file: file.write(novo_t)
                st.success(f"Abertura '{nome_abertura}' cadastrada!")
                st.rerun()
            else:
                st.error("Preencha o nome, a imagem e o insight!")

    with t2:
        if imgs:
            st.info(f"Editando: {nome_exibicao}")
            # Aqui você também poderia editar o nome se quiséssemos complicar o código, 
            # mas por enquanto vamos focar no cadastro novo.
            novo_texto = st.text_area("Alterar Insight:", value="", key="edit_area")
            if st.button("ATUALIZAR INSIGHT"):
                path_txt_edit = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
                with open(path_txt_edit, "w") as f: f.write(novo_texto)
                st.rerun()
