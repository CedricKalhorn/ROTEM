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

/* STANDAARD INPUTVELDEN */
input[type="number"],
input[type="text"],
textarea {
    background-color: #ffffff !important;
    color: #002B45 !important;
}

/* AANPASSING VOOR STREAMLIT INPUT CONTAINERS */
[data-testid="stNumberInput"] {
    background-color: #e6f4f9;
    border-left: 5px solid #00B5E2;
    padding: 8px 12px;
    border-radius: 10px;
    margin-bottom: 12px;
}

/* Inputtekst groter maken */
[data-testid="stNumberInput"] input {
    font-size: 16px;
    font-weight: 600;
    color: #002B45;
}
/* RADIOBUTTONS AANGEPAST NAAR HMC STIJL */
[data-testid="stRadio"] > div > label > div:first-child {
    background-color: #00B5E2 !important;
    border: 2px solid #00B5E2 !important;
}
[data-testid="stRadio"] > div > label[data-selected="true"] > div:first-child {
    background-color: #00B5E2 !important;
    border-color: #00B5E2 !important;
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
def stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, weight_kg, keuze):
    gewicht = weight_kg
    omniplasma_min = 0
    omniplasma_max = 0
    trombocyten = 0
    fibrinogeen = 0
    cofact_dosis = 0.0
    omniplasma_tekst = "Niet nodig in de behandeling"

    # flags voor gebruik
    omniplasma_used = False

    if extem_ct is not None and fibtem_a5 is not None:
        if extem_ct > 80 and fibtem_a5 > 9:
            dosis_min = gewicht * 10
            dosis_max = gewicht * 15
            if keuze == "Cofact":
                cofact_dosis = round(0.4 * gewicht, 1)
            elif keuze == "Omniplasma":
                omniplasma_min = ((dosis_min + 199) // 200) * 200
                omniplasma_max = ((dosis_max + 199) // 200) * 200
                omniplasma_used = True

    if extem_a5 is not None and fibtem_a5 is not None:
        if 30 <= extem_a5 <= 40 and fibtem_a5 > 9:
            trombocyten = 1
            if not omniplasma_used and keuze == "Omniplasma":
                dosis_min = gewicht * 10
                dosis_max = gewicht * 15
                omniplasma_min = ((dosis_min + 199) // 200) * 200
                omniplasma_max = ((dosis_max + 199) // 200) * 200
                omniplasma_used = True

    if fibtem_a5 is not None and extem_a5 is not None:
        if fibtem_a5 < 9 and extem_a5 < 35:
            fibrinogeen = round((6.25 * (12 - fibtem_a5) * gewicht) / 1000)

    advies = {}

    if keuze == "Cofact":
        advies["Cofact"] = f"{cofact_dosis} ml" if cofact_dosis > 0 else "Niet nodig in de behandeling"
    elif keuze == "Omniplasma":
        if omniplasma_used:
            advies["Omniplasma"] = f"{omniplasma_min}–{omniplasma_max} ml"
        else:
            advies["Omniplasma"] = "Niet nodig in de behandeling"

    advies["Trombocyten"] = f"{trombocyten} eenheid" if trombocyten > 0 else "Niet nodig in de behandeling"
    advies["Fibrinogeen"] = f"{fibrinogeen} gram" if fibrinogeen > 0 else "Niet nodig in de behandeling"

    return advies

# =======================
# State management
# =======================
if "show_advies" not in st.session_state:
    st.session_state.show_advies = False
if "advies_resultaat" not in st.session_state:
    st.session_state.advies_resultaat = {}

# =======================
# Disclaimer
# =======================
st.markdown("### ⚠️ Disclaimer")
st.info(
    "Deze tool geeft een **ondersteunend advies** op basis van ROTEM-waarden. "
    "De arts blijft te allen tijde verantwoordelijk voor het uiteindelijke behandelbeleid. "
    "Controleer altijd de onderliggende invoerwaarden en protocollen. "
    "Tool-versie: **v1.2.0**, gegenereerd op " + datetime.now().strftime("%d-%m-%Y %H:%M")
)
# =======================
# HEADER met HMC-logo
# =======================
col_left, col_right = st.columns([6, 1])
with col_left:
    st.markdown("## ROTEM Advies Tool")

# =======================
# PAGINA 1 – Invoer
# =======================
if not st.session_state.show_advies:

    st.markdown("Geef hieronder het gewicht van de patiënt en de ROTEM-waarden:")

    col1, col2 = st.columns(2)
    with col1:
        weight_kg = st.number_input("Gewicht (kg)", min_value=1.0, max_value=3000.0, value=None, step=0.1, format="%.1f")
        extem_ct = st.number_input("EXTEM CT (seconden)", min_value=0, max_value=1000, value=None)

    with col2:
        fibtem_a5 = st.number_input("FIBTEM A5 (mm)", min_value=0, max_value=500, value=None)
        extem_a5 = st.number_input("EXTEM A5 (mm)", min_value=0, max_value=1000, value=None)

    product_keuze = st.radio(
        "Geef hieronder welk bloedproduct uw voorkeur heeft:",
        ["Omniplasma", "Cofact"],
        horizontal=True
    )
    if extem_ct is not None and not (0 < extem_ct < 200):
        st.warning("⚠️ EXTEM CT lijkt buiten normaal bereik te liggen (0–200 s).")

    
    st.caption("Dubbel klik indien nodig om advies te genereren.")

if st.button("Genereer advies ➡️"):
    if weight_kg is None:
        st.error("❌ Gewicht is verplicht. Vul een geschat of exact gewicht in.")
    else:
        waarschuwingen = []
        if extem_ct is None:
            waarschuwingen.append("- EXTEM CT is niet ingevuld. Was deze waarde wel bekend, vul hem dan nog in. Zo niet, klik nogmaals op genereer advies.")
        if fibtem_a5 is None:
            waarschuwingen.append("- FIBTEM A5 is niet ingevuld. Was deze waarde wel bekend, vul hem dan nog in. Zo niet, klik nogmaals op genereer advies.")
        if extem_a5 is None:
            waarschuwingen.append("- EXTEM A5 is niet ingevuld. Was deze waarde wel bekend, vul hem dan nog in. Zo niet, klik nogmaals op genereer advies.")

        if waarschuwingen:
            st.warning("\n".join(["⚠️ Waarschuwing:"] + waarschuwingen))

        try:
            advies = stap_2_na_ROTEM_geleide_stollingscorrectie(
                extem_ct, fibtem_a5, extem_a5, weight_kg, product_keuze
            )
            st.session_state.advies_resultaat = advies
            st.session_state.show_advies = True
        except Exception as e:
            st.error("❌ Er is een onverwachte fout opgetreden bij de berekening. "
                     "Controleer je invoer of neem contact op met de ICT-afdeling.")
            st.exception(e)


# =======================
# PAGINA 2 – Advies
# =======================
else:
    st.success("✅ Advies succesvol gegenereerd op basis van ingevoerde gegevens.")
    input_info = (
        f"- Gewicht: **{weight_kg} kg**\n"
        f"- EXTEM CT: **{extem_ct} s**\n"
        f"- FIBTEM A5: **{fibtem_a5} mm**\n"
        f"- EXTEM A5: **{extem_a5} mm**\n"
        f"- Gekozen product: **{product_keuze}**"
    )
    st.markdown("#### Gebruikte invoerwaarden:")
    st.markdown(input_info)

    for product, waarde in st.session_state.advies_resultaat.items():
        st.markdown(f"### {product}")
        st.markdown(f"<div class='advies-box'>{waarde}</div>", unsafe_allow_html=True)

    st.caption("Dubbel klik indien nodig om terug te gaan naar invoerscherm")
    if st.button("⬅️ Terug naar invoerscherm"):
        st.session_state.show_advies = False

# =======================
# Footer
# =======================
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Gemaakt door studenten Klinische Technologie: Cedric Kalhorn, Fleur de Groot, Anne de Zeeuw & Roos Ritsma</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Contactgegevens: c.a.f.kalhorn@student.tudelft.nl, f.m.j.degroot@student.tudelft.nl, m.a.dezeeuw@student.tudelft.nl, r.p.ritsma@student.tudelft.nl </p>", unsafe_allow_html=True)
