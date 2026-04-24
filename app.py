import streamlit as st
import os
import base64
from datetime import datetime

st.set_page_config(page_title="Audit Protocol", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- CSS (MANTIDO E AJUSTADO PARA AS TAGS) ---
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container { padding-top: 0rem !important; margin-top: -30px !important; max-width: 1100px !important; }
    html, body, [class*="css"] { background-color: #080808 !important; color: #E0E0E0 !important; }
    
    .header-text { font-size: 11px; color: #444; text-transform: uppercase; text-align: center; letter-spacing: 2px; }
    .record-counter { color: #D4AF37; font-size: 12px; font-weight: 600; text-align: center; margin-bottom: 5px; }
    
    /* TAG DE ABERTURA */
    .opening-tag {
        background-color: #1A1A1A;
        color: #D4AF37;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #D4AF37;
        font-size: 10px;
        display: inline-block;
        margin-bottom: 15px;
        text-transform: uppercase;
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

st.markdown('<p class="header-text">Chess Strategy Lab // Auditoria de Aberturas</p>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort()

# --- FILTRO DE BUSCA (NOVO RECURSO) ---
busca = st.sidebar.text_input("🔍 Filtrar por Abertura (Ex: Siciliana)")
if busca:
    imgs = [f for f in imgs if busca.lower() in f.lower()]

if imgs:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr = imgs[st.session_state.idx]
    
    # Extrair nome da abertura do nome do arquivo
    # Esperamos o formato: Abertura_Data.jpg
    abertura_nome = curr.split("_")[0] if "_" in curr else "Não Classificada"
    
    st.markdown(f'<p class="record-counter">REGISTRO {st.session_state.idx + 1} / {len(imgs)}</p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center"><span class="opening-tag">{abertura_nome}</span></div>', unsafe_allow_html=True)

    img_base64 = get_image_base64(os.path.join(IMG_DIR, curr))
    st.markdown(f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>', unsafe_allow_html=True)

    _, b1, b2, _ = st.columns([1, 0.08, 0.08, 1])
    with b1:
        if st.button("‹", key="prev"): st.session_state.idx = (st.session_state.idx - 1) % len(imgs); st.rerun()
    with b2:
        if st.button("›", key="next"): st.session_state.idx = (st.session_state.idx + 1) % len(imgs); st.rerun()

    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    if os.path.exists(path_txt):
        with open(path_txt, "r") as f: st.markdown(f'<div class="insight-box"><b>ANÁLISE:</b> {f.read()}</div>', unsafe_allow_html=True)

st.write("")
with st.expander("⚙️ GESTÃO DE DADOS"):
    t1, t2 = st.tabs(["➕ NOVO", "📝 EDITAR"])
    with t1:
        # PADRONIZAÇÃO AQUI
        opcoes = ["Siciliana", "Inglesa", "Escandinava", "Ruy Lopez", "Gambito da Dama", "Caro-Kann", "Outra"]
        sel_abertura = st.selectbox("Tipo de Abertura:", opcoes)
        if sel_abertura == "Outra":
            sel_abertura = st.text_input("Qual abertura?")
            
        n_f = st.file_uploader("Imagem", type=["jpg", "png"])
        n_t = st.text_area("Insight:")
        if st.button("SALVAR"):
            if n_f and n_t and sel_abertura:
                # O nome do arquivo vira a tag: Abertura_Timestamp.jpg
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                nome_base = f"{sel_abertura.replace(' ', '-')}_{ts}"
                with open(os.path.join(IMG_DIR, f"{nome_base}.jpg"), "wb") as f: f.write(n_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{nome_base}.txt"), "w") as f: f.write(n_t)
                st.rerun()
    # ... (Tab de editar mantida)
