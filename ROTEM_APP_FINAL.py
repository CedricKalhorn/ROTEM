import streamlit as st

# =======================
# Styling
# =======================
st.set_page_config(page_title="ROTEM-tool", layout="wide")
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
    font-size: 29px;
    color: #002B45;
    font-weight: 600;
}
.advies-overzicht {
  font-size: 35px;
  font-weight: 700;
  background-color: #e6f4f9;
  padding: 12px 16px;
  border-left: 6px solid #00B5E2;
  border-radius: 8px;
  margin-bottom: 16px;
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
def stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, weight_kg, keuze, keuze_fib, levensbedreigend):
    gewicht = weight_kg
    omniplasma = 0
    omniplasma_zak = 0
    trombocyten = 0
    fibrinogeen_g = 0
    fibrinogeen_ml = 0.0
    cofact_dosis = 0.0
    omniplasma_used = False

    if extem_ct is not None and fibtem_a5 is not None:
        if extem_ct > 80 and fibtem_a5 > 9:
            dosis = gewicht * 12.5
            if keuze == "Cofact":
                cofact_dosis = round(0.4 * gewicht, 1)
            elif keuze == "Omniplasma":
                if levensbedreigend == "Ja":
                    omniplasma = int((dosis + 199) // 200) * 200
                else: 
                    omniplasma = int(round(dosis / 200) * 200)
                omniplasma_zak = int(omniplasma / 200)
                omniplasma_used = True

    if extem_a5 is not None and fibtem_a5 is not None:
        if 30 <= extem_a5 <= 40 and fibtem_a5 > 9:
            trombocyten = 1
            if not omniplasma_used and keuze == "Omniplasma":
                dosis = gewicht * 12.5
                if levensbedreigend == "Ja":
                    omniplasma = int((dosis + 199) // 200) * 200
                else: 
                    omniplasma = int(round(dosis / 200) * 200)
                omniplasma_zak = int(omniplasma / 200)
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
        advies["Cofact"] = f"{cofact_dosis} ml" if cofact_dosis > 0 else "Geen toediening vereist"
    elif keuze == "Omniplasma":
        advies["Omniplasma"] = f"{omniplasma_zak} zakken ({omniplasma} ml)" if omniplasma_used else "Geen toediening vereist"
        
    advies["Trombocyten"] = f"{trombocyten} eenheid (330 ml)" if trombocyten > 0 else "Geen toediening vereist"

    if keuze_fib == "Fibrinogeen dosis":
        advies["Fibrinogeen dosis"]  = f"{fibrinogeen_g} g" if fibrinogeen_g > 0 else "Geen toediening vereist"
    elif keuze_fib == "Fibrinogeen concentraat":
        advies["Fibrinogeen concentraat"] = f"{fibrinogeen_ml} ml" if fibrinogeen_g > 0 else "Geen toediening vereist"

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

# =======================
# HEADER
# =======================
col_left, col_right = st.columns([6, 1])
with col_left:
    st.markdown("## ROTEM-Tool")
    
st.info("**⚠️ Disclaimer:** De arts blijft altijd eindverantwoordelijk voor het uiteindelijke behandelbeleid. Deze tool dient ter ondersteuning, niet als vervanging van klinisch oordeel.")

# =======================
# Pagina 0 – Live viewer openen
# =======================
if not st.session_state.liveviewer_opened:

    st.warning("Open de live viewer.")

    st.caption("Dubbel klik indien nodig om door te gaan naar invoerscherm.")
    if st.button("Klik om door te gaan ➡️"):
        st.session_state.liveviewer_opened = True

# =======================
# Pagina 1 – Invoer
# =======================

elif not st.session_state.show_advies:
        
    levensbedreigend = st.radio("Betreft het een patiënt met een levensbedreigende bloeding:", ["Ja", "Nee"], horizontal = True)
    product_keuze = st.radio("Maak een keuze:", ["Omniplasma", "Cofact"], horizontal=True)
    product_keuze_fib = st.radio("Maake een keuze:", ["Fibrinogeen dosis", "Fibrinogeen concentraat"], horizontal=True)

    st.markdown("Vul hieronder de patiëntgegevens in:")
    weight_kg = st.number_input("Gewicht (kg)", min_value=1.0, max_value=3000.0, value=None, step=0.1, format="%.1f")
    fibtem_a5 = st.number_input("FIBTEM A5 (mm)", min_value=0, max_value=500, value=None)
    extem_ct = st.number_input("EXTEM CT (seconden)", min_value=0, max_value=1000, value=None)
    extem_a5 = st.number_input("EXTEM A5 (mm)", min_value=0, max_value=1000, value=None)
    
    
    st.caption("Dubbel klik indien nodig om advies te genereren.")

    if st.button("Genereer advies ➡️"):
        waarschuwingen = []
        if weight_kg is None:
                waarschuwingen.append("- ❌ Gewicht is niet ingevuld! Vul een geschat of exact gewicht in.")
        if fibtem_a5 is None:
                waarschuwingen.append("- ❌ FIBTEM A5 is niet ingevuld! Vul de FIBTEM A5 in.")
        if extem_ct is None:
                waarschuwingen.append("- ❌ EXTEM CT is niet ingevuld! Vul de EXTEM CT in.")
        if extem_a5 is None:
                waarschuwingen.append("- ❌ EXTEM A5 is niet ingevuld! Vul de EXTEM A5 in.")

        if waarschuwingen:
                st.warning("\n".join(["⚠️ Waarschuwing:"] + waarschuwingen))
                st.stop()
        
            # Sla inputs tijdelijk op
        st.session_state.extem_ct = extem_ct
        st.session_state.fibtem_a5 = fibtem_a5
        st.session_state.extem_a5 = extem_a5
        st.session_state.weight_kg = weight_kg
        st.session_state.product_keuze = product_keuze
        st.session_state.product_keuze_fib = product_keuze_fib
        st.session_state.product_levensbedreigend = levensbedreigend
  
        st.session_state.advies_resultaat = stap_2_na_ROTEM_geleide_stollingscorrectie(
            extem_ct, fibtem_a5, extem_a5, weight_kg, product_keuze, product_keuze_fib, levensbedreigend
        )
        st.session_state.show_advies = True

# =======================
# Pagina 2 – Advies
# =======================
else:
    adviezen = st.session_state.advies_resultaat
    overzicht_items = [f"{prod}: {val}" for prod, val in adviezen.items()]
    
    # Grote, opvallende overzichtszin
    # Bulletpoint-stijl overzicht met grotere tekst
    bullet_items = "".join([f"<li>{prod}: {val}</li>" for prod, val in adviezen.items()])
    st.markdown(
        f"""
        <div class='advies-overzicht'>
            <span style="font-size: 22px;">Advies:</span>
            <ul style="margin-top: 12px; font-size: 20px; font-weight: 600; color: #002B45;">
                {bullet_items}
            </ul>
        </div>
        """, unsafe_allow_html=True
    )
    # 2) Toon per product de toelichting
    st.markdown("### Toelichting per bloedproduct")
    for product, waarde in adviezen.items():
        # Alleen uitleg als er daadwerkelijk iets toegediend wordt
        if waarde != "Geen toediening vereist" and waarde != "Niet nodig in de behandeling":
            st.markdown(f"**{product}**: {waarde}")
            # Nu je logica uit jouw bestaande snippets
            if product == "Omniplasma":
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>EXTEM CT > 80 sec (waarde: {st.session_state.extem_ct} sec)</li>
                  <li>FIBTEM A5 > 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.weight_kg} kg</li>
                  <li>Levensbedreigend: {st.session_state.product_levensbedreigend}</li>
                </ul>
                """, unsafe_allow_html=True)

            elif product == "Cofact":
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>EXTEM CT > 80 sec (waarde: {st.session_state.extem_ct} sec)</li>
                  <li>FIBTEM A5 > 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.weight_kg} kg</li>
                </ul>
                """, unsafe_allow_html=True)

            elif product == "Trombocyten":
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>EXTEM A5 tussen 30–40 mm (waarde: {st.session_state.extem_a5} mm)</li>
                  <li>FIBTEM A5 > 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.weight_kg} kg</li>
                </ul>
                """, unsafe_allow_html=True)

            elif product.startswith("Fibrinogeen"):
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>FIBTEM A5 < 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>EXTEM A5 < 35 mm (waarde: {st.session_state.extem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.weight_kg} kg</li>
                </ul>
                """, unsafe_allow_html=True)


    st.caption("Dubbel klik indien nodig om terug te gaan naar invoerscherm")
    if st.button("⬅️ Terug naar invoerscherm"):
        st.session_state.show_advies = False

# =======================
# Footer
# =======================
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Gemaakt door studenten Klinische Technologie: Anne de Zeeuw, Cedric Kalhorn, Fleur de Groot & Roos Ritsma</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Contactgegevens: m.a.dezeeuw@student.tudelft.nl, c.a.f.kalhorn@student.tudelft.nl, f.m.j.degroot@student.tudelft.nl & r.p.ritsma@student.tudelft.nl</p>", unsafe_allow_html=True)
