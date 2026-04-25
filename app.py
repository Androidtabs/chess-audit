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

# 2. CSS: DESIGN HUD REFINADO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp {
        margin-top: -85px !important;
        background-color: #0d0d0d !important;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 30px 30px;
    }
    .main .block-container { padding: 1.5rem !important; max-width: 1350px !important; }

    .custom-header {
        background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%);
        border: 1px solid #222; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 30px;
    }
    .custom-header h1 {
        font-size: 13px; color: #D4AF37; text-transform: uppercase; letter-spacing: 7px; font-weight: 300; margin: 0;
    }

    [data-testid="column"]:nth-of-type(2) {
        background: #111111 !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border: 1px solid #1a1a1a !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important;
        min-height: 600px !important;
    }

    .label-tech { font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; font-weight: 600; }
    
    /* BLOCO DE ABERTURA (SUA LINHA) */
    .my-line-box {
        border-left: 3px solid #D4AF37;
        padding-left: 15px;
        margin-bottom: 20px;
    }
    .my-line-title { color: #D4AF37; font-size: 18px; font-weight: 800; text-transform: uppercase; margin: 0; }

    /* BLOCO DO ADVERSÁRIO */
    .opp-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 25px;
        border: 1px solid #222;
    }
    .opp-title { color: #eee; font-size: 14px; font-weight: 600; text-transform: uppercase; margin: 0; }

    .total-display { color: #333; font-size: 24px; font-weight: 900; margin-top: 5px; }
    .stNumberInput input { color: #D4AF37 !important; font-size: 32px !important; font-weight: 900 !important; }

    .status-badge {
        padding: 6px 12px; border-radius: 4px; font-size: 10px; font-weight: bold;
        text-transform: uppercase; display: inline-block; margin-bottom: 15px;
    }
    .status-studied { background-color: rgba(0, 255, 100, 0.1); color: #00FF64; border: 1px solid #00FF64; }
    .status-awaiting { background-color: rgba(255, 50, 50, 0.1); color: #FF3232; border: 1px solid #FF3232; }

    .stButton > button {
        width: 100% !important; background-color: #1a1a1a !important; color: #eee !important;
        border: 1px solid #333 !important; border-radius: 20px !important; font-size: 11px !important;
    }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'studied_list' not in st.session_state: st.session_state.studied_list = {}

st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Auditoria de Aberturas</h1></div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    def handle_jump(): st.session_state.idx = st.session_state.nav_input - 1
    curr = imgs[st.session_state.idx % len(imgs)]
    
    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(os.path.join(IMG_DIR, curr))
        st.markdown(f'<div style="display:flex; justify-content:center;"><img src="data:image/jpeg;base64,{img_64}" style="max-width:85%; border-radius:4px; border:1px solid #222; box-shadow: 0 40px 100px rgba(0,0,0,1);"></div>', unsafe_allow_html=True)

    # DIREITA: Painel de Confronto
    with col_right:
        # Navegação
        st.markdown('<p class="label-tech">Navegação</p>', unsafe_allow_html=True)
        c_in, c_tot = st.columns([0.4, 1])
        with c_in: st.number_input("Pos", min_value=1, max_value=len(imgs), value=st.session_state.idx + 1, key="nav_input", on_change=handle_jump, label_visibility="collapsed")
        with c_tot: st.markdown(f'<div class="total-display">/ {len(imgs)}</div>', unsafe_allow_html=True)

        # Status
        is_studied = st.session_state.studied_list.get(curr, False)
        st.markdown(f'<div class="status-badge {"status-studied" if is_studied else "status-awaiting"}">{"✓ Estudo Concluído" if is_studied else "⚠ Aguardando Estudo"}</div>', unsafe_allow_html=True)

        # --- DADOS DA PARTIDA ---
        path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
        minha_abertura = "Não informada"
        analise_texto = ""
        variante_adv = curr.split("_")[0].replace("-", " ")

        if os.path.exists(path_txt):
            with open(path_txt, "r") as f:
                linhas = f.readlines()
                if len(linhas) > 0:
                    minha_abertura = linhas[0].strip()
                    analise_texto = "".join(linhas[1:])

        st.markdown('<p class="label-tech">Minha Abertura</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="my-line-box"><p class="my-line-title">{minha_abertura.upper()}</p></div>', unsafe_allow_html=True)

        st.markdown('<p class="label-tech">Resposta do Adversário</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="opp-box"><p class="opp-title">{variante_adv}</p></div>', unsafe_allow_html=True)

        # Botões de Navegação
        c_p, c_n = st.columns(2)
        with c_p: 
            if st.button("‹ VOLTAR"): st.session_state.idx -= 1; st.rerun()
        with c_n: 
            if st.button("AVANÇAR ›"): st.session_state.idx += 1; st.rerun()

        st.write("")
        # Insights
        st.markdown('<p class="label-tech">Controle de Auditoria</p>', unsafe_allow_html=True)
        check = st.toggle("MARCAR COMO CONCLUÍDO", value=is_studied, key=f"chk_{curr}")
        if check != is_studied: st.session_state.studied_list[curr] = check; st.rerun()

        if st.toggle("REVELAR ANÁLISE DA ABERTURA", value=False):
            st.markdown(f'<div style="background:rgba(0,0,0,0.4); padding:20px; border-left:2px solid #D4AF37; color:#bbb; font-size:14px; line-height:1.6;">{analise_texto}</div>', unsafe_allow_html=True)

# 3. GESTÃO (ATUALIZADA COM NOVO CAMPO)
st.write("")
with st.expander("⚙️ BASE DE DADOS"):
    t1, t2 = st.tabs(["NOVO REGISTRO", "EDITAR"])
    with t1:
        my_op = st.text_input("Sua Abertura (ex: Taimanov):")
        adv_var = st.text_input("Variante do Adversário (ex: Ataque Inglês):")
        u_f = st.file_uploader("Screenshot:", type=["jpg", "png"])
        u_t = st.text_area("Análise Técnica:")
        if st.button("SALVAR"):
            if my_op and adv_var and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"{adv_var.replace(' ', '-')}_{ts}"
                with open(os.path.join(IMG_DIR, f"{fn}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{fn}.txt"), "w") as f:
                    f.write(f"{my_op}\n{u_t}") # Salva a abertura na primeira linha
                st.rerun()
