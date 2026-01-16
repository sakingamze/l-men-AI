from fpdf import FPDF
from datetime import datetime

def generate_pdf(username, role, analysis_text):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    # Başlık
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, " Lümen-AI Kod Analiz Raporu", ln=True)

    pdf.ln(5)

    # Kullanıcı bilgileri
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Kullanıcı: {username}", ln=True)
    pdf.cell(0, 8, f"Mentör Seviyesi: {role}", ln=True)
    pdf.cell(0, 8, f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True)

    pdf.ln(10)

    # Analiz
    pdf.set_font("Arial", size=11)
    for line in analysis_text.split("\n"):
        pdf.multi_cell(0, 7, line)

    file_path = f"lumen_ai_rapor_{username}.pdf"
    pdf.output(file_path)

    return file_path
