import fitz

async def handle_pdf_cut(input_pdf, rows, cols):
    try:
        doc = fitz.open(input_pdf)
        new_doc = fitz.open()
        
        for page in doc:
            rect = page.rect
            width = rect.width / cols
            height = rect.height / rows
            
            for r in range(rows):
                for c in range(cols):
                    x0 = rect.x0 + c * width
                    y0 = rect.y0 + r * height
                    x1 = x0 + width
                    y1 = y0 + height
                    clip_rect = fitz.Rect(x0, y0, x1, y1)
                    
                    new_page = new_doc.new_page(width=width, height=height)
                    new_page.show_pdf_page(new_page.rect, doc, page.number, clip=clip_rect)
                    
        output_pdf = input_pdf.replace(".pdf", "_cut.pdf")
        new_doc.save(output_pdf)
        new_doc.close()
        doc.close()
        return output_pdf
    except Exception as e:
        print(f"ERROR in PyMuPDF grid cut: {e}")
        return None
