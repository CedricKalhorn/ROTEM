import streamlit as st
import math
# =======================
# Stijl
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
# ROTEM-functie
# =======================

def stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, gewicht_kg, keuze, keuze_fib, levensbedreigend):
    gewicht = gewicht_kg
    omniplasma = 0
    omniplasma_zak = 0
    trombocyten = 0
    fibrinogeen_g = 0
    fibrinogeen_ml = 0.0
    cofact_dosis = 0.0
    omniplasma_gebruikt = False
    
    IE_per_flesje = 500     
    flesje_ml = 20     
    IE_per_ml = IE_per_flesje/ flesje_ml  
    mg_per_ml = 10     

    cofact_ml = 0.0
    cofact_ie = 0
    cofact_mg = 0.0
    cofact_flesjes = 0
    
    if extem_ct is not None and fibtem_a5 is not None:
        if extem_ct > 80 and fibtem_a5 > 9:
            dosis = gewicht * 12.5
            if keuze == "Cofact":
                cofact_ml = round(0.4 * gewicht, 1)
                cofact_ie = int(round(cofact_ml * IE_per_ml))
                cofact_mg  = round(cofact_ml * mg_per_ml, 1)
                if levensbedreigend == "Ja":
                    cofact_flesjes = math.ceil((cofact_ie / IE_per_flesje))
                    # Bepaal het aantal flesjes van 20 ml en 10 ml
                    cofact_flesjes_20ml = int(cofact_ml // 20)
                    rest_ml = cofact_ml - (cofact_flesjes_20ml * 20)
                    cofact_flesjes_10ml = 1 if rest_ml > 0 else 0
                    totaal_flesjes = cofact_flesjes_20ml + cofact_flesjes_10ml
                else: 
                    cofact_flesjes = round(cofact_ie / IE_per_flesje)
            elif keuze == "Omniplasma":
                if levensbedreigend == "Ja":
                    omniplasma = int((dosis + 199) // 200) * 200
                else: 
                    omniplasma = int(round(dosis / 200) * 200)
                omniplasma_zak = int(omniplasma / 200)
                omniplasma_gebruikt = True

    if extem_a5 is not None and fibtem_a5 is not None:
        if 30 <= extem_a5 <= 40 and fibtem_a5 > 9:
            trombocyten = 1
            if not omniplasma_gebruikt and keuze == "Omniplasma":
                dosis = gewicht * 12.5
                if levensbedreigend == "Ja":
                    omniplasma = int((dosis + 199) // 200) * 200
                else: 
                    omniplasma = int(round(dosis / 200) * 200)
                omniplasma_zak = int(omniplasma / 200)
                omniplasma_gebruikt = True

    if fibtem_a5 is not None and extem_a5 is not None and fibtem_a5 < 9 and extem_a5 < 35:
        delta = 12 - fibtem_a5
        fibrinogeen_g = round((6.25 * delta * gewicht) / 1000)
        fibrinogeen_ml = round(delta * (3.8 / 12) * gewicht)

    advies = {}
    if keuze == "Cofact":
        if cofact_ml > 0:
            advies["Cofact"] = (f"{totaal_flesjes} flesje{'s' if totaal_flesjes > 1 else ''} "f"({cofact_ml} ml = {cofact_ie} IE = {cofact_mg} mg) " f"→ {cofact_flesjes_20ml}x 20 ml, {cofact_flesjes_10ml}x 10 ml"        
        else:
            advies["Cofact"] = "Geen toediening vereist"
    elif keuze == "Omniplasma":
        advies["Omniplasma"] = f"{omniplasma_zak} zakken ({omniplasma} ml)" if omniplasma_gebruikt else "Geen toediening vereist"
        
    advies["Trombocyten"] = f"{trombocyten} eenheid (330 ml)" if trombocyten > 0 else "Geen toediening vereist"

    if keuze_fib == "Fibrinogeen dosis":
        advies["Fibrinogeen dosis"]  = f"{fibrinogeen_g} g" if fibrinogeen_g > 0 else "Geen toediening vereist"
    elif keuze_fib == "Fibrinogeen concentraat":
        advies["Fibrinogeen concentraat"] = f"{fibrinogeen_ml} ml" if fibrinogeen_g > 0 else "Geen toediening vereist"

    return advies

# =======================
# State defenities
# =======================
if "advies" not in st.session_state:
    st.session_state.advies = False
if "advies_resultaat" not in st.session_state:
    st.session_state.advies_resultaat = {}
if "liveviewer_geopend" not in st.session_state:
    st.session_state.liveviewer_geopend = False
    
# =======================
# Koptekst
# =======================
col_left, col_right = st.columns([6, 1])
with col_left:
    st.markdown("## ROTEM-Tool")
    
st.info("**⚠️ Disclaimer:** De arts blijft altijd eindverantwoordelijk voor het uiteindelijke behandelbeleid. Deze tool dient ter ondersteuning, niet als vervanging van klinisch oordeel.")

# =======================
# Pagina 0 – Live viewer openen
# =======================
if not st.session_state.liveviewer_geopend:

    st.warning("Open de live viewer.")

    st.caption("Dubbel klik indien nodig om door te gaan naar invoerscherm.")
    if st.button("Klik om door te gaan ➡️"):
        st.session_state.liveviewer_geopend = True

# =======================
# Pagina 1 – Invoerscherm
# =======================

elif not st.session_state.advies:
        
    levensbedreigend = st.radio("Betreft het een patiënt met een levensbedreigende bloeding:", ["Ja", "Nee"], horizontal = True)
    product_keuze = st.radio("Maak een keuze:", ["Omniplasma", "Cofact"], horizontal=True)
    product_keuze_fib = st.radio("Maake een keuze:", ["Fibrinogeen dosis", "Fibrinogeen concentraat"], horizontal=True)

    st.markdown("Vul hieronder de patiëntgegevens in:")
    gewicht_kg = st.number_input("Gewicht (kg)", min_value=1.0, max_value=3000.0, value=None, step=0.1, format="%.1f")
    fibtem_a5 = st.number_input("FIBTEM A5 (mm)", min_value=0, max_value=500, value=None)
    extem_ct = st.number_input("EXTEM CT (seconden)", min_value=0, max_value=1000, value=None)
    extem_a5 = st.number_input("EXTEM A5 (mm)", min_value=0, max_value=1000, value=None)
    
    
    st.caption("Dubbel klik indien nodig om advies te genereren.")

    if st.button("Genereer advies ➡️"):
        waarschuwingen = []
        if gewicht_kg is None:
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
        
        st.session_state.extem_ct = extem_ct
        st.session_state.fibtem_a5 = fibtem_a5
        st.session_state.extem_a5 = extem_a5
        st.session_state.gewicht_kg = gewicht_kg
        st.session_state.product_keuze = product_keuze
        st.session_state.product_keuze_fib = product_keuze_fib
        st.session_state.product_levensbedreigend = levensbedreigend
  
        st.session_state.advies_resultaat = stap_2_na_ROTEM_geleide_stollingscorrectie(
            extem_ct, fibtem_a5, extem_a5, gewicht_kg, product_keuze, product_keuze_fib, levensbedreigend
        )
        st.session_state.advies = True

# =======================
# Pagina 2 – Adviesscherm
# =======================
else:
    adviezen = st.session_state.advies_resultaat
    overzicht_items = [f"{prod}: {val}" for prod, val in adviezen.items()]
    
   
    bullet_items = "".join([f"<li>{prod}: {val}</li>" for prod, val in adviezen.items()])
    st.markdown(f"""
        <div class='advies-overzicht'>
            <span style="font-size: 35px;">Advies:</span>
            <ul style="margin-top: 12px; font-size: 35px; font-weight: 600; color: #002B45;">
                {bullet_items}
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("### Toelichting per bloedproduct:")
    for product, waarde in adviezen.items():
        if waarde != "Geen toediening vereist" and waarde != "Niet nodig in de behandeling":
            st.markdown(f"**{product}**: {waarde}")
            if product == "Omniplasma":
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>EXTEM CT > 80 sec (waarde: {st.session_state.extem_ct} sec)</li>
                  <li>FIBTEM A5 > 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.gewicht_kg} kg</li>
                  <li>Levensbedreigende bloeding: {st.session_state.product_levensbedreigend}</li>
                </ul>
                """, unsafe_allow_html=True)

            elif product == "Cofact":
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>EXTEM CT > 80 sec (waarde: {st.session_state.extem_ct} sec)</li>
                  <li>FIBTEM A5 > 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.gewicht_kg} kg</li>
                  <li>Levensbedreigende bloeding: {st.session_state.product_levensbedreigend}</li>
                </ul>
                """, unsafe_allow_html=True)

            elif product == "Trombocyten":
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>EXTEM A5 tussen 30–40 mm (waarde: {st.session_state.extem_a5} mm)</li>
                  <li>FIBTEM A5 > 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.gewicht_kg} kg</li>
                  <li>Levensbedreigende bloeding: {st.session_state.product_levensbedreigend}</li>
                </ul>
                """, unsafe_allow_html=True)

            elif product.startswith("Fibrinogeen"):
                st.markdown(f"""
                <ul style="margin-top:4px; margin-bottom:12px; color:gray; font-size:0.85em;">
                  <li>FIBTEM A5 < 9 mm (waarde: {st.session_state.fibtem_a5} mm)</li>
                  <li>EXTEM A5 < 35 mm (waarde: {st.session_state.extem_a5} mm)</li>
                  <li>Gewicht: {st.session_state.gewicht_kg} kg</li>
                  <li>Levensbedreigende bloeding: {st.session_state.product_levensbedreigend}</li>
                </ul>
                """, unsafe_allow_html=True)


    st.caption("Dubbel klik indien nodig om terug te gaan naar invoerscherm")
    if st.button("⬅️ Terug naar invoerscherm"):
        st.session_state.advies = False

# =======================
# Voet tekst
# =======================
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Gemaakt door studenten Klinische Technologie: Anne de Zeeuw, Cedric Kalhorn, Fleur de Groot & Roos Ritsma</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.85em;'>Contactgegevens: m.a.dezeeuw@student.tudelft.nl, c.a.f.kalhorn@student.tudelft.nl, f.m.j.degroot@student.tudelft.nl & r.p.ritsma@student.tudelft.nl</p>", unsafe_allow_html=True)
