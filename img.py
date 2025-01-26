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
from PIL import Image
 
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
    filename = filedialog.askopenfilename(
        filetypes=[('Images', '*.jpg *.jpeg *.png *.BMP')])
    #sclice2(filename)
    slice_inner_rectangles(filename)

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
                if (w > 100) and (h > 100):
                    cropped_image = img[y:y+h, x:x+w]             
                    image_name=questionNoToFileName(cropped_image)  
                    print(image_name)                  
                    cv2.imwrite(dir_path+r"/" + image_name +".jpg", cropped_image)
    except Exception as e:
        print(str(e))




def sclice2(pathh):
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
        for i, cnt in enumerate(contours):
            # Use hierarchy to ensure only inner contours are considered
            # hierarchy[i][3] == -1 means the contour has no parent
            if hierarchy[0][i][3] != -1:  # Only process inner contours
                approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                
                if len(approx) == 4:  # Ensure it's a rectangle
                    x, y, w, h = cv2.boundingRect(cnt)
                    if w > 100 and h > 100:  # Filter based on size
                        cropped_image = img[y:y+h, x:x+w]             
                        image_name = questionNoToFileName(cropped_image)  
                        print(image_name)                  
                        cv2.imwrite(dir_path + r"/" + image_name + ".jpg", cropped_image)

    except Exception as e:
        print(str(e))


def slice_inner_rectangles(image_path):
    img = cv2.imread(image_path)    
    filename = os.path.basename(image_path)
    dir_path = os.path.dirname(image_path)
    
    # Create output directory
    index = filename.find('.')
    filename = filename[:index]
    dir_path = dir_path+r"/"+filename
    if not os.path.exists(dir_path):
      os.makedirs(dir_path)

    # Convert to grayscale and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Find contours with hierarchy
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]  # Simplify access to the hierarchy array

    try:
        for i, cnt in enumerate(contours):
            # Only process contours with a parent (inner rectangles)
            if hierarchy[i][3] != -1:  # Check if the contour has a parent
                approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                
                # Ensure the contour is a rectangle (4 corners)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(cnt)
                    
                    # Apply size filtering (adjust as needed)
                    if w > 100 and h > 100:
                        cropped_image = img[y:y+h, x:x+w]
                        b,g,r = (cropped_image[2, 15])
                        dominant_color=int(b)+int(r)+int(g)  

                        if dominant_color>400:                
                            image_name = questionNoToFileName(cropped_image)                 
                            cv2.imwrite(dir_path + r"/" + image_name + ".jpg", cropped_image)
    except Exception as e:
        print(f"Error: {str(e)}")



def findDigits(str):
    number=''
    for char in str:
        if char.isdigit():
            number+=char
    
    if number == '':
        id=uuid.uuid4() 
        return(str(id))        
    else:
        return number

def questionNoToFileName(img):    
    try:
        crop=img[0:140, 0:120]
        img_name=pytesseract.image_to_string(crop)
        img_name=img_name.strip()
        img_name=img_name.split('.')
        img_name=img_name[0]        
        img_name=img_name.split(',')
        img_name=img_name[0]        
        return img_name
    except Exception as e:
        print('question no to file name error:  '+str(e))
        id=uuid.uuid4() 
        return (str(id))
    


def detectQuestion():
    filename = filedialog.askopenfilename(
        filetypes=[('Images', '*.jpg *.jpeg *.png *.BMP')])
    
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    cv2.waitKey(0) 
   


openPdf_btn = tk.Button(root, text="PDF faylını ac", command=openPdf)

first_page_label = tk.Label(root, text = 'İlk səhifə', font=('calibre',10, 'bold'))
first_page_entry = tk.Entry(root,textvariable = page_first_var, font=('calibre',10,'normal'))
last_page_label = tk.Label(root, text = 'Son səhifə', font = ('calibre',10,'bold'))
last_page_entry=tk.Entry(root, textvariable = page_last_var, font = ('calibre',10,'normal'))
 
convert_btn=tk.Button(root,text = 'Şəkilə çevir', command = convert)

slice_btn=tk.Button(root,text = 'Şəkli suallara ayır', command = SliceImageToQuestions)

detectQuestion_btn=tk.Button(root,text= " Suallari tap ", command= detectQuestion )
 
openPdf_btn.grid(row=0,column=1)
first_page_label.grid(row=1,column=0)
first_page_entry.grid(row=1,column=1)
last_page_label.grid(row=2,column=0)
last_page_entry.grid(row=2,column=1)
convert_btn.grid(row=3,column=1)
slice_btn.grid(row=4,column=1)

detectQuestion_btn.grid(row=5,column=1)



#btn_pdf_to_image.pack(padx=12,pady=5)
#root.bind('<Return>', lambda event: pdftoimage())


 
root.mainloop()
