import streamlit as st

def fibrinogeen_dosis_lineair(targeted_delta_A5: float):
    # 6.25 komt uit je tabel: elke 2 stijgt de dosis met 12.5, dus 12.5/2 = 6.25 per A5
    dosis = targeted_delta_A5 * 6.25
    return dosis
    
def stap_2_na_ROTEM_geleide_stollingscorrectie(EXTEM_CT, FIBTEM_A5, EXTEM_A5, weight_kg):
    cofact_dosis = 0.0
    op_min = 0.0
    op_max = 0.0
    tc_aantal = 0
    fibrinogeen_g = 0.0
    targeted_delta_A5 = None
    fibrinogeen_conc_ml_per_kg = 0.0
    fibrinogeen_conc_ml_totaal = 0.0

    fibrinogeen_ml_per_kg_dict = {
        2: 0.6,
        4: 1.2,
        6: 1.9,
        8: 2.5,
        10: 3.1,
        12: 3.8
    }

    if EXTEM_CT > 80 and FIBTEM_A5 > 9:
        cofact_dosis = round(0.4 * weight_kg, 1)
        op_min = round(10 * weight_kg, 1)
        op_max = round(15 * weight_kg, 1)
    if 30 <= EXTEM_A5 <= 40 and FIBTEM_A5 > 9:
        tc_aantal += 1
    if EXTEM_A5 < 30:
        tc_aantal += 1
        op_min = round(10 * weight_kg, 1)
        op_max = round(15 * weight_kg, 1)
    if FIBTEM_A5 < 9 and EXTEM_A5 < 35:
        targeted_delta_A5 = 12 - FIBTEM_A5
        if targeted_delta_A5 > 0:
            fibrinogeen_mg_per_kg = fibrinogeen_dosis_lineair(targeted_delta_A5)
            fibrinogeen_g = round((fibrinogeen_mg_per_kg * weight_kg) / 1000, 2)
            fibrinogeen_conc_ml_per_kg = targeted_delta_A5 * (3.8 / 12)
            fibrinogeen_conc_ml_totaal = round(fibrinogeen_conc_ml_per_kg * weight_kg, 1)
        else:
            fibrinogeen_g = 0.0
            fibrinogeen_conc_ml_per_kg = 0.0
            fibrinogeen_conc_ml_totaal = 0.0

    return {
        "cofact_dosis": cofact_dosis,
        "op_min": op_min,
        "op_max": op_max,
        "tc_aantal": tc_aantal,
        "fibrinogeen_g": fibrinogeen_g,
        "targeted_delta_A5": targeted_delta_A5,
        "fibrinogeen_conc_ml_per_kg": fibrinogeen_conc_ml_per_kg,
        "fibrinogeen_conc_ml_totaal": fibrinogeen_conc_ml_totaal
    }

st.title("ROTEM Advies Tool")
st.write("Geef patiëntwaarden op en genereer direct een behandeladvies.")
st.write("Voeg hier disclaimers toe")

# Inputvelden
weight_kg = st.number_input("Gewicht (kg)", min_value=1, max_value=300, value=70)
extem_ct = st.number_input("EXTEM CT (seconde)", min_value=0, max_value=1000, value=100)
fibtem_a5 = st.number_input("FIBTEM A5 (mm)", min_value=0, max_value=50, value=5)
extem_a5 = st.number_input("EXTEM A5 (mm)", min_value=0, max_value=100, value=20)

if st.button("Genereer advies"):
    advies = stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, weight_kg)
    st.subheader("Advies & Doseringen")
    st.code(
        f"Cofact-dosis: {advies['cofact_dosis']} ml\n"
        f"OP minimaal: {advies['op_min']} ml\n"
        f"OP maximaal: {advies['op_max']} ml\n"
        f"TC aantal: {advies['tc_aantal']}\n"
        f"Fibrinogeen (g): {advies['fibrinogeen_g']}\n"
        f"Targeted delta A5: {advies['targeted_delta_A5']}\n"
        f"Fibrinogeen conc. (ml/kg): {advies['fibrinogeen_conc_ml_per_kg']}\n"
        f"Fibrinogeen conc. totaal (ml): {advies['fibrinogeen_conc_ml_totaal']}"
    )
    st.caption("Powered by ROTEM • Clinical Technology • TU Delft")
