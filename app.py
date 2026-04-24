# --- 1. TABULEIRO (MANTIDO VIA HTML PARA CENTRALIZAÇÃO TOTAL) ---
img_base64 = get_image_base64(path_img)
st.markdown(
    f'<div class="centered-image-container"><img src="data:image/jpeg;base64,{img_base64}"></div>',
    unsafe_allow_html=True
)

# --- 2. NOVO CONTROLE DE SETAS (CENTRALIZAÇÃO ABSOLUTA) ---
# Em vez de colunas st.columns, usamos HTML para garantir que o centro seja perfeito
st.markdown("""
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: -10px; margin-bottom: 20px;">
        <div id="btn-prev"></div>
        <div id="btn-next"></div>
    </div>
""", unsafe_allow_html=True)

# Como o Streamlit não permite botões dentro de markdown puro, 
# usamos uma estrutura de colunas bem curta só para os botões, 
# mas com gap zero no CSS.
col1, col2 = st.columns([1, 1], gap="small")
# Ajuste de margens negativas para "colar" os botões um no outro no centro
st.markdown("""
    <style>
    [data-testid="column"]:nth-of-type(1) { text-align: right !important; padding-right: 10px !important; }
    [data-testid="column"]:nth-of-type(2) { text-align: left !important; padding-left: 10px !important; }
    div[data-testid="stHorizontalBlock"] { justify-content: center !important; }
    </style>
""", unsafe_allow_html=True)

with col1:
    if st.button("‹", key="prev"):
        st.session_state.idx = (st.session_state.idx - 1) % total
        st.rerun()
with col2:
    if st.button("›", key="next"):
        st.session_state.idx = (st.session_state.idx + 1) % total
        st.rerun()
