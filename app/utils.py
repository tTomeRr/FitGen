from flask import redirect, url_for, flash
import os
import smtplib


def send_mail(name, email, phone, message):
    gmail_user = os.getenv('GMAIL_USERNAME')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    sent_from = gmail_user
    to = [gmail_user]
    subject = f'Message from: Name- {name} Email- {email}, Phone- {phone}'
    body = message

    email_text = f"""From: {sent_from}\nTo: {", ".join(to)}\nSubject: {subject}\n\n{body}"""

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        flash("Thanks for reaching us. Your message has been sent!")


    except Exception as e:
        flash(f'Something went wrong')
        print(e)

    return redirect(url_for('main.index'))
