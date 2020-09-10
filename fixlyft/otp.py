from .forms import PhoneForm, VerifyForm
from django.shortcuts import render, redirect
from .models import SmsOTP
from django.http import JsonResponse
import random
import requests
import http.client
import ast
from django.utils import timezone
import datetime
from django.conf import settings
conn = http.client.HTTPConnection('2factor.in')

def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        return key
    else:
        return False



def phone_validation(request):
    api_key = getattr(settings, 'SMS_API_KEY')
    sms_template = getattr(settings, 'SMS_TEMPLATE_NAME')
    if request.method == 'POST':

        phone_number = request.POST['mobile_number']

        if phone_number:

            phone = str(phone_number)
            key = send_otp(phone)
            if key:
                old = SmsOTP.objects.filter(phone__iexact = phone)
                
                if old.exists():
                    print(key)
                    old = old.first()
                    old.otp = key
                    count = old.count
                    if count > 5:
                        return JsonResponse({
                            'status': False,
                            'detail': 'Sending OTP Error. Limit Exceeded'
                        })

                    old.count = count + 1
                    old.save()


                    conn.request('GET',"https://2factor.in/API/R1/?module=SMS_OTP&apikey=4f68f705-ef4a-11ea-9fa5-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=fixllyft99")
                    res = conn.getresponse()
                    data = res.read()
                    data = data.decode("utf-8")
                    data = ast.literal_eval(data)
                    

                    if data["Status"] == "Success":
                        conn.close()
                        old.otp_session_id = data["Details"]
                        old.timestamp = str(timezone.now)
                        old.save()

                        # for i in old:
                        #     i.otp_session_id = data["Details"]
                        #     i.save()

                        return JsonResponse({
                            'status': 'ok',
                            'detail': 'otp sents succesfully'
                        })

                    else:
                        return JsonResponse({
                            'status': False,
                            'detail': 'otp sending failed'
                        })

                else:

                    SmsOTP.objects.create(
                        phone = phone,
                        otp = key
                    )

                    conn.request('GET',"https://2factor.in/API/R1/?module=SMS_OTP&apikey=4f68f705-ef4a-11ea-9fa5-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=fixllyft99")
                    res = conn.getresponse()
                    data = res.read()
                    data = data.decode("utf-8")
                    data = ast.literal_eval(data)
                    

                    if data["Status"] == "Success":
                        conn.close()
                        # old.otp_session_id = data["Details"]
                        for i in old:
                            i.otp_session_id = data["Details"]
                            i.save()
                    

                        return JsonResponse({
                            'status': 'ok',
                            'detail': 'otp senttt succesfully'
                        })

                    else:
                        return JsonResponse({
                            'status': False,
                            'detail': 'otp sending failed'
                        })

                    # url = self.setUrl("developer", key, phone)
                    # requests.get(url)

                    # return Response({
                    #     'status': True,
                    #     'detail': '{} is your OTP'.format(key)
                    # })

            else:
                return JsonResponse({
                    'status' : False,
                    'detail' : 'Sending otp error'
                })

        else:
            return JsonResponse({
                'status': False,
                'detail': 'Missing paramater - phone_number'
            })

    else:
        return redirect('index')

def validate_otp(request):
    if request.method == 'POST':

  

        phone = request.POST['mobile_number']
        otp_sent = request.POST['otp']
        # password = 'comuungooys'

        if phone and otp_sent:
            timestamp_difference = datetime.datetime.now() - datetime.timedelta(minutes=30)
            old = SmsOTP.objects.filter(phone__iexact=phone, timestamp__gte=timestamp_difference)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.delete()
                    return JsonResponse({
                        'status': 'ok',
                        'detail': 'otp matched'
                    })

                else:
                    return JsonResponse({
                        'status': False,
                        'detail': 'Incorrect OTP, Please Try Again'
                    })

            else:
                return JsonResponse({
                    'status': False,
                    'detail': 'OTP Expired'
                })

        else:
            return JsonResponse({
                'status': False,
                'detail': 'Parameters Missing - Phone/OTP'
            })
    else:
        return redirect('index')
