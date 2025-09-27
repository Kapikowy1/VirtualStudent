import os, json, re, traceback
from time import sleep

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import HttpResponse, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import permissions
from rest_framework.decorators import permission_classes

from django_q.tasks import async_task

from users.models import QueueInfo
from custom_config import (
    doc_path,
    fv_output_path,
    output_path,
    working_mode,
)

from .tasks import run_summary_task
from .user_token import account_activation_token

from unidecode import unidecode


User = get_user_model()


def check_user_validity(username, password, email):
    if username and password and email:
        # Username length validation
        if not (3 <= len(username) <= 15):
            raise ValueError(f"Username length must be between 3 and 15 characters. Current length: {len(username)}")
        
        # Username regex validation
        username_pattern = r'^[a-zA-Z0-9äöüÄÖÜéèÉÈáÁàÀçÇñÑ]+$'
        if not re.match(username_pattern, username):
            raise ValueError("Username can only contain digits, letters (a-z, A-Z), and European characters.")
        
        # Password length validation
        if not (6 <= len(password) <= 25):
            raise ValueError(f"Password length must be between 6 and 25 characters. Current length: {len(password)}")
        
        # Email length validation
        if not (5 <= len(email) <= 320):
            raise ValueError(f"Email length must be between 5 and 320 characters. Current length: {len(email)}")
        
        # Email regex validation
        email_pattern = r'^[a-zA-Z0-9äöüÄÖÜéèÉÈáÁàÀçÇñÑ._-]+@[a-zA-Z0-9äöüÄÖÜéèÉÈáÁàÀçÇñÑ.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format. Allowed characters: letters (a-z, A-Z), digits, European characters, and symbols: @ . _ -")  

def validate_input(topic, purpose):
    
    # Topic length validation
    if not (15 <= len(topic) <= 150):
        raise ValueError(f"Topic length must be between 15 and 150 characters. Current length: {len(topic)}")

    # Purpose length validation
    if not (20 <= len(purpose) <= 470):
        raise ValueError(f"Purpose length must be between 20 and 470 characters. Current length: {len(purpose)}")


def transform_input(topic, purpose):
    # Remove special characters and replace with spaces
    def clean_string(input_string):
        cleaned = re.sub(r'[^\w\s]', '', unidecode(input_string))  # Keep only alphanumeric characters and spaces
        return cleaned.strip()  # Remove leading/trailing spaces

    transformed_topic = clean_string(topic)
    transformed_purpose = clean_string(purpose)
    # print(transformed_purpose, transformed_topic)
    return {
        'transformed_topic': transformed_topic,
        'transformed_purpose': transformed_purpose
    }


def register_view(request):
    if request.user.is_anonymous:

        if request.method == 'POST':
            username = request.POST['username'].strip()
            password = request.POST['password'].strip()
            email = request.POST['email'].strip()
            is_consent_pop=request.POST['is_consent_pop'].strip()
            if is_consent_pop == "1":

                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    error_msg = "Użytkownik z takim e-mailem lub nazwą już istnieje" 
                    return render(request, 'users/register.html', {'error_msg': error_msg})
                
                user={}
                
                try:
                    check_user_validity(username, password, email)

                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        is_active=True,
                        is_consent_pop=True)

                    user.save()
                    current_site=get_current_site(request)
                    message = render_to_string('emailTemplates/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                    })

                    emailObject = EmailMessage(
                        'Link aktywacyjny został wysłany na Twoją skrzynkę pocztową',
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email]
                    )
                    emailObject.content_subtype = 'html'

                    # emailObject.send() - wymaga skonfigurowania odpowiednio usługi dostarczającej emaile.

                    return render(request, 'users/login.html', {'error_msg': 'Pomyślnie zarejestrowano. Aplikacja w trybie developerskim - brak emaila weryfikacyjnego. Konto zostalo aktywowane.'})
                except ValueError as ve:
                    error_msg = str(ve)
                    print(ve)
                    return render(request, 'users/register.html',{'error_msg': ve})
                except Exception as e:

                    error_msg = str(e)
                    traceback.print_exc()
                    if(user):
                        user.delete()
                    return render(request, 'users/register.html',{'error_msg': 'Nie udało się zarejestrować. Spróbuj ponownie'})
            else:
                return render(request, 'users/register.html',{'error_msg': 'W celu rejestracji potwierdź zgode na przetwarzanie danych osobowych'})
        else:
            print("request method is not post")
            return render(request, 'users/register.html',{'error_msg': ''})
    else:
        print("user is not annonymous")
        username=request.user
        return render(request, 'users/dashboard.html',{'username':username,'error_msg': ''})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        messages.success(request, f'Witaj {user.username}')
        return redirect('user_board')
    else:
        return HttpResponse('Link aktywacyjny przestał być aktywny lub jest niepoprawny')


