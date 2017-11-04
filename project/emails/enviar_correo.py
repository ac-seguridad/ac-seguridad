# '''
#     Este archivo envía correos electrónicos a un usuario determinado utilizando
#     una conexión a los servidores SMTP de Gmail o Hotmail.
    
#     Docs: https://docs.python.org/3/library/email-examples.html
#           https://docs.python.org/3/library/smtplib.html?highlight=smtplib
# '''

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

#### CREACION DEL CORREO.
subject = 'Pa\' que veas que somos serios.'
content = 'Pal\' pato de Christian!'

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# with open(textfile) as fp:
#     # Create a text/plain message
#     msg = MIMEText(fp.read())
msg = MIMEText(content) # Crea un correo de tipo MIME/Text con las cabeceras y el contenido 'content'


me = 'acseguridad256@outlook.com' # quien lo manda.
you = 'anabelrincon9@gmail.com' # quien lo recibe
msg['Subject'] = subject # cabecera MIME que contiene el asunto.
msg['From'] = me # cabecera MIME de quien lo manda.
msg['To'] = you # cabecera MIME de quien lo recibe


# ENVIAR CORREO.
# gmail_user = 'acseguridad256@outlook.com'
gmail_user = 'ac.seguridad256@gmail.com'
gmail_pwd = 'Anabel94'

# https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
server = smtplib.SMTP("smtp.gmail.com", 587)
# server = smtplib.SMTP('smtp-mail.outlook.com', 587)
server.ehlo()
server.starttls() #Inicia el modo TLS transfer layer security - encriptar msg
server.ehlo() # the docs says we need to call this function again.
server.login(gmail_user, gmail_pwd)
# server.sendmail(FROM, TO, message)
server.send_message(msg)
server.close()
        
# Send the message via our own SMTP server.
# s = smtplib.SMTP('localhost')
# s.send_message(msg)
# s.quit()
