#!/usr/bin/env python
# coding: utf-8
# In[26]:
from tkinter import *
from tkinter import StringVar
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
# from PIL import ImageTk, Image
from os import path
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import path
import os.path
import pandas as pd
import time
import os
import os.path
import string
import random
import csv


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::: Main Program :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def checker(namaToko):
    if len(urlTkinter.get()) == 0:
        messageUrl()
        return False
    substring = "https://www.tokopedia.com/"
    if substring not in namaToko:
        mssgUrlError()
        return False

daftarToko = []
results = []
pageCounter=0
global jumlahScraped
jumlahScraped=len(results)
checkerResult=False

# In[27]:
# --Pengaturan Chrome Drive--
chrome_options = Options()
chrome_options.headless = True
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(
    executable_path="chromedriver.exe")
    # , chrome_options=chrome_options)

def findByTestId(element, tag, identifier):
    data = element.find(tag, attrs={"data-testid": identifier})
    return data.text if data else ""

def findByClassId(element, tag, identifier):
    data = element.find(tag, class_=identifier)
    return data.text if data else ""

# In[28]:

def getLink(namaToko, page):
    linkToko = "https://www.tokopedia.com/" + \
        str(namaToko)+"/product/page/"+str(page)+"?perpage=80"
    return linkToko

with open(InputPath, newline='') as f:
  reader = csv.reader(f)
  dataCSV = list(reader)

def ambilNamaToko(listNamaCSV):
    for item in listNamaCSV:
        linkToko = ''.join(str(e) for e in item)
        namaTokoScrap = linkToko.strip()
        namaTokoScrap = namaTokoScrap.replace("https://www.tokopedia.com/", "")
        namaTokoScrap = namaTokoScrap.replace(";", "")
        daftarToko.append(namaTokoScrap)
        if namaTokoScrap=="":
            break
        print(namaTokoScrap)

ambilNamaToko(dataCSV)

# In[29]:

def getUlasan(link):
    driver.get(link)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    return findByTestId(soup,"span","lblPDPDetailProductRatingCounter")

# Fungsi Utama
def run(namaToko, page):
    tokoKe = 0
    linkToko = getLink(namaToko, page, tokoKe)
    tokoKe = tokoKe + 1
    driver.get(linkToko)
    scrollbawah = "window.scrollBy(0,500);"
    for y in range(1, 11):
        driver.execute_script(scrollbawah)
        time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    products = soup.find_all("div", attrs={'data-testid': "divProductWrapper"})
    for product in products:
        rating = findByClassId(product, "span", "css-etd83i")
        linkProduk = product.find("div", class_="css-7fmtuv").a["href"]
        # gambarProd = product.find("div", attrs={'data-testid': "imgProduct"})

        result = {
            "Nama": (findByTestId(product, "div", "linkProductName")),
            "Harga": (findByTestId(product, "div", "linkProductPrice")),
            "Terjual": (findByClassId(product, "span", "css-1kgbcz0")),
            "Rating ": rating,
            "Link URL ": linkProduk,
            # "Gambar ": gambarProd.img["src"],
            "Harga Sebelum Diskon": (findByTestId(product, "div", 'lblProductSlashPrice')),
            "Jumlah ulasan": getUlasan(linkProduk) if rating else "",
        }
        results.append(result)
    return len(products) > 0


