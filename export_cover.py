import scribus

pdf = scribus.PDFfile()
pdf.file = "c:\\Repozitáře\\nudaHypotekyFasismus\\Prebal_v7.pdf"
pdf.quality = 0
pdf.fontEmbedding = 0
pdf.version = 14
pdf.resolution = 300
pdf.save()
