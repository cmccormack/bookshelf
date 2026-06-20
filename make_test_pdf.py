from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=16)
pdf.cell(0, 10, "Test Book for CWA Ingest", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=12)
pdf.multi_cell(0, 8, "This is a test PDF to verify Calibre-Web Automated PDF conversion and ingest.")
pdf.output("ingest/test_book.pdf")
print("Created ingest/test_book.pdf")
