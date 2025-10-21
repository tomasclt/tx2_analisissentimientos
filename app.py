# -*- coding: utf-8 -*-
import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# ------------------------------
# Configuración de página
# ------------------------------
st.set_page_config(page_title="Análisis de Sentimiento", page_icon="🧠", layout="centered")

# ------------------------------
# Estilos (Dark theme alto contraste + fixes de legibilidad)
# ------------------------------
st.markdown("""
<style>
:root{
  --radius:16px;
  --bgA:#0b1120; --bgB:#0f172a;
  --panel:#111827; --panel-border:#1f2937;
  --text:#f8fafc; --muted:#cbd5e1;
  --input:#0f172a; --input-border:#334155;
  --primaryA:#2563eb; --primaryB:#1d4ed8; --focus:#22d3ee;
  --pos:#10b981; --neu:#60a5fa; --neg:#ef4444;
}

[data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg,var(--bgA) 0%,var(--bgB) 100%) !important;
  color: var(--text) !important;
}
html, body{
  color:var(--text) !important;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}
main .block-container{max-width:900px; padding-top:2rem; padding-bottom:3rem;}
h1,h2,h3{letter-spacing:-.01em; color:#f9fafb !important;}

/* Nada “apagadito” nunca */
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] *,
section[data-testid="stSidebar"] * {
  color: var(--text) !important;
  opacity: 1 !important;
}

/* Evitar code-tags claros (ej. los ceros se veían en caja blanca) */
code, kbd, samp {
  background: #0f172a !important;
  color: var(--text) !important;
  border: 1px solid #334155 !important;
  border-radius: 6px;
  padding: .05rem .3rem;
}

/* Tarjetas */
.card{background:var(--panel); border:1px solid var(--panel-border); border-radius:var(--radius);
      box-shadow:0 18px 50px rgba(0,0,0,.45); padding:18px 20px;}

/* Inputs */
.stTextArea textarea, .stTextInput input{
  background:var(--input) !important; border:1px solid var(--input-border) !important;
  color:var(--text) !important; border-radius:12px !important; transition: all 0.25s ease;
}
.stTextArea textarea:hover, .stTextInput input:hover { background:#1a2234 !important; border-color:#3b82f6 !important; }
.stTextArea textarea:focus, .stTextInput input:focus {
  background:#0d1829 !important; color:#f8fafc !important;
  border-color:var(--focus) !important; outline:none !important;
  box-shadow:0 0 0 2px rgba(34,211,238,.25);
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder{ color:#94a3b8 !important; }

/* Radio/checkbox visibles */
input[type="radio"], input[type="checkbox"]{ accent-color: var(--primaryA) !important; }

/* Botones */
.stButton > button, .stDownloadButton > button{
  border-radius:999px; padding:.72rem 1.15rem; border:1px solid var(--panel-border);
  background:linear-gradient(90deg,var(--primaryA),var(--primaryB)) !important;
  color:#fff !important; box-shadow:0 14px 36px rgba(37,99,235,.35);
  transition:transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover{transform:translateY(-1px); box-shadow:0 18px 48px rgba(37,99,235,.45);}

/* Sidebar */
section[data-testid="stSidebar"] > div:first-child{background:#0c1324; border-right:1px solid var(--panel-border);}

/* Chips de estado */
.badge{display:inline-block; padding:.25rem .6rem; border-radius:999px; font-weight:600; font-size:.8rem;}
.badge-pos{background:rgba(16,185,129,.15); color:#86efac; border:1px solid rgba(16,185,129,.35);}
.badge-neu{background:rgba(96,165,250,.12); color:#93c5fd; border:1px solid rgba(96,165,250,.35);}
.badge-neg{background:rgba(239,68,68,.14); color:#fca5a5; border:1px solid rgba(239,68,68,.35);}

/* Barras */
.bar{height:10px; width:100%; background:#0f172a; border:1px solid #334155; border-radius:999px; overflow:hidden;}
.bar > div{height:100%;}

/* key-value para números */
.kv{ display:flex; align-items:center; gap:.75rem; margin:.35rem 0; }
.kv .k{ color:var(--text); font-weight:600; }
.kv .v{
  background:#0f172a; border:1px solid #334155; color:#f8fafc;
  padding:.25rem .6rem; border-radius:10px; font-variant-numeric: tabular-nums;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# App (misma lógica, SIN expanders)
# ------------------------------
translator = Translator()
st.title('🧠 Uso de TextBlob')

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

# Sidebar (texto sin backticks para que no genere cajas)
with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.markdown(
        "**Polaridad**: valor entre **-1** (muy negativo) y **1** (muy positivo). "
        "Cero representa sentimiento **neutral**.\n\n"
        "**Subjetividad**: valor entre **0** (objetivo) y **1** (muy subjetivo)."
    )

# ===== Sección 1: Análisis visible siempre =====
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader('Analizar Polaridad y Subjetividad en un texto')
text1 = st.text_area('Escribe por favor:')
if text1:
    # Traducción ES → EN
    translation = translator.translate(text1, src="es", dest="en")
    trans_text = translation.text

    blob = TextBlob(trans_text)
    pol = round(blob.sentiment.polarity, 2)
    sub = round(blob.sentiment.subjectivity, 2)

    # Valores legibles
    st.markdown(f'<div class="kv"><div class="k">Polarity:</div><div class="v">{pol}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="kv"><div class="k">Subjectivity:</div><div class="v">{sub}</div></div>', unsafe_allow_html=True)

    # Chip de estado
    if pol >= 0.5:
        st.markdown('<span class="badge badge-pos">Sentimiento Positivo 😊</span>', unsafe_allow_html=True)
    elif pol <= -0.5:
        st.markdown('<span class="badge badge-neg">Sentimiento Negativo 😔</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-neu">Sentimiento Neutral 😐</span>', unsafe_allow_html=True)

    # Barras visuales
    st.markdown("###### Intensidad de Polaridad")
    pol_pct = int((pol + 1) * 50)
    pol_color = "var(--pos)" if pol > 0.05 else ("var(--neg)" if pol < -0.05 else "var(--neu)")
    st.markdown(f'''<div class="bar"><div style="width:{pol_pct}%; background:{pol_color};"></div></div>''', unsafe_allow_html=True)
    st.caption(f"Escala centrada en 0 (neutral). Valor actual: {pol}")

    st.markdown("###### Subjetividad")
    sub_pct = int(sub * 100)
    st.markdown(f'''<div class="bar"><div style="width:{sub_pct}%; background:var(--primaryA);"></div></div>''', unsafe_allow_html=True)
    st.caption(f"0 = objetivo • 1 = muy subjetivo. Valor actual: {sub}")

    # Texto traducido (siempre visible pero en code oscuro, sin hover necesario)
    st.markdown("**Texto analizado (EN):**")
    st.code(trans_text, language="text")
st.markdown('</div>', unsafe_allow_html=True)

# ===== Sección 2: Corrección en inglés (visible siempre) =====
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader('Corrección en inglés')
text2 = st.text_area('Escribe por favor:', key='4')
if text2:
    blob2 = TextBlob(text2)
    st.write(blob2.correct())
st.markdown('</div>', unsafe_allow_html=True)
