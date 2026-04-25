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

# 2. CSS: DESIGN TÁTICO DE ALTA PRECISÃO
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none !important;}
    .stApp { 
        margin-top: -95px !important; 
        background-color: #0d0d0d !important; 
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px); 
        background-size: 30px 30px; 
    }
    .main .block-container { padding: 1rem !important; max-width: 1400px !important; }
    
    /* HEADER COMPACTO */
    .custom-header { 
        background: linear-gradient(180deg, #151515 0%, #0d0d0d 100%); 
        border: 1px solid #222; border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 15px; 
    }
    .custom-header h1 { font-size: 12px; color: #D4AF37; text-transform: uppercase; letter-spacing: 6px; font-weight: 300; margin: 0; }

    /* PAINEL HUD */
    [data-testid="column"]:nth-of-type(2) { 
        background: #111111 !important; 
        padding: 20px !important; 
        border-radius: 12px !important; 
        border: 1px solid #1a1a1a !important; 
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important; 
    }
    
    /* TABULEIRO: AUMENTADO PARA 65VH */
    .board-container img {
        max-width: 90% !important;
        max-height: 65vh !important; 
        border-radius: 4px;
        border: 1px solid #222;
        box-shadow: 0 25px 70px rgba(0,0,0,1);
    }

    .label-tech { font-size: 9px; color: #444; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; font-weight: 600; }
    
    .data-display-box { 
        background: rgba(255, 255, 255, 0.02); 
        padding: 12px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #1a1a1a; 
    }
    .my-line-text { color: #D4AF37; font-size: 18px; font-weight: 800; text-transform: uppercase; margin: 0; }
    .opp-line-text { color: #eee; font-size: 14px; font-weight: 600; text-transform: uppercase; margin: 0; }
    
    .total-display { color: #333; font-size: 24px; font-weight: 900; margin-top: 5px; }
    .stNumberInput input { color: #D4AF37 !important; font-size: 32px !important; font-weight: 900 !important; }

    .status-badge { padding: 5px 12px; border-radius: 4px; font-size: 10px; font-weight: bold; text-transform: uppercase; margin-bottom: 12px; }
    .status-studied { background-color: rgba(0, 255, 100, 0.05); color: #00FF64; border: 1px solid #00FF64; }
    .status-awaiting { background-color: rgba(255, 50, 50, 0.05); color: #FF3232; border: 1px solid #FF3232; }

    .stButton > button { height: 40px !important; font-size: 11px !important; border-radius: 20px !important; }
    
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE ARQUIVOS
IMG_DIR = "jogadas"
if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
imgs = [f for f in sorted(os.listdir(IMG_DIR)) if f.endswith(".jpg")]

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'studied_list' not in st.session_state: st.session_state.studied_list = {}

st.markdown('<div class="custom-header"><h1>Chess Strategy Lab // Estudo de Aberturas</h1></div>', unsafe_allow_html=True)
col_left, col_right = st.columns([1.5, 1], gap="large")

if imgs:
    st.session_state.idx = max(0, min(st.session_state.idx, len(imgs) - 1))
    curr = imgs[st.session_state.idx]
    path_jpg = os.path.join(IMG_DIR, curr)
    path_txt = os.path.join(IMG_DIR, curr.replace(".jpg", ".txt"))
    path_op = os.path.join(IMG_DIR, curr.replace(".jpg", "_op.txt"))

    # ESQUERDA: Tabuleiro com Altura Otimizada
    with col_left:
        img_64 = get_image_base64(path_jpg)
        st.markdown(f'''
            <div class="board-container" style="display:flex; justify-content:center; align-items:center; height:70vh;">
                <img src="data:image/jpeg;base64,{img_64}">
            </div>
        ''', unsafe_allow_html=True)

    # DIREITA: Painel HUD
    with col_right:
        st.markdown('<p class="label-tech">Navegação</p>', unsafe_allow_html=True)
        c_in, c_tot = st.columns([0.4, 1])
        with c_in:
            # Key dinâmica para garantir sincronia do número ao mudar
            v_input = st.number_input("Pos", min_value=1, max_value=len(imgs), value=st.session_state.idx + 1, key=f"nav_{st.session_state.idx}", label_visibility="collapsed")
            if v_input != st.session_state.idx + 1:
                st.session_state.idx = v_input - 1
                st.rerun()
        with c_tot: st.markdown(f'<div class="total-display">/ {len(imgs)}</div>', unsafe_allow_html=True)

        is_studied = st.session_state.studied_list.get(curr, False)
        st.markdown(f'<div class="status-badge {"status-studied" if is_studied else "status-awaiting"}">{"✓ Estudo Concluído" if is_studied else "⚠ Aguardando Estudo"}</div>', unsafe_allow_html=True)

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

# 4. GESTÃO DE BASE
st.write("")
with st.expander("⚙️ BASE DE DADOS (CADASTRAR / EDITAR / EXCLUIR)"):
    t1, t2, t3 = st.tabs(["NOVO", "EDITAR", "EXCLUIR"])
    
    with t1:
        new_my = st.text_input("Sua Abertura:")
        new_adv = st.text_input("Variante Adversário:")
        u_f = st.file_uploader("Screenshot:", type=["jpg", "png"], key="up_new")
        u_t = st.text_area("Análise Técnica:")
        if st.button("SALVAR REGISTRO"):
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
            e_my = st.text_input("Minha Abertura:", value=my_opening, key="e_my_")
            e_adv = st.text_input("Variante Adversário:", value=curr.split("_")[0].replace("-", " "), key="e_adv_")
            e_img = st.file_uploader("Trocar Foto:", type=["jpg", "png"], key="e_img_")
            c_an = ""
            if os.path.exists(path_txt):
                with open(path_txt, "r") as f: c_an = f.read()
            e_an = st.text_area("Análise:", value=c_an, key="e_an_")
            if st.button("ATUALIZAR DADOS"):
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
            st.error("AÇÃO PERMANENTE")
            if st.button("CONFIRMAR EXCLUSÃO"):
                if os.path.exists(path_jpg): os.remove(path_jpg)
                if os.path.exists(path_txt): os.remove(path_txt)
                if os.path.exists(path_op): os.remove(path_op)
                st.session_state.idx = 0
                st.rerun()
