from shiny import App, reactive, render, ui

def fibrinogeen_dosis(targeted_delta_A5: float):
    dosis_per_A5 = {2: 12.5, 4: 25.0, 6: 37.5, 8: 50.0, 10: 62.5, 12: 75.0}
    beschikbare_doses = sorted(dosis_per_A5.items())
    for a5, dosis in beschikbare_doses:
        if targeted_delta_A5 <= a5:
            return a5, dosis
    return beschikbare_doses[-1]  # hoogste waarde

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
            gekozen_a5, fibrinogeen_mg_per_kg = fibrinogeen_dosis(targeted_delta_A5)
            fibrinogeen_g = round((fibrinogeen_mg_per_kg * weight_kg) / 1000, 2)
            fibrinogeen_conc_ml_per_kg = fibrinogeen_ml_per_kg_dict[gekozen_a5]
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

app_ui = ui.page_fluid(
    ui.tags.style("""
        body { background-color: #f8fafc; }
        .card { border-radius: 1.5rem; box-shadow: 0 4px 24px rgba(0,0,0,0.07);}
        .btn-primary { background-color: #0d6efd; border-color: #0d6efd; }
        .custom-header { padding-top: 2rem; padding-bottom: 1rem;}
        .advice-card { background: linear-gradient(120deg, #dbeafe 60%, #f0fdf4 100%); border-radius: 1.5rem;}
        .output-label { font-weight: 500; color: #0369a1; margin-bottom: 0.5rem;}
        .custom-footer { text-align: center; margin-top: 2.5rem; color: #888;}
    """),
    ui.div(
        ui.h1("ROTEM Advies Tool", class_="text-center custom-header"),
        ui.p("Geef patiëntwaarden op en genereer direct een behandeladvies.", class_="text-center text-secondary"),
    ),
    ui.layout_columns(
        ui.div(
            ui.card(
                ui.card_header("Invoer patiëntwaarden"),
                ui.input_numeric("weight_kg", "Gewicht (kg)", value=70, min=1, max=300, width="100%"),
                ui.input_numeric("extem_ct", "EXTEM CT (seconde)", value=100, min=0, max=1000, width="100%"),
                ui.input_numeric("fibtem_a5", "FIBTEM A5 (mm)", value=5, min=0, max=50, width="100%"),
                ui.input_numeric("extem_a5", "EXTEM A5 (mm)", value=20, min=0, max=100, width="100%"),
                ui.input_action_button("submit", "Genereer advies", class_="btn btn-primary mt-3"),
            ), style="max-width: 350px; margin: 0 auto;"
        ),
        ui.div(
            ui.card(
                ui.card_header("Advies & Doseringen"),
                ui.div(
                    ui.output_text_verbatim("advies"),
                    class_="advice-card px-3 py-3"
                )

            ), style="max-width: 450px; margin: 0 auto;"
        ),
        col_widths=[6, 6]
    ),
    ui.div(
        "Powered by ROTEM • Clinical Technology • TU Delft",
        class_="custom-footer"
    )
)

def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.submit)
    def advies():
        gewicht = input.weight_kg()
        extem_ct = input.extem_ct()
        fibtem_a5 = input.fibtem_a5()
        extem_a5 = input.extem_a5()
        advies = stap_2_na_ROTEM_geleide_stollingscorrectie(extem_ct, fibtem_a5, extem_a5, gewicht)
        advies_str = (
            f"Cofact-dosis: {advies['cofact_dosis']} ml\n"
            f"OP minimaal: {advies['op_min']} ml\n"
            f"OP maximaal: {advies['op_max']} ml\n"
            f"TC aantal: {advies['tc_aantal']}\n"
            f"Fibrinogeen (g): {advies['fibrinogeen_g']}\n"
            f"Targeted delta A5: {advies['targeted_delta_A5']}\n"
            f"Fibrinogeen conc. (ml/kg): {advies['fibrinogeen_conc_ml_per_kg']}\n"
            f"Fibrinogeen conc. totaal (ml): {advies['fibrinogeen_conc_ml_totaal']}"
        )
        return advies_str

app = App(app_ui, server)