# In[32]:
def start():
    global checkerResult
    if checkerResult==True:
        messageStartClear()
        clear()
    page=1
    global pageCounter
    namaToko=urlTkinter.get()
    if checker(namaToko)==False:
        return
    else:
        namaTokoScrap = namaToko.strip()
        # namaTokoScrap = namaTokoScrap.replace("https://www.tokopedia.com/", "")
        checkerResult = True
        while True:
            if run(namaTokoScrap, page) == False:
                break
            jumlahScraped = len(results)
            page+= 1
            pageCounter += 1
            berubah(jumlahScraped)
        print(results)
        print(pageCounter)
        print(jumlahScraped)
        message()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def change():
    # Variabel untuk menyimpan hasil input nama csv
    nama_csv = changeFileName.get()
    # Variabel untuk menyimpan path dari file csv
    pathFile = changeFilePath.get()

    if len(changeFileName.get()) == 0:
        nama_csv = 'tkpdScrap' + "_"+ urlTkinter.get().strip().replace("https://www.tokopedia.com/", "")   + "_"+id_generator()
    if len(changeFilePath.get()) == 0:
        #cwd = os.getcwd()
        #Menyimpan ke user/download
        homedir = os.path.expanduser("~")
        pathFile = homedir+'\Hasil scrap'

    if path.exists(pathFile)== False:
        os.makedirs(pathFile)
        print("sukses")
        
    if path.exists(pathFile):
        print("Folder exist")
    else:
        messageWarning()
        print("Folder not exist")
    download(nama_csv, pathFile)

    # if my_file.is_file():
    #     print("File exist")
    # else:
    #     messageWarning()
    #     print("File not exist")

def download(nama_csv, path):
    if len(results) == 0:
        messageNotice()
    else:
        df = pd.DataFrame(results)
        df.index+=1
        # saving the dataframe
        # Menampilkan kolom no dimulai dari angka 1
        df.to_csv(path + '/' + nama_csv + '.csv', index=1, index_label='No')
        messageSccs()
        print(nama_csv)
        print(path)


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::: GUI Program :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# the whole window
main_window = Tk()
main_window.title("Webscrapping")  # the title of apps
main_window.geometry("850x600")  # pixels of the apps
main_window.configure(bg="#F6F9FE")  # main background of the apps
main_window.resizable(0, 0)

#dirname = os.path.dirname(__file__)

photo = PhotoImage(file="exer_kecil.png")
photo_label = Label(main_window, image=photo)
photo_label.grid(row=0, column=1, sticky = "")

# --- Variabel String untun input GUI ---
urlTkinter = StringVar()
changeFileName = StringVar()
changeFilePath = StringVar()
jumlahScrapedTampil=StringVar()
pageCounterTampil=StringVar()
#jumlahScrapedTampil.set(jumlahScraped)
#pageCounterTampil.set(pageCounter)

# All about input URL
# --- Variabel String untun input GUI ---
urlTkinter = StringVar()
changeFileName = StringVar()
changeFilePath = StringVar()
jumlahScrapedTampil=StringVar()
pageCounterTampil=StringVar()
#jumlahScrapedTampil.set(jumlahScraped)
#pageCounterTampil.set(pageCounter)

InputPath = []
#Fungsi File Input
def select_file_input():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.csv')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename,
    )
    global InputPath
    InputPath = filename

# File Input Location
FileInput= LabelFrame(text=" File Input ", font=(
    'roboto', 11, 'bold'), bg="#F6F9FE")
InpFile = Label(FileInput, text="File Input Name", fg="#C10ABA",
                bg="#F6F9FE", font=('roboto', 11, 'bold'), width=80)
namaFile_in = Button(FileInput, padx=19.4, pady=7, text=" Open ", fg="#FAFAFA", borderwidth=2,
                bg="#442B71",relief=RAISED, font=('roboto', 12, "bold"), width=10, command=select_file_input)
InpFile.pack()
namaFile_in.pack()
FileInput.place(x=50, y=125)





#Pause & Continue Button
Reset = Button(main_window, text="Reset" ,bg="#442B71", 
            fg="#FAFAFA",borderwidth=2, padx=19.4, pady=7, relief=RAISED,font=('roboto', 12, 'bold'))
StartButton = Button(main_window, padx=20, pady=12, text="START", fg="#FAFAFA", 
            bg="#442B71",relief=RAISED, font=('roboto', 12, "bold"))
StartButton.place(x=550, y=470)
Reset.place(x=555, y=530)

#Fungsi Scraped
def clear():
    global pageCounter
    global checkerResult
    jumlahScrapedTampil.set("0")
    pageCounter=0
    pageCounterTampil.set("0")
    urlTkinter.set("")
    changeFileName.set("")
    changeFilePath.set("")
    results.clear()
    checkerResult=False


