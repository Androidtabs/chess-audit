import streamlit as st
import os
import base64
from datetime import datetime

# 1. CONFIGURAÇÃO BASE
st.set_page_config(page_title="Strategy Lab", layout="wide", initial_sidebar_state="collapsed")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. CSS: DESIGN TÁTICO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { margin-top: -85px !important; background-color: #0d0d0d !important; background-image: radial-gradient(#1a1a1a 1px, transparent 1px); background-size: 30px 30px; }
    .main .block-container { padding: 1.5rem !important; max-width: 1350px !important; }
    .custom-header { background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%); border: 1px solid #222; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 30px; }
    .custom-header h1 { font-size: 13px; color: #D4AF37; text-transform: uppercase; letter-spacing: 7px; font-weight: 300; margin: 0; }
    [data-testid="column"]:nth-of-type(2) { background: #111111 !important; padding: 25px !important; border-radius: 15px !important; border: 1px solid #1a1a1a !important; box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important; min-height: 600px !important; }
    .label-tech { font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; font-weight: 600; }
    .data-display-box { background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 6px; margin-bottom: 20px; border: 1px solid #1a1a1a; }
    .my-line-text { color: #D4AF37; font-size: 18px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .opp-line-text { color: #eee; font-size: 14px; font-weight: 600; text-transform: uppercase; margin: 0; }
    .total-display { color: #333; font-size: 24px; font-weight: 900; margin-top: 5px; }
    .stNumberInput div[data-baseweb="input"] { background-color: transparent !important; border: none !important; width: 100px !important; }
    .stNumberInput input { color: #D4AF37 !important; font-size: 32px !important; font-weight: 900 !important; padding: 0 !important; }
    .status-badge { padding: 6px 12px; border-radius: 4px; font-size: 10px; font-weight: bold; text-transform: uppercase; display: inline-block; margin-bottom: 15px; }
    .status-studied { background-color: rgba(0, 255, 100, 0.1); color: #00FF64; border: 1px solid #00FF64; }
    .status-awaiting { background-color: rgba(255, 50, 50, 0.1); color: #FF3232; border: 1px solid #FF3232; }
    .stButton > button { width: 100% !important; background-color: #1a1a1a !important; color: #eee !important; border: 1px solid #333 !important; border-radius: 20px !important; height: 40px !important;}
    .stButton > button:disabled { opacity: 0.1; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. DIRETÓRIO
IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

# --- ESTADO DE SESSÃO ---
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'studied_list' not in st.session_state: st.session_state.studied_list = {}

st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Estudo de Aberturas</h1></div>', unsafe_allow_html=True)
col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    # Segurança de Índice
    st.session_state.idx = max(0, min(st.session_state.idx, len(imgs) - 1))
    
    curr = imgs[st.session_state.idx]
    path_jpg = os.path.join(IMG_DIR, curr)
    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    path_op = os.path.join(IMG_DIR, curr.replace(".jpg", "_op.txt"))

    # ESQUERDA: Tabuleiro
    with col_left:
        img_64 = get_image_base64(path_jpg)
        st.markdown(f'<div style="display:flex; justify-content:center;"><img src="data:image/jpeg;base64,{img_64}" style="max-width:85%; border-radius:4px; border:1px solid #222; box-shadow: 0 40px 100px rgba(0,0,0,1);"></div>', unsafe_allow_html=True)

    # DIREITA: Painel
    with col_right:
        st.markdown('<p class="label-tech">Navegação</p>', unsafe_allow_html=True)
        c_in, c_tot = st.columns([0.4, 1])
        with c_in:
            v_input = st.number_input("Pos", min_value=1, max_value=len(imgs), value=st.session_state.idx + 1, key=f"nav_{st.session_state.idx}", label_visibility="collapsed")
            if v_input != st.session_state.idx + 1:
                st.session_state.idx = v_input - 1
                st.rerun()
        with c_tot: st.markdown(f'<div class="total-display">/ {len(imgs)}</div>', unsafe_allow_html=True)

        is_studied = st.session_state.studied_list.get(curr, False)
        st.markdown(f'<div class="status-badge {"status-studied" if is_studied else "status-awaiting"}">{"✓ Estudo Concluído" if is_studied else "⚠ Aguardando Estudo"}</div>', unsafe_allow_html=True)

        # Dados da Base
        my_opening = "NÃO INFORMADA"
        if os.path.exists(path_op):
            with open(path_op, "r") as f: my_opening = f.read()

        st.markdown('<p class="label-tech">Minha Abertura</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-display-box" style="border-left: 3px solid #D4AF37;"><p class="my-line-text">{my_opening}</p></div>', unsafe_allow_html=True)

        st.markdown('<p class="label-tech">Variante do Adversário</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-display-box"><p class="opp-line-text">{curr.split("_")[0].replace("-", " ")}</p></div>', unsafe_allow_html=True)

        c_p, c_n = st.columns(2)
        with c_p: 
            if st.button("‹ VOLTAR", disabled=(st.session_state.idx <= 0)):
                st.session_state.idx -= 1
                st.rerun()
        with c_n: 
            if st.button("AVANÇAR ›", disabled=(st.session_state.idx >= len(imgs) - 1)):
                st.session_state.idx += 1
                st.rerun()

        st.write("")
        check = st.toggle("CONCLUIR REVISÃO", value=is_studied, key=f"chk_{curr}")
        if check != is_studied:
            st.session_state.studied_list[curr] = check
            st.rerun()

        if st.toggle("REVELAR ANÁLISE DA ABERTURA", value=False):
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f:
                    st.markdown(f'<div style="background:rgba(0,0,0,0.4); padding:20px; border-left:2px solid #D4AF37; color:#bbb; font-size:14px; line-height:1.6;">{f.read()}</div>', unsafe_allow_html=True)

# 4. GESTÃO DE BASE (INCLUINDO REMOÇÃO)
st.write("---")
with st.expander("⚙️ BASE DE DADOS (CADASTRAR / EDITAR / EXCLUIR)"):
    t1, t2, t3 = st.tabs(["NOVO REGISTRO", "EDITAR ATUAL", "EXCLUIR ATUAL"])
    
    with t1:
        new_my = st.text_input("Sua Abertura:")
        new_adv = st.text_input("Variante Adversário:")
        u_f = st.file_uploader("Screenshot:", type=["jpg", "png"], key="up_n")
        u_t = st.text_area("Análise:")
        if st.button("SALVAR NOVO"):
            if new_my and new_adv and u_f and u_t:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                fn = f"{new_adv.replace(' ', '-')}_{ts}"
                with open(os.path.join(IMG_DIR, f"{fn}.jpg"), "wb") as f: f.write(u_f.getbuffer())
                with open(os.path.join(IMG_DIR, f"{fn}.txt"), "w") as f: f.write(u_t)
                with open(os.path.join(IMG_DIR, f"{fn}_op.txt"), "w") as f: f.write(new_my)
                st.rerun()

    with t2:
        if imgs:
            st.write(f"Editando: `{curr}`")
            e_my = st.text_input("Minha Abertura:", value=my_opening, key="e_my")
            e_adv = st.text_input("Variante Adversário:", value=curr.split("_")[0].replace("-", " "), key="e_adv")
            e_img = st.file_uploader("Trocar Foto:", type=["jpg", "png"], key="e_img")
            c_an = ""
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f: c_an = f.read()
            e_an = st.text_area("Análise:", value=c_an, key="e_an")
            if st.button("ATUALIZAR DADOS"):
                # (Lógica de renomear e salvar mantida)
                new_pref = e_adv.replace(" ", "-")
                old_pref = curr.split("_")[0]
                t_c = curr
                if new_pref != old_pref:
                    ts_part = curr.split("_", 1)[1]
                    nn = f"{new_pref}_{ts_part}"
                    os.rename(path_jpg, os.path.join(IMG_DIR, nn))
                    os.rename(path_txt, os.path.join(IMG_DIR, nn.replace(".jpg", ".txt")))
                    os.rename(path_op, os.path.join(IMG_DIR, nn.replace(".jpg", "_op.txt")))
                    t_c = nn
                if e_img:
                    with open(os.path.join(IMG_DIR, t_c), "wb") as f: f.write(e_img.getbuffer())
                with open(os.path.join(IMG_DIR, t_c.replace(".jpg", "_op.txt")), "w") as f: f.write(e_my)
                with open(os.path.join(IMG_DIR, t_c.replace(".jpg", ".txt")), "w") as f: f.write(e_an)
                st.rerun()

    with t3:
        if imgs:
            st.error(f"CUIDADO: Você está prestes a apagar o registro da posição {st.session_state.idx + 1}")
            st.write(f"**Variante:** {curr.split('_')[0].replace('-', ' ')}")
            if st.button("CONFIRMAR EXCLUSÃO PERMANENTE"):
                # Remove os 3 arquivos
                if os.path.exists(path_jpg): os.remove(path_jpg)
                if os.path.exists(path_txt): os.remove(path_txt)
                if os.path.exists(path_op): os.remove(path_op)
                
                # Ajusta o índice para não dar erro após apagar
                if st.session_state.idx > 0:
                    st.session_state.idx -= 1
                else:
                    st.session_state.idx = 0
                
                st.success("Registro removido com sucesso!")
                st.rerun()
