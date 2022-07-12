import decimal
import json
import requests

from django.db import transaction
from django.db.models import Sum

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import request

from .models import *

User = settings.AUTH_USER_MODEL


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#
# @receiver(post_save, sender=User, dispatch_uid='save_complaint')
# def save_complaint(sender, instance, created, raw=False, **kwargs):


@receiver(post_save, sender=User, dispatch_uid='save_staff')
def save_staff(sender, instance, created, raw=False, **kwargs):
    if created and instance.title == "complaint":
        Complainant.objects.create(user=instance)
    else:
        try:
            if created and instance.is_superuser is False:
                if not instance.title == "complaint":
                    URL = 'https://apisms.beem.africa/v1/send'
                    api_key = '2799f1a807695012'
                    secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
                    content_type = 'application/json'
                    source_addr = 'INFO'
                    apikey_and_apisecret = api_key + ':' + secret_key

                    '''Get name and concatenate them'''
                    first_name = instance.first_name
                    password = instance.last_name.upper()
                    last_name = instance.last_name
                    title = instance.title
                    username = instance.username

                    full_name = f"{first_name} {last_name}"

                    '''Get phone detail and convert and user id as recipient_id on api'''
                    # number= "255755422199"
                    phone = str(instance.phone)
                    # phone = str(number)
                    phone = phone[1:10]
                    # phone = phone
                    phone = '255' + phone

                    user_id = instance.id

                    message_body = f"Hello, {full_name}, \nyou have been successful registered on the police system as {title}" \
                                   f"\nyou can access the system via\n" \
                                   f"https://crms-police.herokuapp.com/" \
                                   f"\nUsername:{username},\nPassword:{password} "

                    print(message_body)
                    first_request = requests.post(url=URL, data=json.dumps({
                        'source_addr': source_addr,
                        'schedule_time': '',
                        'encoding': '0',
                        'message': message_body,
                        'recipients': [
                            {
                                'recipient_id': user_id,
                                'dest_addr': phone,
                            },
                        ],
                    }),

                                                  headers={
                                                      'Content-Type': content_type,
                                                      'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                                  },

                                                  auth=(api_key, secret_key), verify=False)

                    print(first_request.status_code)
                    if first_request.status_code == 200:
                        full_name = ''
                        phone = ''
                    print(first_request.json())


        except:
            pass


@receiver(post_save, sender=Case, dispatch_uid='generate_the_rb')
def generate_rb(sender, instance, created, raw=False, **kwargs):
    if created:
        get_station = instance.registerer.station.name.upper()
        get_station_first = get_station[:3]
        get_district = instance.registerer.station.district.name.upper()
        get_district_first = get_district[:3]
        get_code = instance.complainant.code
        get_number = id_generator()
        get_rb_string = f"{get_district_first}/{get_station_first}/{get_code}/{get_number}"

        get_case = Case.objects.get(id=instance.id)
        get_case.rb = get_rb_string
        save_case = get_case.save()
        import datetime

        get_date = datetime.date.today()
        add_record_to_chart = Chart.objects.create(complaint=instance.complainant, crime=instance.crime,
                                                   start_date=get_date)

        URL = 'https://apisms.beem.africa/v1/send'
        api_key = '2799f1a807695012'
        secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
        content_type = 'application/json'
        source_addr = 'INFO'
        apikey_and_apisecret = api_key + ':' + secret_key

        '''Get name and concatenate them'''
        code = instance.complainant.code
        # rb = instance.rb
        full_name = f"{code}"

        '''Get amount invested and daily amount earning'''

        '''Get phone detail and convert and user id as recipient_id on api'''
        # number= "255755422199"
        phone = str(instance.complainant.user.phone)
        # phone = str(number)
        phone = phone[1:10]
        # phone = phone
        phone = '255' + phone

        user_id = instance.complainant.user.id

        message_body = f"Hello: {full_name}, \nyour case was successfully registered with RB:\n {get_rb_string}" \
                       f"\nyou can dial *384*654444# to keep track" \
                       f"of the RB\n or visit \n https://crms-police.herokuapp.com/\n" \
                       f"for more information"

        first_request = requests.post(url=URL, data=json.dumps({
            'source_addr': source_addr,
            'schedule_time': '',
            'encoding': '0',
            'message': message_body,
            'recipients': [
                {
                    'recipient_id': user_id,
                    'dest_addr': phone,
                },
            ],
        }),

                                      headers={
                                          'Content-Type': content_type,
                                          'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                      },

                                      auth=(api_key, secret_key), verify=False)

        print(first_request.status_code)
        if first_request.status_code == 200:
            full_name = ''
            phone = ''
        print(first_request.json())

    # return (first_request.json())


@receiver(post_save, sender=InvestigationRecord, dispatch_uid='send_investigation_alert')
def send_investigation_alert(sender, instance, created, **kwargs):
    if created:

        URL = 'https://apisms.beem.africa/v1/send'
        api_key = '2799f1a807695012'
        secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
        content_type = 'application/json'
        source_addr = 'INFO'
        apikey_and_apisecret = api_key + ':' + secret_key

        '''Get name and concatenate them'''
        get_rb = instance.case_investigator.case.rb
        get_code = instance.case_investigator.case.complainant.code
        code = f"{get_code}"

        '''Get amount invested and daily amount earning'''

        '''Get phone detail and convert and user id as recipient_id on api'''
        # number= "255755422199"
        phone = str(instance.case_investigator.case.complainant.user.phone)
        # phone = str(number)
        phone = phone[1:10]
        # phone = phone
        phone = '255' + phone

        user_id = instance.case_investigator.case.complainant.user.id

        message_body = f"Hello complainant with code number: {code},\nchanges on the progress of the case with file " \
                       f"number:\n {get_rb}" \
                       f"\nhas been done, please login to the police site\n" \
                       f"https://crms-police.herokuapp.com/\n" \
                       f"for more information\n"

        print(message_body)
        first_request = requests.post(url=URL, data=json.dumps({
            'source_addr': source_addr,
            'schedule_time': '',
            'encoding': '0',
            'message': message_body,
            'recipients': [
                {
                    'recipient_id': user_id,
                    'dest_addr': phone,
                },
            ],
        }),

                                      headers={
                                          'Content-Type': content_type,
                                          'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                      },

                                      auth=(api_key, secret_key), verify=False)

        print(first_request.status_code)
        if first_request.status_code == 200:
            full_name = ''
            phone = ''
        print(first_request.json())

        # return (first_request.json())


#
@receiver(post_save, sender=Complainant, dispatch_uid='send_feedback_to_complaint')
def send_feedback_to_complaint(sender, instance, created, **kwargs):
    if created and instance.user.title == "complaint":

        URL = 'https://apisms.beem.africa/v1/send'
        api_key = '2799f1a807695012'
        secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
        content_type = 'application/json'
        source_addr = 'INFO'
        apikey_and_apisecret = api_key + ':' + secret_key

        '''Get name and concatenate them'''
        first_name = instance.user.first_name
        last_name = instance.user.last_name.upper()
        full_name = f"{first_name} {last_name}"

        '''Get amount invested and daily amount earning'''
        code = instance.code
        username = instance.user.username
        password = last_name

        '''Get phone detail and convert and user id as recipient_id on api'''
        # number= "255755422199"
        phone = str(instance.user.phone)
        # phone = str(number)
        phone = phone[1:10]
        # phone = phone
        phone = '255' + phone

        user_id = instance.user.id

        message_body = f"Hello, {full_name}, \nyou have been fully registered on the police system with a complainant " \
                       f"code {code}" \
                       f"\nyou can access the system via\n" \
                       f"https://crms-police.herokuapp.com/" \
                       f"\n username:{username},\n password:{password} "

        print(message_body)
        first_request = requests.post(url=URL, data=json.dumps({
            'source_addr': source_addr,
            'schedule_time': '',
            'encoding': '0',
            'message': message_body,
            'recipients': [
                {
                    'recipient_id': user_id,
                    'dest_addr': phone,
                },
            ],
        }),

                                      headers={
                                          'Content-Type': content_type,
                                          'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                      },

                                      auth=(api_key, secret_key), verify=False)

        print(first_request.status_code)
        if first_request.status_code == 200:
            full_name = ''
            phone = ''
        print(first_request.json())

        # return (first_request.json())
    else:

        URL = 'https://apisms.beem.africa/v1/send'
        api_key = '2799f1a807695012'
        secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
        content_type = 'application/json'
        source_addr = 'INFO'
        apikey_and_apisecret = api_key + ':' + secret_key

        '''Get name and concatenate them'''
        first_name = instance.user.first_name
        last_name = instance.user.last_name.upper()
        full_name = f"{first_name} {last_name}"

        '''Get amount invested and daily amount earning'''
        code = instance.code
        username = instance.user.username
        password = last_name

        '''Get phone detail and convert and user id as recipient_id on api'''
        # number= "255755422199"
        phone = str(instance.user.phone)
        # phone = str(number)
        phone = phone[1:10]
        # phone = phone
        phone = '255' + phone

        user_id = instance.user.id

        message_body = f"Hello, {full_name}, \nyou have been successful registered to a police system with a " \
                       f"complainant code {code}" \
                       f"\nyou can now approach any police station to report a case\n"
        print(message_body)
        first_request = requests.post(url=URL, data=json.dumps({
            'source_addr': source_addr,
            'schedule_time': '',
            'encoding': '0',
            'message': message_body,
            'recipients': [
                {
                    'recipient_id': user_id,
                    'dest_addr': phone,
                },
            ],
        }),

                                      headers={
                                          'Content-Type': content_type,
                                          'Authorization': 'Basic ' + api_key + ':' + secret_key,
                                      },

                                      auth=(api_key, secret_key), verify=False)

        print(first_request.status_code)
        if first_request.status_code == 200:
            full_name = ''
            phone = ''
        print(first_request.json())

        # return (first_request.json())
