from django.shortcuts import render, redirect
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


import secrets, random, string, requests
from django.db import IntegrityError, transaction
from datetime import timedelta, datetime, timezone as dt_timezone
from django.utils import timezone

from threading import Thread

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from premailer import transform
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def UserRegisterView(request):

    if request.user.is_authenticated:

        return redirect("/")

    error = ""
    values = { "username": "", "email": "" }

    if request.method == "POST":
    
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        values["username"] = username
        values["email"]    = email

        # — Username validation —
        if not username:
            
            error = "Username is required."

            return render(request, "auth/user-register.html", {
                "errors": error,
                "values": values
            })

        # — Email validation —
        if not email:

            error = "Email is required."

            return render(request, "auth/user-register.html", {
                "errors": error,
                "values": values
            })

        else:
            try:
                validate_email(email)

            except ValidationError:
                error = "Enter a valid email address."

            else:
                if User.objects.filter(email=email).exists():
                    error = "An account with that email already exists."

        # — Password validation —
        if not password:
            error["password"] = "Password is required."

        else:
            if len(password) < 8:
                error = "Password Must Contain 8 characters"

        # — Confirm password —
        if password and password != confirm_password:
            
            error = "Passwords do not match."

        # If valid, create the user
        if not error:
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password
            )

            assign_otp(user=user)

            assign_verification_token(user=user)
            
            user.is_active = False

            email_thread = Thread(target=send_stylized_email,args=(user.email, "Verify Your Account", "auth/otp.html", {'username': user.username, 'otp':user.otp}))

            email_thread.start()

            request.session['verification_tok'] = user.verification_token

            return redirect("/authentication/verify-otp")

    return render(request, "auth/user-register.html", {
        "error": error,
        "values": values
    })




def UserOTPVerifyView(request):

    if "verification_tok" not in request.session:
        
        return redirect("signup")

    verf_tok = request.session["verification_tok"]
    user = User.objects.filter(verification_token=verf_tok).first()

    if not user:
        return redirect("signup")

    error = ""

    if request.method == "POST":

        input_otp = ''.join([
            request.POST.get(f'otp{i}', '') for i in range(1, 5)
        ])

        if not input_otp:

            error = "Please Enter OTP"

        elif input_otp != user.otp:

            error = "Incorrect OTP"

        elif user.otp_expiry and timezone.now() > user.otp_expiry:

            error = "OTP has expired."

        else:
            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()

            del request.session["verification_tok"]

            return redirect('/')

    return render(request, "auth/verify-user-otp.html", {
        "error": error,
    })




def UserLoginView(request):

    if request.user.is_authenticated:
        return redirect("/")  # already logged in

    error = ""
    email = ""

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        # Validation
        if not email:
            error = "Email is required."

        elif not password:
            error = "Password is required."

        else:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")  # or dashboard
                else:
                    error = "Your account is not activated. Please verify your email."
            else:
                error = "Invalid email or password."

    return render(request, "auth/user-login.html", {
        "error": error,
        "email": email
    })



@login_required(login_url='/authentication/user-login')
def UserLogoutView(request):

    logout(request=request)

    return redirect('/authentication/user-login')



def assign_verification_token(user : User):

    """
    Assigns User A Unique Verification Token
    """

    while True:

        generated_token = secrets.token_urlsafe(32)

        try:

            with transaction.atomic():

                user.verification_token = generated_token

                user.verification_token_expiry = timezone.now() + timedelta(minutes=5)

                user.save()

                return generated_token
            

        except IntegrityError:

            continue



def assign_otp(user : User):

    """
    Assigns User A Unique OTP
    """

    while True:

        generated_otp = "".join(random.choices(population=string.digits,k=4))

        try:

            with transaction.atomic():

                user.otp = generated_otp

                user.otp_expiry = timezone.now() + timedelta(minutes=5)

                user.save()

                break

        except IntegrityError:

            continue



def send_stylized_email(user_email : str , subject : str, template_name : str , arguments_for_template : dict):
    
    subject = subject

    message = "Email Failed To Send"

    # Render and transform the HTML email
    html_message = render_to_string(template_name, arguments_for_template)
    html_message = transform(html_message)  # Inline CSS

    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    
    email.content_subtype = 'html'
    email.body = html_message

    email.send()
