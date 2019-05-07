import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_email(to, subject, text): 
    fromaddr = "Your email"
    toaddr = to
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
 
    body = text
    msg.attach(MIMEText(body, 'plain'))
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Enter your password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def send_confirmation_email(user_email,user_name, confirmation_key):
    send_email(user_email, "Welcome to The Auction",
"""Hello {}!, and thanks for registering with {}!
We are really happy that you choose to be a part of our site
Your account is created, now you can host auctions

Regards
Team 0|1
Founder & Creator
prakhark19@gmail.com""".format(user_name,"The Auction ", confirmation_key))



def send_welcome_email(user_email, user_name, provider):
    send_email(user_email, "Welcome To The Auction", 
        """Hey {} 
I would like to take the opportunity of thanking you for signing up on our platform using your {} credentials.
There are a lot of things for you to explore so I suggest you get right on them :)
Once again welcome aboard sailor!

It was awesome talking to you!
Happy Biddin!

Regards
Team 0|1
System Admin
(prakhark19@gmail.com)""".format(user_name, provider))

def send_reset_email(email, name, conf_key):
    send_email(email, "You requested for a new password!","""
Hey {}!
We see that you requested for your password to be changed!
Please click the below link for changing your password:
righ now not working


Please note that the above link is valid only for one time use""".format(name))


def is_valid_email(email):

	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return 1
	return 0
