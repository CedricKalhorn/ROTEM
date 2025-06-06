import streamlit as st

# =======================
# Styling
# =======================
st.set_page_config(page_title="ROTEM Advies Tool", layout="wide")
st.markdown("""
<style>
    .stButton>button {
        background-color: #004494;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .advies-box {
        background-color: #e6f4f9;
        border-left: 6px solid #00B5E2;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 16px;
    }
    .hmc-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# =======================
# ROTEM Functie
# =======================
def stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, weight_kg):
    gewicht = weight_kg if weight_kg else 70
    omniplasma = 0
    trombocyten = 0
    fibrinogeen = 0

    if extem_ct > 80 and fibtem_a5 > 9:
        dosis = gewicht * 10
        omniplasma = ((dosis + 199) // 200) * 200

    if 30 <= extem_a5 <= 40 and fibtem_a5 > 9:
        trombocyten = 330
        if omniplasma == 0:
            dosis = gewicht * 10
            omniplasma = ((dosis + 199) // 200) * 200

    if fibtem_a5 < 9 and extem_a5 < 35:
        fibrinogeen = round((6.25 * (12 - fibtem_a5) * gewicht) / 1000)

    return {
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
with col_right:
    st.image("38b9a13a-6e25-41f5-8a45-59eb064662a4.png", width=80)

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
