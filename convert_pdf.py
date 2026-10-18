from docx2pdf import convert
import sys

try:
    print("Converting DOCX to PDF...")
    convert("ICFOSS_Project_Report_Final_Internship.docx", "ICFOSS_Project_Report_Final_Internship.pdf")
    print("PDF generated successfully!")
except Exception as e:
    print("Error during conversion:", e)