@permission_classes([permissions.AllowAny])
def login_view(request):
    if request.user.is_anonymous:
        return render(request, 'users/login.html',{'error_msg': ''})
    else:
        username=request.user
        return render(request, 'users/dashboard.html',{'username':username,'error_msg': ''})


@permission_classes([permissions.AllowAny])
def login_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is None:
                error_msg = "Taki użytkownik nie istnieje"
                return render(request, 'users/login.html', {'error_msg': error_msg})

            if user and not user.is_active:
                error_msg = "Twoje konto jest nieaktywne"
                return render(request, 'users/login.html', {'error_msg': error_msg})

            user = authenticate(request, username=username, password=password)
            request.session["username"] = username
            if user is not None:
                login(request, user)
                messages.success(request, f'Login Success {username}')
                return redirect('user_board')
            else:
                error_msg = "Błędne hasło lub nazwa użytkownika"
                return render(request, 'users/login.html', {'error_msg': error_msg})

        except SuspiciousOperation:
            # Handle the case where the session was deleted
            error_msg = "Wystąpił problem z sesją. Spróbuj ponownie."
            return render(request, 'users/login.html', {'error_msg': error_msg})

    else:
        error_msg = "Logowanie zakończone niepowodzeniem"
        return render(request, 'users/login.html', {'error_msg': error_msg})

@login_required
def logout_auth(request):
    try:
        auth.logout(request)
        return render(request, 'users/login.html',{'error_msg': ''})
    except:
        error_msg = "Nie udało się wylogować"
        return render(request, 'users/login.html', {'error_msg': error_msg})



folder_name = 'python_language_model'
folder_name2 = 'MVP'

@login_required
def generation_view(request):

    currentUsername = request.session.get('username') or request.user.username

    user = User.objects.get(username=currentUsername)


    if request.method == 'POST':

        try:
            purpose = request.POST.get('purpose')
            topic = request.POST.get('topic')
            request.session['topic'] = topic
            request.session['purpose'] = purpose
            try:
                no_special_signs=transform_input(topic,purpose)

                saveFileToPath(output_path, no_special_signs)
                saveFileToPath(fv_output_path, no_special_signs)

            except Exception as e:
                print("error during saving output.txt",e)

            return redirect('generation_view')
        except Exception as e:
            print("Error in saving data to output txt",e)

            return redirect('home_view')
    topic = request.session.get('topic')
    purpose = request.session.get('purpose')
    return render(request, 'users/generationView.html',{"topic":topic,"purpose":purpose,'error_msg': 'Zapisano temat i cel'})


def saveFileToPath(path, no_special_signs):
    with open(path, 'w') as file:
        file.write(f"Purpose: {no_special_signs['transformed_purpose']}\n")
        file.write(f"Topic: {no_special_signs['transformed_topic']}\n")

@login_required
def generation_view_file(request):

    return render(request, 'users/generationViewFile.html',{'error_msg': ''})

@login_required
def refresh_generation_view_file(request):
    queue=checkSpotInQueue()

    return redirect(f'/generation-view-file/?{queue}')
    #return render(request, 'users/generationViewFile.html',{'error_msg': '','spot_in_queue':queue['spot_in_queue'],"estimated_time":queue["estimated_time"]})


@login_required
def send_test_email(request):

    message = render_to_string('emailTemplates/demo_bachelor_email.html', {
        'user': "test",
        'domain': "test",
        'uid': "test",
    })


    email=request.user.email
    email_object = EmailMessage(
        'Gratulacje! Twoja praca została wygenerowana. Korzystaj śmiało ze swojej inspiracji !',
        message,
        settings.DEFAULT_FROM_EMAIL, 
        [email]
    )

    email_object.content_subtype = "html"
    email_object.attach_file('Generuj prosze mordo.docx')
    # file_path = os.path.join('Dane', 'dokumenty', topic)
    email_object.send()

    return render(request, 'users/dashboard.html')




