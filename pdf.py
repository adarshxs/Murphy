import fitz # this is PyMuPDF
filepath = "test.pdf" # change this to your pdf file path
text = '' # initialize text buffer
with fitz.open(filepath) as doc: # open the pdf document
    for page in doc: # iterate through the pages
        text += page.get_text() # append the text of each page to the buffer

with open('output.txt', 'w', encoding='utf-8') as f: # open a file for writing
 f.write(text) # write the extracted text to the file
