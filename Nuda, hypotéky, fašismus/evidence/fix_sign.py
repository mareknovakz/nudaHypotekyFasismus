import fitz

doc = fitz.open(r'c:\Repozitáře\nudaHypotekyFasismus\evidence.pdf')
page = doc[0]

sig_rect = fitz.Rect(380, 688, 530, 718)
page.insert_image(sig_rect, filename=r'c:\Repozitáře\nudaHypotekyFasismus\podpis.png')

# No Bc. this time

doc.save(r'c:\Repozitáře\nudaHypotekyFasismus\evidence_signed.pdf')
doc.close()
print('Done')
