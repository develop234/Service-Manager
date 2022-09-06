import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform as p

os_details ='Pleae find the OS details below: \n\n' \
            'System:  ' + p.system() +'\n' + \
            'Node:    ' + p.node() +'\n' + \
            'Version: ' + p.version()+'\n' + \
            'Machine: ' + p.machine()+'\n' + \
            'Python:  ' + p.python_version() +'\n\n' + \
            'Regards'+'\n' + \
            'Automation Team'

#The mail addresses and password
sender_address       = 'rameshvp.sss@TestSarp.com'
sender_pass          = 'tceaglgaawiczxov' #This is enc password and watch video to generate enc pwd https://www.google.com/search?q=google+does+not+support+less+secure+apps&oq=google+does+not+support+&aqs=chrome.1.0i512l2j69i57j0i22i30l7.5062j0j4&sourceid=chrome&ie=UTF-8#kpvalbx=_txIMY5njH8HWz7sPsuy-wAM14
receiver_address     = 'rameshvp.sss@sarptest123.com'

#Setup the MIME
message = MIMEMultipart()
message['From']      = sender_address
message['To']        = receiver_address
message['Subject']   = 'Automated system details' #The subject line
mail_content         = os_details

message.attach(MIMEText(mail_content, 'plain'))

#Create SMTP session for sending the mail
try:
    session = smtplib.SMTP('smtp.TestSarp.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print ('Email is sent successfully')

except Exception as Err:
    print('Failed to send email due to',Err)
