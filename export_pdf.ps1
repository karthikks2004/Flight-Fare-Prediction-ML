$word = New-Object -ComObject Word.Application
$word.Visible = $false

# Disable image compression in Word application settings globally for this session
$word.Options.SavePropertiesPrompt = $false
$word.Options.DoNotPromptForConvert = $true

$inputPath = "D:\Machinelearning icfoss\FINAL PROJECT FOR GRADING\ICFOSS_Project_Report_Final_Internship.docx"
$outputPath = "D:\Machinelearning icfoss\FINAL PROJECT FOR GRADING\ICFOSS_Project_Report_Final_Internship.pdf"

Write-Host "Opening document: $inputPath"
$doc = $word.Documents.Open($inputPath)

# 17 = wdExportFormatPDF, 0 = wdExportOptimizeForPrint
Write-Host "Exporting to PDF with high-quality print optimization..."
$doc.ExportAsFixedFormat($outputPath, 17, $false, 0)

$doc.Close($false)
$word.Quit()

Write-Host "PDF export complete! Saved as: $outputPath"
