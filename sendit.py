#! /usr/bin/env python 
import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.ehlo()
smtpObj.login('xxmrmau5@gmail.com','') 
smtpObj.sendmail('xxmrmau5@gmail.com','xxmrmau5@gmail.com','')
