import logging
logger = logging.getLogger(__name__)

from pykeepass import PyKeePass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail(
        l_to,
        s_header,
        s_body,
        s_footer,
        s_subject,
        s_accountname='hotmail_martienstam',
        s_key_file='passworddb//id_rsa.pub'
        ):

    logger.info('Start send mail')

    kp = PyKeePass('passworddb//Passwords.kdbx', password=None, keyfile=s_key_file)
    secret=kp.find_entries(title=s_accountname, first=True)

    #The mail addresses and password
    sender_address = secret.username
    sender_pass = secret.password
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ', '.join(l_to)
    message['Subject'] = s_subject
    #The body and the attachments for the mail
    message.attach(MIMEText(s_header, 'plain'))
    message.attach(MIMEText(s_body, 'html'))
    message.attach(MIMEText(s_footer, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.live.com",587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, l_to, text)
    session.quit()

    logger.info('End send mail')
    
    return True