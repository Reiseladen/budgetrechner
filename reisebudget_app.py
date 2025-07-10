# reisebudget_app.py

import streamlit as st
import datetime
from fpdf import FPDF
import base64

# Beispielhafte Tagesbudgets pro Person und Reisestil (EUR)
budget_data = {
    "Österreich": {"Low-Budget": 60, "Mittelklasse": 110, "Luxus": 200},
    "Deutschland": {"Low-Budget": 65, "Mittelklasse": 115, "Luxus": 210},
    "Italien": {"Low-Budget": 70, "Mittelklasse": 120, "Luxus": 220},
    "Spanien": {"Low-Budget": 60, "Mittelklasse": 110, "Luxus": 200},
    "Kroatien": {"Low-Budget": 50, "Mittelklasse": 100, "Luxus": 180},
    "Griechenland": {"Low-Budget": 55, "Mittelklasse": 105, "Luxus": 190}
}

st.set_page_config(page_title="Reisebudget-Rechner", layout="centered")
st.title("💶 Reisebudget-Rechner")
st.markdown("Berechne dein geschätztes Urlaubsbudget auf Basis deiner Reisedaten.")

# Eingabefelder
reiseziel = st.selectbox("Reiseziel", list(budget_data.keys()))
dauer = st.number_input("Reisedauer (in Tagen)", min_value=1, max_value=90, value=7)

st.subheader("👥 Anzahl der Reisenden")
erwachsene = st.number_input("Erwachsene", min_value=1, max_value=10, value=1)
kinder = st.number_input("Kinder (inkl. Babys)", min_value=0, max_value=10, value=0)
babys = st.number_input("Davon Babys", min_value=0, max_value=kinder, value=0)
haustiere = st.number_input("Haustiere", min_value=0, max_value=5, value=0)

unterkunft = st.selectbox("Unterkunftstyp", ["Low-Budget", "Mittelklasse", "Luxus"])
anreise = st.selectbox("Anreiseart", ["Flug", "Bahn", "Auto"])
aktivitaeten = st.multiselect("Geplante Aktivitäten", ["Restaurants", "Bars & Discos", "Sport"])
bestehende_ausgaben = st.text_input("Bereits gebuchte Ausgaben (z. B. Flug, Hotel)", placeholder="z. B. 400 für Flug")
freie_anmerkungen = st.text_area("Weitere Hinweise", placeholder="z. B. Mietwagen, Eintritte, Rabatte")

# PDF Generator
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Reisebudget Übersicht", ln=True, align="C")
        self.ln(5)

    def chapter_body(self, text):
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln()

if st.button("📊 Budget berechnen"):
    tagesbudget = budget_data[reiseziel][unterkunft]
    personen_gesamt = erwachsene + kinder
    gesamt_budget = dauer * tagesbudget * personen_gesamt

    st.subheader("💰 Geschätztes Urlaubsbudget")
    st.write(f"Reiseziel: **{reiseziel}**")
    st.write(f"Dauer: **{dauer} Tage**")
    st.write(f"Anzahl Personen: **{personen_gesamt} (inkl. {babys} Babys, {haustiere} Haustiere)**")
    st.write(f"Unterkunftstyp: **{unterkunft}**, Tagesbudget: **{tagesbudget:.2f} € pro Person**")
    st.write(f"**Gesamtkosten: ~{gesamt_budget:.2f} €** (exkl. Anreise & Aktivitäten)")

    if bestehende_ausgaben:
        st.write(f"Bereits gebuchte Ausgaben: {bestehende_ausgaben}")

    if aktivitaeten:
        st.write(f"Geplante Aktivitäten: {', '.join(aktivitaeten)}")

    if freie_anmerkungen:
        st.markdown("---")
        st.subheader("📝 Anmerkungen")
        st.markdown(f"{freie_anmerkungen}")

    pdf = PDF()
    pdf.add_page()
    content = f"""
Reiseziel: {reiseziel}
Dauer: {dauer} Tage
Erwachsene: {erwachsene}
Kinder: {kinder} (davon Babys: {babys})
Haustiere: {haustiere}
Unterkunft: {unterkunft}
Anreiseart: {anreise}
Tagesbudget: {tagesbudget:.2f} €
Gesamtbudget: ~{gesamt_budget:.2f} €
"""
    if bestehende_ausgaben:
        content += f"Bereits gebuchte Ausgaben: {bestehende_ausgaben}\n"

"
    if aktivitaeten:
        content += f"Geplante Aktivitäten: {', '.join(aktivitaeten)}

"
    if freie_anmerkungen:
        content += f"Anmerkungen: {freie_anmerkungen}
"

    pdf.chapter_body(content)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64_pdf = base64.b64encode(pdf_output).decode('utf-8')
    pdf_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="reisebudget.pdf">📥 PDF herunterladen</a>'
    st.markdown(pdf_link, unsafe_allow_html=True)

    share_text = f"Ich habe mein Reisebudget für {reiseziel} berechnet: ca. {gesamt_budget:.2f} €. Jetzt ausprobieren!"
    share_url = f"https://wa.me/?text={share_text.replace(' ', '%20')}"
    st.markdown(f"[🔗 Teilen via WhatsApp]({share_url})")
