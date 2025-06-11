import streamlit as st

# =======================
# Styling
# =======================
st.set_page_config(page_title="ROTEM Advies Tool", layout="wide")
st.markdown("""
<style>
body, .main, [data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    color: #002B45 !important;
}
html, body, [data-testid="stMarkdownContainer"] {
    color: #002B45 !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #002B45 !important;
}
input[type="number"],
input[type="text"],
textarea {
    background-color: #ffffff !important;
    color: #002B45 !important;
}
[data-testid="stNumberInput"] {
    background-color: #e6f4f9;
    border-left: 5px solid #00B5E2;
    padding: 8px 12px;
    border-radius: 10px;
    margin-bottom: 12px;
}
[data-testid="stNumberInput"] input {
    font-size: 16px;
    font-weight: 600;
    color: #002B45;
}
[data-testid="stRadio"] > div > label > div:first-child {
    background-color: #00B5E2 !important;
    border: 2px solid #00B5E2 !important;
}
[data-testid="stRadio"] > div > label[data-selected="true"] > div:first-child {
    background-color: #00B5E2 !important;
    border-color: #00B5E2 !important;
}
label {
    color: #002B45 !important;
    font-weight: bold;
}
.stButton > button {
    background-color: #e6f4f9;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
}
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
[data-testid="stAlert"] {
    background-color: #e6f4f9 !important;
    color: #002B45 !important;
    border: 1px solid #00B5E2;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =======================
# ROTEM functie
# =======================
def stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, weight_kg, keuze):
    gewicht = weight_kg
    omniplasma_min = 0
    omniplasma_max = 0
    trombocyten = 0
    fibrinogeen_g = 0
    fibrinogeen_ml = 0.0
    cofact_dosis = 0.0
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

 # Fibrinogeen-berekening
    if fibtem_a5 is not None and extem_a5 is not None and fibtem_a5 < 9 and extem_a5 < 35:
        delta = 12 - fibtem_a5
        # gram
        fibrinogeen_g = round((6.25 * delta * gewicht) / 1000)
        # ml
        fibrinogeen_ml = round(delta * (3.8 / 12) * gewicht)

    advies = {}
    if keuze == "Cofact":
        advies["Cofact"] = f"{cofact_dosis} ml" if cofact_dosis > 0 else "Niet nodig in de behandeling"
    elif keuze == "Omniplasma":
        advies["Omniplasma"] = f"{omniplasma_min}–{omniplasma_max} ml" if omniplasma_used else "Niet nodig in de behandeling"
    advies["Trombocyten"] = f"{trombocyten} eenheid" if trombocyten > 0 else "Niet nodig in de behandeling"
    # Toon nu beide doseringen
    if fibrinogeen_g > 0:
        advies["Fibrinogeen dosis"]  = f"{fibrinogeen_g} g"
        advies["Fibrinogeen concentraat"] = f"{fibrinogeen_ml} ml"
    else:
        advies["Fibrinogeen dosis"]  = "Niet nodig"
        advies["Fibrinogeen concentraat"] = "Niet nodig"

    return advies

# =======================
# State management
# =======================
if "show_advies" not in st.session_state:
    st.session_state.show_advies = False
if "advies_resultaat" not in st.session_state:
    st.session_state.advies_resultaat = {}
if "liveviewer_opened" not in st.session_state:
    st.session_state.liveviewer_opened = False

# =======================
# Disclaimer
# =======================
st.markdown("### ⚠️ Disclaimer")
st.info("De arts blijft altijd eindverantwoordelijk voor het uiteindelijke behandelbeleid. Deze tool dient ter ondersteuning, niet als vervanging van klinisch oordeel.")

# =======================
# HEADER
# =======================
col_left, col_right = st.columns([6, 1])
with col_left:
    st.markdown("## ROTEM Advies Tool")

# =======================
# Pagina 0 – Live viewer openen
# =======================
if not st.session_state.liveviewer_opened:
    st.markdown("## Open de Live Viewer")
    st.warning("⚠️ Open eerst de Live Viewer zodat je toegang hebt tot de ROTEM-waarden.")

    st.caption("Dubbel klik indien nodig om door te gaan naar invoerscherm.")
    if st.button("Live viewer is geopend, ga verder naar invoerscherm ➡️"):
        st.session_state.liveviewer_opened = True

# =======================
# Pagina 1 – Invoer
# =======================
elif not st.session_state.show_advies:
    st.markdown("Geef hieronder het gewicht van de patiënt en de ROTEM-waarden:")
    col1, col2 = st.columns(2)
    with col1:
        weight_kg = st.number_input("Gewicht (kg)", min_value=1.0, max_value=3000.0, value=None, step=0.1, format="%.1f")
        extem_ct = st.number_input("EXTEM CT (seconden)", min_value=0, max_value=1000, value=None)
    with col2:
        fibtem_a5 = st.number_input("FIBTEM A5 (mm)", min_value=0, max_value=500, value=None)
        extem_a5 = st.number_input("EXTEM A5 (mm)", min_value=0, max_value=1000, value=None)

    product_keuze = st.radio("Geef hieronder welk bloedproduct uw voorkeur heeft:", ["Omniplasma", "Cofact"], horizontal=True)

    st.caption("Dubbel klik indien nodig om advies te genereren.")

    if st.button("Genereer advies ➡️"):
        if weight_kg is None:
            st.error("❌ Gewicht is verplicht. Vul een geschat of exact gewicht in.")
        if fibtem_a5 is None:
            st.error("❌ FIBTEM A5 is verplicht om het protocol te doorlopen. Vul een waarde in als deze bekend is. Zo niet, vraag ROTEM opnieuw aan! ")
        else:
            waarschuwingen = []
            if extem_ct is None:
                waarschuwingen.append("- EXTEM CT is niet ingevuld. Als hij niet bekend is klik dan door.")
            if extem_a5 is None:
                waarschuwingen.append("- EXTEM A5 is niet ingevuld. Als hij niet bekend is klik dan door.")
            if waarschuwingen:
                st.warning("\n".join(["⚠️ Waarschuwing:"] + waarschuwingen))
                st.stop()
            # Sla inputs tijdelijk op
            st.session_state.extem_ct = extem_ct
            st.session_state.fibtem_a5 = fibtem_a5
            st.session_state.extem_a5 = extem_a5
            st.session_state.weight_kg = weight_kg
            st.session_state.product_keuze = product_keuze

            st.session_state.advies_resultaat = stap_2_na_ROTEM_geleide_stollingscorrectie(
                extem_ct, fibtem_a5, extem_a5, weight_kg, product_keuze
            )
            st.session_state.show_advies = True

# =======================
# Pagina 2 – Advies
# =======================
else:
    st.success("✅ Advies succesvol gegenereerd op basis van ingevoerde gegevens.")
    for product, waarde in st.session_state.advies_resultaat.items():
        st.markdown(f"### {product}")
        st.markdown(f"<div class='advies-box'>{waarde}</div>", unsafe_allow_html=True)

        # Toelichting per bloedproduct
        if product == "Omniplasma" and "ml" in waarde:
            st.markdown(f"""
            <span style='font-size: 0.85em; color: gray;'>ℹ️ Gebaseerd op:</span>
            <ul style='font-size: 0.85em; color: gray; margin-top: 0px;'>
                <li>EXTEM CT &gt; 80 sec (gegeven waarde: {st.session_state.extem_ct} sec)</li>
                <li>FIBTEM A5 &gt; 9 mm (gegeven waarde: {st.session_state.fibtem_a5} mm)</li>
                <li>Gewicht: {st.session_state.weight_kg} kg</li>
            </ul>
            """, unsafe_allow_html=True)

        elif product == "Cofact" and "ml" in waarde:
            st.markdown(f"""
            <span style='font-size: 0.85em; color: gray;'>ℹ️ Gebaseerd op:</span>
            <ul style='font-size: 0.85em; color: gray; margin-top: 0px;'>
                <li>EXTEM CT &gt; 80 sec (gegeven waarde: {st.session_state.extem_ct} sec)</li>
                <li>FIBTEM A5 &gt; 9 mm (gegeven waarde: {st.session_state.fibtem_a5} mm)</li>
                <li>Gewicht: {st.session_state.weight_kg} kg</li>
            </ul>
            """, unsafe_allow_html=True)  
            
        elif product == "Trombocyten" and "1 eenheid" in waarde:
            st.markdown(f"""
            <span style='font-size: 0.85em; color: gray;'>ℹ️ Gebaseerd op:</span>
            <ul style='font-size: 0.85em; color: gray; margin-top: 0px;'>
                <li>EXTEM A5 tussen 30–44 mm of &lt; 30 mm (gegeven waarde: {st.session_state.extem_a5} mm)</li>
                <li>FIBTEM A5 &gt; 9 mm (gegeven waarde: {st.session_state.fibtem_a5} mm)</li>
                <li>Gewicht: {st.session_state.weight_kg} kg</li>
            </ul>
            """, unsafe_allow_html=True)
        elif product.startswith("Fibrinogeen") and waarde != "Niet nodig":

        st.caption("Dubbel klik indien nodig om terug te gaan naar invoerscherm")
    if st.button("⬅️ Terug naar invoerscherm"):
        st.session_state.show_advies = False

# =======================
# Footer
# =======================
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Gemaakt door studenten Klinische Technologie: Anne de Zeeuw, Cedric Kalhorn, Fleur de Groot & Roos Ritsma</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Contactgegevens: m.a.dezeeuw@student.tudelft.nl, c.a.f.kalhorn@student.tudelft.nl, f.m.j.degroot@student.tudelft.nl & r.p.ritsma@student.tudelft.nl</p>", unsafe_allow_html=True)