def sendErrorMail(request,error_msg):
    send_mail(
            'Error in Django Application',
            error_msg,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )


@login_required
def generateBachelor(request):
    check_duplicates=False
    if request.method == "POST":

        check_duplicate = request.POST.get("check_duplicate", "0")  # Domyślnie 0, jeśli brak klucza
        check_duplicates=check_duplicate == "1"

    return process_bachelor_request(request, check_duplicates, is_full_version=False)


@login_required
def genFullVersion(request):
    check_duplicates=False

    if request.method == "POST":
        check_duplicate = request.POST.get("check_duplicate", "0")  # Domyślnie 0, jeśli brak klucza
        check_duplicates=check_duplicate == "1"

    return process_bachelor_request(request, check_duplicates, is_full_version=True)


@login_required
def process_bachelor_request(request, check_duplicates, is_full_version):
    try:

        current_site = str(get_current_site(request))

        currentUsername = request.session.get('username') or request.user.username
        currentUser = User.objects.get(username=currentUsername)
        generation_quantity = currentUser.generation_quantity
        full_generation_quantity= currentUser.full_generation_quantity

        topic = request.session.get('topic')
        purpose = request.session.get('purpose')

        no_special_signs = transform_input(topic, purpose)

        if generation_quantity > 0 or (is_full_version and full_generation_quantity > 0 ):
            if is_full_version:
                currentUser.full_generation_quantity -= 1
                currentUser.save()
            else:
                currentUser.generation_quantity -= 1
                currentUser.save()

            if check_duplicates and doesTopicExists(topic):
                error_msg = "Duplikat tematu jest już w bazie"
                return render(request, 'users/generationView.html', {"topic": topic, "purpose": purpose, 'error_msg': error_msg})

            saveTopicToList(topic)
            queue = checkSpotInQueue()

            try:
                validate_input(topic, purpose)
                sleep(1)

                async_task(run_summary_task, currentUser.id, is_full_version, current_site, no_special_signs['transformed_topic'])
                
            except ValueError as ve:
                print(f"Input validation error: {ve}")

                if is_full_version:
                    currentUser.full_generation_quantity += 1
                    currentUser.save()
                else:
                    currentUser.generation_quantity += 1
                    currentUser.save()

                return render(request, 'users/dashboard.html', {'error_msg': ve})
            except Exception as e:
                print(e)

            return redirect(f'/generation-view-file/?{queue}')

        else:
            error_msg = "Twoje darmowe projekty się skończyły. Dzięki, że wypróbowałeś naszą aplikację!"
            return render(request, 'users/dashboard.html', {'error_msg': error_msg})

    except Exception as e:
        error_msg = str(e)
        return render(request, 'users/dashboard.html', {'error_msg': error_msg})





def checkSpotInQueue():

    pending_queue = QueueInfo.objects.filter(status='pending')

    task_number = pending_queue.count()

    if task_number > 0:
        spotInQueue = max(task_number - 3, 1)
        
    
        if task_number > 4:
         
            estimatedTime = 8
         
            for i in range(5, task_number + 1):
            
                if i % 4 == 1:
                    estimatedTime += 5  
                elif i % 4 == 0:
                    estimatedTime += 1  
                else:
                    continue 
        else:
           
            estimatedTime = (5 * spotInQueue) + (1 * (task_number - 1))
    else:
        spotInQueue = 1
        estimatedTime = 5

    return {
        'spot_in_queue': spotInQueue,
        'estimated_time': estimatedTime
    }

def sendEmailWithBachelor(request):

    #wyłączone na potrzeby prezentacji
    return 

    current_site = get_current_site(request)

    message = render_to_string('emailTemplates/demo_bachelor_email.html', {
        'user': request.user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
    })
    topic = request.session.get('topic')

    email_object = EmailMessage(
        'Wygenerowano projekt',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email]
    )

    sub_path = f"{topic}.docx"
    file_production_path = os.path.join(doc_path, sub_path)


    if os.path.exists(file_production_path):
        print("file exists")
        email_object.attach_file(file_production_path)
    else:
        print(f"File '{file_production_path}' not found. Attachment skipped.")

    try:
        email_object.send()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")




