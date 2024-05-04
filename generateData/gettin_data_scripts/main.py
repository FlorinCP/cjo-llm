import PyPDF2

with open("../data/codpenal.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        print(page_text)
        if page_text:
            full_text += page_text + "\n"

with open("./output.txt", "w", encoding="utf-8") as file:
    file.write(full_text)
