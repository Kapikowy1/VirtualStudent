
from django.core.mail import send_mail


import os, subprocess, json, time
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from celery import shared_task
from django.core.mail import EmailMessage
from custom_config import working_mode, full_version_summary_path, summary_path
from .models import QueueInfo

User = get_user_model()


from django.conf import settings

@shared_task
def run_summary_task(user_id, is_full_version, current_site, topic):

    try:
        user = User.objects.get(id=user_id)
        new_queue_info = QueueInfo(status='pending', topic=topic)
        new_queue_info.save()
        if user :
            if working_mode=="dev":
                print('wersja developerska nie trzeba uruchamiac wirtualnego srodowiska')
            else:
                activate_this = '/home/username/.virtualenvs/venv/bin/activate_this.py' #TODO: podmienic na swojego uzytkownika
                exec(open(activate_this).read(), {'__file__': activate_this})
            print("task status pending")
     
            if not new_queue_info.id:
                raise ValueError("Failed to create a QueueInfo record.")
            #time.sleep(30)
            if is_full_version:
                summaryFV = ['python', full_version_summary_path]
                subprocess.run(summaryFV, capture_output=True, text=True, check=True, env=os.environ)
            else:
                summaryRun = ['python', summary_path]
                subprocess.run(summaryRun, capture_output=True, text=True, check=True, env=os.environ)

            sendEmailWithBachelor(user.email, current_site,user.id, topic)

            print("success status resolved")
            new_queue_info.status = 'resolved'
            new_queue_info.save()

            print("task status resolved success")
        else:

            print("task status failed")
            new_queue_info.status = 'failed'
            new_queue_info.save()


    except subprocess.CalledProcessError as e:
        new_queue_info.status = 'failed'
        new_queue_info.save()

        #jezeli proces generacji rzucil bledem zwraca userowi generacje
        if is_full_version:
            user.full_generation_quantity = max(0, user.full_generation_quantity + 1)
            user.save()
        else:
            user.generation_quantity = max(0, user.generation_quantity + 1)
            user.save()

        error_message = f"Error message: {e.stderr} {e}"
        print(user.email,error_message)
        if working_mode=="dev":
            sendErrorMail(user.email, error_message)
        else:
            log_error(user.email,error_message)
            sendErrorMail(user.email, "Wystąpił błąd podczas generowania pliku. W razie pytań prosimy o kontakt na adres e-mail, z którego otrzymałeś wiadomość.")




def sendEmailWithBachelor(email,current_site,id,topic):

    user = User.objects.get(id=id)
    message = render_to_string('emailTemplates/demo_bachelor_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(id)),
    })



    email_object = EmailMessage(
        'Gratulacje! Twoja praca została wygenerowana. Korzystaj śmiało ze swojej inspiracji !',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )

    sub_path = f"{topic}.docx"
    file_production_path = os.path.join(sub_path)

    if os.path.isfile(file_production_path):
        print("file exists")
        email_object.attach_file(file_production_path)
    else:
        print(f"File '{file_production_path}' not found. Attachment skipped.")

    # Send email
    try:
        email_object.content_subtype = "html"
        email_object.send()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def sendErrorMail(email,error_message):
    send_mail(
                'Błąd podczas generowania projektu',
                error_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )


def log_error(user_email, error_message):
    json_file_path='error_log.json'

    if working_mode=="dev":
        json_file_path='error_log.json'
    else:
        json_file_path='error_log_production.json'

    if len(error_message) > 500:
        error_message = error_message[-500:]

    error_details = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_email': user_email,
        'error_message': error_message
    }
    
    if os.path.exists(json_file_path):
        print("saving error to the log")
        with open(json_file_path, 'r') as file:
            error_log = json.load(file)
    else:
        print("cannot save error")
        error_log = {}

    next_index = len(error_log)

    error_log[next_index] = error_details

    with open(json_file_path, 'w') as file:
        json.dump(error_log, file, indent=4)