import streamlit as st
import os
from datetime import datetime

# Configuração para esconder a barra lateral por padrão e usar a largura total
st.set_page_config(page_title="Audit Chess", layout="centered", initial_sidebar_state="collapsed")

# CSS para esconder a sidebar e focar no conteúdo
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 600px; }
    .stImage { border-radius: 10px; border: 2px solid #444; }
    div.stButton > button {
        height: 80px; background-color: #333; color: white;
        font-size: 25px; border-radius: 10px; border: none;
    }
    .insight-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 10px;
        border-left: 5px solid #00ff00; margin-top: 10px; font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)

if 'idx' not in st.session_state: st.session_state.idx = 0

st.title("♟️ Auditoria de Elite")

imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
imgs.sort(reverse=True)

if not imgs:
    st.info("Nenhuma jogada. Use o menu 'Cadastrar' no final da página.")
else:
    if st.session_state.idx >= len(imgs): st.session_state.idx = 0
    total = len(imgs)
    curr = imgs[st.session_state.idx]
    p = os.path.join(IMG_DIR, curr)
    t_p = p.replace(".jpg", ".txt")

    # NAVEGAÇÃO E IMAGEM (TUDO NA MESMA LINHA)
    col_ant, col_mid, col_prox = st.columns([0.6, 4, 0.6])
    
    with col_ant:
        st.write("#") # Alinhamento vertical
        if st.button("‹", key="prev"):
            st.session_state.idx = (st.session_state.idx - 1) % total
            st.rerun()

    with col_mid:
        st.image(p, use_container_width=True)
        if os.path.exists(t_p):
            with open(t_p, "r") as file: texto = file.read()
            st.markdown(f'<div class="insight-box"><b>Insight:</b><br>{texto}</div>', unsafe_allow_html=True)

    with col_prox:
        st.write("#")
        if st.button("›", key="next"):
            st.session_state.idx = (st.session_state.idx + 1) % total
            st.rerun()

    st.caption(f"Registro {st.session_state.idx + 1} de {total}")

st.write("---")

# --- FERRAMENTAS ESCONDIDAS (SÓ APARECEM QUANDO VOCÊ CLICA) ---
col1, col2 = st.columns(2)

with col1:
    with st.expander("📥 Cadastrar Novo"):
        f = st.file_uploader("Print", type=["jpg", "png", "jpeg"])
        c = st.text_area("Insight da Engine:")
        if st.button("Salvar Agora"):
            if f and c:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = os.path.join(IMG_DIR, f"{ts}.jpg")
                with open(path, "wb") as file: file.write(f.getbuffer())
                with open(path.replace(".jpg", ".txt"), "w") as file: file.write(c)
                st.success("Salvo!")
                st.rerun()

with col2:
    with st.expander("⚙️ Editar/Excluir"):
        if imgs:
            novo = st.text_area("Editar Insight Atual:", value=texto if 'texto' in locals() else "")
            if st.button("Atualizar Texto"):
                with open(t_p, "w") as file: file.write(novo)
                st.rerun()
            if st.button("🗑️ Apagar este Registro"):
                os.remove(p); os.remove(t_p)
                st.session_state.idx = 0
                st.rerun()
