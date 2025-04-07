import random
import smtplib

user_db = {}  

def send_otp(email):
    otp = str(random.randint(1000, 9999))
    user_db[email] = otp

    sender_email = "smart.carrer.prep25@gmail.com"
    sender_password = "rxyi vtlp pxtf ahqs"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = f"Subject: Your OTP Code\n\nYour OTP is: {otp}"
        server.sendmail(sender_email, email, message)
        server.quit()

        return True  
    except Exception as e:
        print("Error sending email:", e)
        return False  
def verify_otp(email, entered_otp):
    return email in user_db and user_db[email] == entered_otp
