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

                    message_body = f"Habari,Ndugu {full_name}, \nUmesajiliwa Kikamilifu kwenye Mfumo wa Polisi kama {title}" \
                                   f"\nWaweza kuingia kwenye Mfumo  kupitia\n" \
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

        message_body = f"Habari,Ndugu Namba: {full_name}, \nJarada lako limefunguliwa kikamilifu kwa RB:\n {get_rb_string}" \
                       f"\nWaweza Bofya *149*01# kufuatilia mwenendo wa " \
                       f"Jarida\nAu ingia kwenye tovuti Kwa taarifa zaidi \n https://crms-police.herokuapp.com/"

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

        message_body = f"Habari,Ndugu Namba: {code}, \nJarada namba:\n {get_rb}" \
                       f"\nLimefanyiwa maboresho, tafadhali ingia kwenye tovuti kwa taarifa zaidi\n"\
                                   f"https://crms-police.herokuapp.com/"

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
    if created:

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

        message_body = f"Habari,Ndugu {full_name}, \nUmesajiliwa Kikamilifu kwenye Mfumo wa Polisi kwa namba {code}" \
                       f"\nWaweza kuingia kwenye Mfumo  kupitia\n" \
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

#
# @receiver(post_save, sender=Type, dispatch_uid='create_payment_structure')
# def create_payment_structure_total(sender, instance, created, **kwargs):
#     if created:
#         get_ordinary_level = Level.objects.get(name="O-Level")
#         get_advanced_level = Level.objects.get(name="A-Level")
#
#         PaymentStructure.objects.create(type=instance, level=get_ordinary_level)
#         PaymentStructure.objects.create(type=instance, level=get_advanced_level)

# @receiver(post_save, sender=Payment, dispatch_uid='update_balance')
# def update_remaining_fee_amount(sender, instance, created, **kwargs):
#     if created:
#         get_latest_balance = InvestmentTracking.objects.filter(
#             investment__account__code=instance.investment.account.invite).order_by(
#             '-id').first()
#         get_user = Investment.objects.filter(account__code=instance.investment.account.invite).order_by('-id').first()
#
#         # print(get_latest_balance.balance)
#
#         save_balance = InvestmentTracking(
#             investment=get_user,
#             total_referral=get_latest_balance.total_referral + decimal.Decimal(float(instance.amount)),
#             total_earning=get_latest_balance.total_earning,
#             total_withdraw=get_latest_balance.total_withdraw,
#
#             balance=get_latest_balance.balance + instance.amount
#         )
#         save_balance.save()
