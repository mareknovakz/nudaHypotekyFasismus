import fitz

doc = fitz.open('evidence.pdf')
page = doc[0]

sig_rect = fitz.Rect(380, 688, 530, 718)
page.insert_image(sig_rect, filename='podpis.png')

# No Bc. this time

doc.save('evidence_signed.pdf')
doc.close()
print('Done')
