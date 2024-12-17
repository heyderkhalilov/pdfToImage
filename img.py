import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path
from pypdf import PdfReader
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import uuid
import os
 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
            print(pg_no)            
            images[i].save(destination+r"/"+'sehife '+ str(pg_no) +'.jpg', 'JPEG')
    except Exception as e:
        print(str(e))


def SliceImageToQuestions():
    # destination = tk.filedialog.askdirectory()
    filename = filedialog.askopenfilenames(
        filetypes=[('Images', '*.jpg *.jpeg *.png *.BMP')])
    sclice(filename)

def openfolder():
    destination = tk.filedialog.askdirectory()
    return destination


def sclice(pathh):
    img = cv2.imread(pathh[0])    
    filename = os.path.basename(pathh[0])
    dir_path = os.path.split(pathh[0])[0]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    index = filename.find('.')
    filename=filename[0:index]
    dir_path = dir_path+r"/"+filename
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)

    try:
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                if (w > 30) and (h > 20):
                    cropped_image = img[y:y+h, x:x+w]             
                    image_name=questionNoToFileName(cropped_image)                    
                    cv2.imwrite(dir_path+r"/" + image_name +".jpg", cropped_image)
    except Exception as e:
        print(str(e))


def questionNoToFileName(img):    
    try:
        crop=img[0:100, 0:100]
        img_name=pytesseract.image_to_string(crop).strip()
        return(img_name)
    except Exception as e:
        print(str(e))
        id=uuid.uuid4() 
        return(str(id))
    

openPdf_btn = tk.Button(root, text="PDF faylını ac", command=openPdf)

first_page_label = tk.Label(root, text = 'İlk səhifə', font=('calibre',10, 'bold'))
first_page_entry = tk.Entry(root,textvariable = page_first_var, font=('calibre',10,'normal'))
last_page_label = tk.Label(root, text = 'Son səhifə', font = ('calibre',10,'bold'))
last_page_entry=tk.Entry(root, textvariable = page_last_var, font = ('calibre',10,'normal'))
 
convert_btn=tk.Button(root,text = 'Şəkilə çevir', command = convert)

slice_btn=tk.Button(root,text = 'Şəkli suallara ayır', command = SliceImageToQuestions)
 
openPdf_btn.grid(row=0,column=1)
first_page_label.grid(row=1,column=0)
first_page_entry.grid(row=1,column=1)
last_page_label.grid(row=2,column=0)
last_page_entry.grid(row=2,column=1)
convert_btn.grid(row=3,column=1)
slice_btn.grid(row=4,column=1)



#btn_pdf_to_image.pack(padx=12,pady=5)
#root.bind('<Return>', lambda event: pdftoimage())


 
root.mainloop()
