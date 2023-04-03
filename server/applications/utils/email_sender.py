from distutils.command.install_egg_info import to_filename
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class EmailSender:
    def __init__(self, from_email, to, subject, context, template):
        self.to = to
        self.from_email = from_email
        self.context = context
        self.template = template
        self.subject = subject

    def send_mail(self):
        template = get_template(self.template).render(self.context)
        msg = EmailMultiAlternatives(
            self.subject,
            None,
            self.from_email,
            self.to
        )
        msg.attach_alternative(template, "text/html")
        msg.send(fail_silently=False)
