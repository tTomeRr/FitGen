from flask import redirect, url_for, flash
import os
import smtplib
from openai import OpenAI
import ast

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

def generate_ai_workout(duration, fitness_level, fitness_goal, equipment_access, running_type):

    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Create a workout plan with only the workout name and details based on these criteria:\n"
                    f"- Workout Duration: '{duration} minutes'\n- Fitness Level: '{fitness_level}'\n- "
                    f"Fitness Goal: '{fitness_goal}'\n- Equipment Access: '{equipment_access}'\n- Running Type: '{running_type}'\n\n"
                    "Format:\n{\n  'workout_name': 'Name of the workout',\n  "
                    "'workout_details': [('Exercise Name', 'Description', Sets, Repetitions, 'Rest Time in minutes'), ...]\n}\n"
                    "Note: Provide the response in this exact format, without any additional text.\n"
                    "Provide a workout name that reflects the workout's focus and goal, e.g., 'Intense Cardio Circuit' or 'Beginners Full-Body Strength. with no punctuation marks"
                )
            }
        ]
    )

    workout_output = completion.choices[0].message.content
    workout_output = workout_output.replace("'", '"')

    return ast.literal_eval(workout_output)
