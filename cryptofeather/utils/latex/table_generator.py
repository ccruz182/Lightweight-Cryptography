'''
  File name: utils/latex/table_generator.py
  Author: Cesar Cruz
  Project: cryptofeather
  Python Version: 2.7
'''

from pylatex import Document, LongTabu, HFill, PageStyle, Head, LargeText
from pylatex.utils import bold

def generate_table(header_text, header_row, rows, pdf_name):
  geometry_options = {
        "landscape": True,
        "margin": "1.0in",
        "headheight": "14pt",
        "headsep": "10pt",
        "includeheadfoot": True
  }
  header = PageStyle("header")
  doc = Document(page_numbers=True, geometry_options=geometry_options)

  with header.create(Head("C")):
    header.append(LargeText(bold(header_text)))
  
  doc.preamble.append(header)
  doc.change_document_style("header")

  header_latex = generate_header_latex(len(header_row))
  
  with doc.create(LongTabu(header_latex)) as data_table:    
    data_table.add_row(header_row, mapper=[bold])
    data_table.add_hline()
    data_table.add_empty_row()
    data_table.end_table_header()

    for row in rows:
      data_table.add_row(row)
  
  doc.generate_pdf(pdf_name, clean_tex=False)
  doc.generate_tex()


def generate_header_latex(num_rows):
  header_latex = ""
  
  for i in range(num_rows):
    header_latex = header_latex + "X[r] "

  return header_latex.rstrip()
