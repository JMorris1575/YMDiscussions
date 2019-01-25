from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.http import is_safe_url

from config.settings.base import get_secret

import utilities

def convert_tags(subject, message, user):
    """
    Converts the following tags in the message or subject line of an e-mail to their equivalent for the given user:
    [first] = first name
    [last] = last name
    [full] = full name
    [user] = username
    [pwrd] = password
    :param subject: string containing the subject line to be sent
    :param message: string containing the message to be sent
    :param user: User object containing data for the given user
    :return: a subject string and message string with all the tags filled in
    """
    user_info = {'[first]':user.first_name,
                 '[last]': user.last_name,
                 '[full]': user.get_full_name(),
                 '[user]': user.username,
                 '[pwd]': get_secret(user.username.upper())}
    for tag in user_info.keys():
        subject = subject.replace(tag, user_info[tag])
        message = message.replace(tag, user_info[tag])

    return subject, message


class SendMail(View):
    template_name = 'mail/send-mail.html'

    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST['button'] == 'send':
            recipients = list(set(request.POST.getlist('recipients')))
            subject_template = request.POST['subject']
            message_template = request.POST['message']
            for recipient in recipients:
                print('recipient = ', recipient)
                member = User.objects.get(username=recipient)
                email_list = [member.email]
                subject, message = convert_tags(subject_template, message_template, member)
                send_mail(subject, message,
                          'FrJim@ymdisc.jmorris.webfactional.com',
                          email_list, fail_silently=False)

        return redirect('activity:welcome')