#Data scraped progress
Scraped = LabelFrame(text=" Scraped result ", font=(
            'roboto', 11, 'bold'), bg="#F6F9FE")
scrpd = Label(Scraped, text='Scraped Product', fg="#C10ABA",
            bg="#F6F9FE", font=('roboto', 11, 'bold'), width=80)
Data = Label(Scraped, textvariable=jumlahScrapedTampil, fg="#C10ABA",
            bg="#F6F9FE", font=('roboto', 11, 'bold'), width=80)
scrpdPage = Label(Scraped, text='Page Scraped', fg="#C10ABA",
            bg="#F6F9FE", font=('roboto', 11, 'bold'), width=80)
Page = Label(Scraped, textvariable=pageCounterTampil, fg="#C10ABA",
            bg="#F6F9FE", font=('roboto', 11, 'bold'), width=80, height=1)
scrpd.pack()
Data.pack()
scrpdPage.pack()
Page.pack()
Scraped.place(x=50, y=245)

# -- Untuk menampilkan hasil scrap dan page yang telah dilakukan--
def berubah(jumlahScraped):
    # --Variabel Progress scrapping--
    # Data scraped progress
    jumlahScrapedTampil.set(jumlahScraped)
    pageCounterTampil.set(pageCounter)
    Scraped = LabelFrame(text=" Scraped result ", font=('roboto', 11,
                'bold'), bg="#F6F9FE")
    scrpd = Label(Scraped, text='Scraped Product', fg="#C10ABA",
                bg="#F6F9FE", font=('roboto', 11, 'bold'),width=80 )
    Data = Label(Scraped, textvariable=jumlahScrapedTampil, fg="#C10ABA",
                bg="#F6F9FE", font=('roboto', 11, 'bold'),width=80 )
    scrpdPage = Label(Scraped, text='Page Scraped', fg="#C10ABA",
                bg="#F6F9FE", font=('roboto', 11, 'bold'),width=80)
    Page = Label(Scraped, textvariable=pageCounterTampil, fg="#C10ABA",
                bg="#F6F9FE", font=('roboto', 11, 'bold'),width=80, height=1)
    scrpd.pack()
    Data.pack()
    scrpdPage.pack()
    Page.pack()
    Scraped.place(x=50, y=245)


# untuk menampilkan Output File   
def select_file_output():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.csv')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename,
    )

# File Output Location
File = LabelFrame(text=" File Output ", font=('roboto', 11, 'bold'), bg="#F6F9FE")
Name = Label(File, text="File Output Name", fg="#C10ABA", bg="#F6F9FE", font=('roboto', 11, 'bold'), width=80)
Filebutton= Button(File, text="Open" ,bg="#442B71", fg="#FAFAFA", borderwidth=2, padx=19.4, pady=7, relief=RAISED, font= ("roboto", 12, "bold"), width =10, command=select_file_output)
Name.pack()
Filebutton.pack()
File.place(x=50, y=365)

main_window.mainloop()

def message():
    msgShow = messagebox.showinfo("CSV Ready", "File .csv dapat di download !")

def messageUrl():
    msgShow = messagebox.showinfo(
        "Insert URL", "Masukkan Link Tokopedia untuk di scrap")

def messageNotice():
    msgShow = messagebox.showinfo(
        "Info", "Tidak ada data untuk dikonversi ke CSV !")

def mssgUrlError():
    msgShow = messagebox.showinfo(
        "URL wrong", "Input URL tidak sesuai dengan format")

def messageWarning():
    msgShow = messagebox.showinfo(
        "Error", "File Location tidak ditemukan !  ")

def messageSccs():
    msgShow = messagebox.showinfo("Berhasil", "File CSV berhasil dikonversi !")

def messageStartClear():
    msgShow = messagebox.showinfo("Scrap direset", "Proses baru akan dimulai \n Hasil Scrap sebelum akan dihapus")

main_window.mainloop()

#:::::::::::::::::::::::::::::::::::::::::::::: END OF GUI Program :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# In[ ]: