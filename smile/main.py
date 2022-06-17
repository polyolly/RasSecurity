# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 16:08:59 2021

@author: Anpoint
"""




import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os



import cv2

cap = cv2.VideoCapture(-1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
while True:
    _, frame = cap.read()
    original_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    photo_taken = False
    for x, y, w, h in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        face_roi = frame[y:y+h, x:x+w]
        gray_roi = gray[y:y+h, x:x+w]
        smile = smile_cascade.detectMultiScale(gray_roi, 1.3, 25)
        for x1, y1, w1, h1 in smile:
            cv2.rectangle(face_roi, (x1, y1), (x1+w1, y1+h1), (0, 0, 255), 2)
            cv2.imwrite('sel.png',original_frame )
            mail_content = '''Thank for smiling~
'''
#The mail addresses and password
            sender_address = 'leafgreen714@gmail.com'
            sender_pass = 'oeotjzyjchjhssey'
            receiver_address = 'polyolly8099@gmail.com'
#Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Your Smile has been sent.'
#The subject line
#The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            for imageName in os.listdir('/home/pi/smile'):
                if imageName.endswith('jifif'):
                    print(imageName)

    
            attachName='/home/pi/smile/sel.png'
            attach_file_name = attachName


            attach_file = open(attach_file_name, "rb") # Open the file as binary mode
            payload = MIMEBase('image', 'png')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
#Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Sent')
            
    cv2.imshow('cam star', frame)    
    if cv2.waitKey(10) == ord('q'):
    #
        cv2.destroyAllWindows();
        break
    



        
