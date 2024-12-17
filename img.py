import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from pypdf import PdfReader
 
root=tk.Tk()
root.geometry("600x400")
page_first_var=tk.StringVar()
page_last_var=tk.StringVar()
pdf_file_name=""

 
def openPdf():
    filename = filedialog.askopenfilename()  
    global pdf_file_name
    pdf_file_name=filename             
    try:
        reader = PdfReader(filename)
        print('Səhifə sayı ='+str(len(reader.pages)))
    except Exception as e:
        print(str(e))
        

def convert():
    first_page=page_first_var.get()
    last_page=page_last_var.get()

    pdfToImage(int(first_page),int(last_page))
    
    page_first_var.set("")
    page_last_var.set("")

   
def pdfToImage(f,l):
    poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"  
    global pdf_file_name   
    try:   
        images = convert_from_path(pdf_file_name,first_page= f ,last_page=l,poppler_path=poppler_path)
        destination = filedialog.askdirectory()
        print(destination)
        for i in range(len(images)):      
            pg_no=f+i
            print(i)
            images[i].save(destination+r"/"+'sehife '+ str(pg_no) +'.jpg', 'JPEG')
    except Exception as e:
        print(str(e))


openPdf_btn = tk.Button(root, text="PDF faylını ac", command=openPdf)

first_page_label = tk.Label(root, text = 'İlk səhifə', font=('calibre',10, 'bold'))
first_page_entry = tk.Entry(root,textvariable = page_first_var, font=('calibre',10,'normal'))
last_page_label = tk.Label(root, text = 'Son səhifə', font = ('calibre',10,'bold'))
last_page_entry=tk.Entry(root, textvariable = page_last_var, font = ('calibre',10,'normal'))
 
sub_btn=tk.Button(root,text = 'Şəkilə çevir', command = convert)
 
openPdf_btn.grid(row=0,column=1)
first_page_label.grid(row=1,column=0)
first_page_entry.grid(row=1,column=1)
last_page_label.grid(row=2,column=0)
last_page_entry.grid(row=2,column=1)
sub_btn.grid(row=3,column=1)



#btn_pdf_to_image.pack(padx=12,pady=5)
#root.bind('<Return>', lambda event: pdftoimage())


 
root.mainloop()
