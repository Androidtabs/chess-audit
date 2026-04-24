import streamlit as st
import os
from datetime import datetime

# Configuração de Página: Layout centralizado para evitar distorção
st.set_page_config(page_title="Chess Lab", layout="centered", initial_sidebar_state="collapsed")

# CSS: Estética "Cyber-Aviation" (Preto, Branco e Cinza Técnico)
st.markdown("""
    <style>
    /* 1. Reset Total e Fundo */
    [data-testid="stHeader"] {display: none !important;}
    .main .block-container {
        padding-top: 1rem !important;
        max-width: 600px !important; /* Limita a largura para o tabuleiro não explodir */
    }
    html, body, [class*="css"] {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Título de Sistema (Ultra limpo) */
    .system-title {
        text-align: center;
        font-size: 10px;
        letter-spacing: 4px;
        color: #444;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* 3. O Tabuleiro (Ajuste de Proporção) */
    .stImage img {
        border: 1px solid #222;
        border-radius: 4px;
        max-height: 400px !important; /* Fixa uma altura que cabe em qualquer tela */
        object-fit: contain;
    }

    /* 4. Caixa de Insight (Estilo 'Paper') */
    .insight-box {
        background-color: #0A0A0A;
        padding: 20px;
        border-left: 2px solid #FFFFFF;
        margin-top: 10px;
        line-height: 1.6;
    }
    .insight-label {
        font-size: 9px;
        color: #666;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .insight-text {
        font-size: 15px;
        color: #CCC;
    }

    /* 5. Navegação Minimalista (Embaixo da Imagem) */
    .nav-btn {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid #222 !important;
        color: #666 !important;
        width: 100% !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #FFF !important;
        color: #FFF !important;
    }

    /* Esconde elementos do Streamlit */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
if 'idx' not in st.session_state: st.session_state.idx = 0

# Título Superior
st.markdown('<div class="system-title">Opening Strategy Lab</div>', unsafe_allow_html=True)

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Aguardando inserção de dados.")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    curr_img = imgs[st.session_state.idx]
    p_img = os.path.join(IMG_DIR, curr_img)
    p_txt = p_img.replace(".jpg", ".txt")

    # Exibição do Tabuleiro (Centralizado e com altura fixa)
    st.image(p_img, use_container_width=True)

    # Navegação (Logo abaixo da imagem)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Anterior", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % len(imgs)
            st.rerun()
    with c2:
        if st.button("Próximo", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % len(imgs)
            st.rerun()

    # Caixa de Insight
    if os.path.exists(p_txt):
        with open(p_txt, "r") as f: texto = f.read()
        st.markdown(f'''
            <div class="insight-box">
                <div class="insight-label">Analysis Node // Post-Game</div>
                <div class="insight-text">{texto}</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown(f"<p style='text-align:center; color:#222; font-size:10px; margin-top:20px;'>{st.session_state.idx + 1} / {len(imgs)}</p>", unsafe_allow_html=True)

# Gestão Oculta no Fundo
st.write("<br>"*2, unsafe_allow_html=True)
with st.expander("Gereneciamento de Dados"):
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Upload", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight:")
        if st.button("Salvar"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                p = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(p, "wb") as file: file.write(f.getbuffer())
                with open(p.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.rerun()
    with c2:
        if imgs:
            novo = st.text_area("Editar:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar"):
                with open(p_txt, "w") as file: file.write(novo)
                st.rerun()
            if st.button("Deletar"):
                os.remove(p_img); os.remove(p_txt)
                st.session_state.idx = 0
                st.rerun()