def readFile(request):
    print(output_path)
    purpose_lines = []
    topic_lines = []

    try:
        with open(output_path, 'r') as file:
            for line in file:
                if 'Purpose:' in line:
                    purpose_lines.append(line.strip())
                elif 'Topic:' in line:
                    topic_lines.append(line.strip())

    except Exception as e:
        print("Error reading file:", str(e))

    return render(request, 'users/generationView.html', {
        'purpose_lines': purpose_lines,
        "topic_lines": topic_lines
    })



def generationViewEmpty(request):
    someString = "Hello, World!" 
    return render(request, 'users/generationView.html', {"somestring": someString})




#static render_html_page

def home(request):
    return render(request, 'users/home.html',{'error_msg': ''})


def cooperation_view(request):
    return render(request, 'users/cooperation.html',{'error_msg': ''})

@login_required
def dashboard(request):
    topic = request.session.get('topic')
    purpose=  request.session.get('purpose')
    
    if topic and purpose:
        return render(request, 'users/dashboard.html',{"topic": topic, "purpose": purpose, 'error_msg': ''})
    else:
        return render(request, 'users/dashboard.html',{'error_msg': ''})



def creators_view(request):
    return render(request, 'users/login.html',{'error_msg': ''})
    return render(request, 'users/creators.html')


def user_board(request):
    try:
        username = request.session.get('username', 'someUser')
    except Exception as e:
        print(e)

    return render(request, 'users/dashboard.html', {'username': username,'error_msg': ''})




def terms_of_use_view(request):
    return render(request, 'users/termsOfUse.html',{'error_msg': ''})



def bachelors_store(request):
    topic_list_MVP = ['topic1MVP', 'topic2MVP', 'topic3MVP']
    topic_list_full = ['topic1full', 'topic2full', 'topic3full']
    request.session['topic_list_MVP'] = topic_list_MVP
    request.session['topic_list_full'] = topic_list_full

    return render(request, 'users/bachelorsStore.html', {
        'error_msg': '',
        'topic_list_MVP': topic_list_MVP,
        'topic_list_full': topic_list_full
    })

def download_full(request):
    # Pobieranie list z sesji
    topic_list_full = request.session.get('topic_list_full', [])
    
    if request.method == 'POST':
        name = request.POST.get('download_full_hidden', 'nieznany dokument')
        print(name)
        error_msg = f'Udało się pobrać dokument full: {name}'
    else:
        error_msg = 'Nie udało się pobrać dokumentu.'

    return render(request, 'users/bachelorsStore.html', {
        'error_msg': error_msg,
        'topic_list_MVP': request.session.get('topic_list_MVP', []),
        'topic_list_full': topic_list_full
    })

def download_MVP(request):
    # Pobieranie list z sesji
    topic_list_MVP = request.session.get('topic_list_MVP', [])

    if request.method == 'POST':
        name = request.POST.get('download_MVP_hidden', 'nieznany dokument')
        print(name)
        error_msg = f'Udało się pobrać dokument MVP: {name}'
    else:
        error_msg = 'Nie udało się pobrać dokumentu.'

    return render(request, 'users/bachelorsStore.html', {
        'error_msg': error_msg,
        'topic_list_MVP': topic_list_MVP,
        'topic_list_full': request.session.get('topic_list_full', [])
    })



def saveTopicToList(topic):
    try:
        data = {}
         
        json_path = doc_path + 'topicList.json'

        if os.path.exists(json_path):
            # Load the existing data
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

        topic_lower = topic.lower()

        if any(str(topic_lower) == str(value).lower() for value in data.values()):
            return
        else:
            data_key = f"{len(data) + 1}"
            data[data_key] = topic

            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    except Exception as e:
        print(e)


def doesTopicExists(topic):
    try:
        data = {}

        json_path = doc_path + 'topicList.json'

        if os.path.exists(json_path):
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

        topic_lower = topic.lower()

        if any(str(topic_lower) == str(value).lower() for value in data.values()):
            print('This topic already is in json')
            return True
        else:
            print('Topic is not on json')
            return False

    except Exception as e:
        print(e)
        return True

