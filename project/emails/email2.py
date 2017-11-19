import sys
import os

import django
sys.path.append('/home/ubuntu/workspace/project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
django.setup()

# from django.core.mail import send_mail

# # text = fp.getvalue()

# EMAIL_USE_TLS='TRUE'
# EMAIL_HOST='smtp.gmail.com'
# EMAIL_HOST_USER ='ac.seguridad256@gmail.com'
# EMAIL_HOST_PASSWORD = 'Anabel94'
# EMAIL_PORT=587


# subject= 'Probando anabel1'
# message= '1'
# recipient_list= 'ac.seguridad256@gmail.com'
# auth_user='ac.seguridad256@gmail.com'
# auth_password='Anabel94'

# send_mail(
#     '1',
#     'Here is the message.',
#     'ac.seguridad256@gmail.com',
#     ['ac.seguridad256@gmail.com'],
#     fail_silently=False,)

from django.core.mail import EmailMessage
email = EmailMessage('Test', 'Test', to=['anaberincon9@gmail.com'])
email.send()



