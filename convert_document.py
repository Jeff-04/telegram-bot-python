# TELEGRAM BOT
# Library : pip install pyTelegramBotAPI / pillow

import telebot
import pdf2docx
from telebot.apihelper import download_file
import requests
from io import BytesIO
from PyPDF2 import PdfFileWriter
import cv2
import pyqrcode

def read_qr_code(filename):

    try:
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return
    
def make_qr_code(data):
    try:
        url = pyqrcode.create(data)
        url.png('QrCode.png', scale = 6)
        return True
    
    except Exception as e:
        return False

def convert_document(document_inp, document_out):
    if '.docx' in document_inp:
        try:
            file = open(document_inp, 'rb')
            word_file = BytesIO(file.read())

            pdf_file = open(document_out, 'wb')
            pdf_writer = PdfFileWriter()
            pdf_writer.write(pdf_file)
            file.close()
            pdf_file.close()
            return True
        except Exception as e:
            print(e)
            return False

    elif '.pdf' in document_inp:
        print("pdf")
        try:
            file = pdf2docx.Converter(document_inp)
            file.convert(document_out)
            return True
        except Exception as e:
            print(e)
            return False


def downloadfile(token, id, nama):
    # Download the file and save it to the current directory
    try:
        response = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, id))
        path = 'document/{}'.format(nama)
        open(path, "wb").write(response.content)
        return True

    except Exception as e:
        print(e)
        return False

# Inisialisasi bot
bot = telebot.TeleBot("5779756895:AAG49MwwxEuXShao-Lr5KBXiPTnDtDs-neY")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.content_type == 'text':
        help = ['help', 'Help', '/help', '/Help', 'start', '/Start', '/start']
        qrkey2img = ['/key2qr', '/KEY2QR', '/Key2qr']
        myres = [ele for ele in qrkey2img if(ele in message.text)]
        print(myres)
        if message.text in help:
            text = """
            Selamat datang di bot saya :)
Bot ini bisa digunakan untuk :
1. Konversi file (pdf -> word, word -> pdf)
2 ..
3 ..

Keyword :
1. help / start
2. konversi word ke pdf (/word2pdf)
3. konversi pdf ke word (/pdf2word)
           """
            bot.reply_to(message, text)
        
        elif myres:
            bot.reply_to(message, 'Tunggu sebentar ..')
            text = str(message.text).split()
            bot.reply_to(message, 'Key yang akan di generate : {}'.format(str(text[1])))
            qr = make_qr_code(text[1])
            
            if qr == True:
                with open('QrCode.png', 'rb') as img:
                    bot.send_photo(message.chat.id, img)
            
            else:
                bot.send_message(message.chat.id, 'Gagal')

        else :
            bot.send_message(message.chat.id, 'keyword eror')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    word2pdfkey = ['/word2pdf', '/WORD2PDF', '/Word2pdf']
    pdf2word = ['/pdf2word', '/PDF2WORD', '/Pdf2word']
    if message.caption in word2pdfkey:
        bot.reply_to(message, "Tunggu sebentar ..")
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        path = 'document/{}'.format(file_name)
        download = downloadfile("5779756895:AAG49MwwxEuXShao-Lr5KBXiPTnDtDs-neY", file_info.file_path, file_name)
        if download == True:
            print("path word :{}\npath Convert : {}".format(path, path.replace('docx', 'pdf')))
            convert = convert_document(path, path.replace('docx', 'pdf'))
            if convert == True:
                open_pdf = 'document/{}'.format(file_name.replace('docx', 'pdf'))
                with open(open_pdf, 'rb') as document:
                    bot.send_document(message.chat.id, document)
            else:
                bot.reply_to(message, 'Document gagal !') 
        else:
            bot.reply_to(message, 'Document gagal download !')
    
    elif message.caption in pdf2word:
        bot.reply_to(message, "Tunggu sebentar ..")
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        path = 'document/{}'.format(file_name)
        download = downloadfile("5779756895:AAG49MwwxEuXShao-Lr5KBXiPTnDtDs-neY", file_info.file_path, file_name)
        if download == True:
            convert = convert_document(path, path.replace('pdf', 'docx'))
            print("CONVERT : {}".format(convert))
            if convert == True:
                open_pdf = 'document/{}'.format(file_name.replace('pdf', 'docx'))
                with open(open_pdf, 'rb') as document:
                    bot.send_document(message.chat.id, document)
            else:
                bot.reply_to(message, 'Document gagal !') 
        else:
            bot.reply_to(message, 'Document gagal download !')

    else:
        bot.reply_to(message, 'keyword salah !')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    img = False
    qrimg2key = ['/qr2key', '/QR2KEY', '/Qr2key']
    if message.caption in qrimg2key:
        bot.reply_to(message, 'Tunggu Sebentar ..')
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
            img = True
        
        if img == True:
            value = read_qr_code('image.jpg')
            bot.send_message(message.chat.id, value)

print("Bot Running")
bot.polling()
