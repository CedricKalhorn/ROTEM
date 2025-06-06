import streamlit as st

# =======================
# Styling
# =======================
st.set_page_config(page_title="ROTEM Advies Tool", layout="wide")
st.markdown("""
<style>
/* VOLLEDIGE PAGINAACHTERGROND */
body, .main, [data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    color: #002B45 !important;
}

/* ALGEMENE TEKSTKLEUR */
html, body, [data-testid="stMarkdownContainer"] {
    color: #002B45 !important;
}

/* KOPPEN */
h1, h2, h3, h4, h5, h6 {
    color: #002B45 !important;
}

/* INVOERVELDEN */
input[type="number"],
input[type="text"],
textarea {
    background-color: #004494 !important;
    color: white !important;
    border-radius: 6px;
    border: 1px solid #002B45;
    padding: 10px;
}

/* LABELS BOVEN VELDEN */
label {
    color: #002B45 !important;
    font-weight: bold;
}

/* BUTTONS */
.stButton > button {
    background-color: #e6f4f9;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
}

/* ADVIESBLOKKEN */
.advies-box {
    background-color: #e6f4f9;
    border-left: 6px solid #00B5E2;
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    font-size: 16px;
    color: #002B45;
    font-weight: 600;
}

/* INFO/DISCLAIMER BLOCKS */
[data-testid="stAlert"] {
    background-color: #e6f4f9 !important;
    color: #002B45 !important;
    border: 1px solid #00B5E2;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)



# =======================
# ROTEM Functie
# =======================
def stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, weight_kg):
    gewicht = weight_kg
    omniplasma = 0
    trombocyten = 0
    fibrinogeen = 0
    cofact_dosis = 0.0


    
    if extem_ct > 80 and fibtem_a5 > 9:
        dosis = gewicht * 10
        cofact_dosis = round(0.4 * weight_kg, 1)
        omniplasma = ((dosis + 199) // 200) * 200

    if 30 <= extem_a5 <= 40 and fibtem_a5 > 9:
        trombocyten = 330
        if omniplasma == 0:
            dosis = gewicht * 10
            omniplasma = ((dosis + 199) // 200) * 200

    if fibtem_a5 < 9 and extem_a5 < 35:
        fibrinogeen = round((6.25 * (12 - fibtem_a5) * gewicht) / 1000)

    return {
        "Cofact": f"{cofact_dosis} ml?" if cofact_dosis > 0 else "Geen",
        "Omniplasma": f"{omniplasma} ml" if omniplasma > 0 else "Geen",
        "Trombocyten": f"{trombocyten} eenheden" if trombocyten > 0 else "Geen",
        "Fibrinogeen": f"{fibrinogeen} gram" if fibrinogeen > 0 else "Geen"
    }


# =======================
# State management
# =======================
if "show_advies" not in st.session_state:
    st.session_state.show_advies = False
if "advies_resultaat" not in st.session_state:
    st.session_state.advies_resultaat = {}

# =======================
# HEADER met HMC-logo
# =======================
col_left, col_right = st.columns([6, 1])
with col_left:
    st.markdown("## ROTEM Advies Tool")

# =======================
# Disclaimer
# =======================
st.markdown("### ⚠️ Disclaimer")
st.info("De arts blijft altijd eindverantwoordelijk voor het uiteindelijke behandelbeleid. Deze tool dient ter ondersteuning, niet als vervanging van klinisch oordeel.")

# =======================
# PAGINA 1 – Invoer
# =======================
if not st.session_state.show_advies:
    st.markdown("Geef hieronder de ROTEM-waarden in. Invoer is optioneel – defaults worden gebruikt bij lege velden.")

    col1, col2 = st.columns(2)
    with col1:
        weight_kg = st.number_input("Gewicht (kg)", min_value=0, max_value=300, value=0)
        fibtem_a5 = st.number_input("FIBTEM A5 (mm)", min_value=0, max_value=50, value=0)
    with col2:
        extem_ct = st.number_input("EXTEM CT (seconden)", min_value=0, max_value=1000, value=0)
        extem_a5 = st.number_input("EXTEM A5 (mm)", min_value=0, max_value=100, value=0)

    if st.button("Genereer advies"):
        st.session_state.advies_resultaat = stap_2_na_ROTEM_geleide_stollingscorrectie(
            extem_ct, fibtem_a5, extem_a5, weight_kg
        )
        st.session_state.show_advies = True
        st.stop()

# =======================
# PAGINA 2 – Advies
# =======================
else:
    st.success("✅ Advies succesvol gegenereerd op basis van ingevoerde gegevens.")

    for product, waarde in st.session_state.advies_resultaat.items():
        st.markdown(f"### {product}")
        st.markdown(f"<div class='advies-box'>{waarde}</div>", unsafe_allow_html=True)

    if st.button("⬅️ Terug naar invoer"):
        st.session_state.show_advies = False
        st.stop()

# =======================
# Footer
# =======================
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Makers: Cedric Kalhorn, Fleur de Groot, Anne de Zeeuw & Roos Ritsma</p>", unsafe_allow_html=True)
