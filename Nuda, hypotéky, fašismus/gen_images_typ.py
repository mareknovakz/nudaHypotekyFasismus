typst_content = r"""
#set page(
  paper: "a4",
  flipped: true,
  margin: 5mm,
)

#set text(font: "Courier Prime", size: 10pt)

// --- COVER PAGE ---
#page(margin: 0mm)[
  #image("Přebal_v2.pdf", width: 100%, height: 100%, fit: "cover")
]

// --- IMAGES PAGES ---
#let img_w = 115mm
#let img_h = 185mm
#let gap = 5mm

#let draw_images(img_list) = {
  let chunks = ()
  for i in range(0, img_list.len(), step: 2) {
    let chunk = ()
    chunk.push(img_list.at(i))
    if i + 1 < img_list.len() {
      chunk.push(img_list.at(i + 1))
    }
    chunks.push(chunk)
  }

  for chunk in chunks {
    align(center + horizon)[
      #grid(
        columns: (img_w, img_w),
        column-gutter: gap,
        rows: (img_h),
        ..chunk.map(path => {
          stack(
            spacing: 2mm,
            rect(width: img_w, height: img_h, stroke: 0.2pt + gray, inset: 0pt)[
              #image(path, width: 100%, height: 100%, fit: "cover")
            ],
            text(fill: gray, size: 8pt)[#path]
          )
        })
      )
    ]
    pagebreak(weak: true)
  }
}

#draw_images(("DreamCoreObdelnik.png", "pole.png", "koně.png", "predmesti.png", "věž.png", "dveře.png", "postel3.png"))
"""
with open("images_a4.typ", "w", encoding="utf-8") as f:
    f.write(typst_content)
