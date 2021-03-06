from itertools import count

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
from ..models import Complainant


@csrf_exempt
def ussd(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        text_array = text.split("*")
        user_response = text_array[len(text_array) - 1]
        # level = count(text_array)

        response = ""

        if text == "":
            response = "CON Karibu CCRMS \nTafadhali Ingiza namba yako Kuendelea \n"
            # response .= "1. My Account \n"
            # response += "1. My Phone Number"

        elif text:

            get_code = Complainant.objects.filter(code=text).count()
            get_number=get_code
            if get_number == 1:
                get_complaint = Complainant.objects.filter(code=text).first()
                code = get_complaint.code

                response += "CON Karibu {0}: {1} {2} \n1. Endelea ".format(get_complaint.code,
                                                                                get_complaint.user.first_name,
                                                                                get_complaint.user.last_name)
                if get_number == 1 and text == "{0}*1".format(code):
                    response = "END umechagua moja {0}".format(get_number)
                # else:
                #     response = "END umechagua moja {0}".format(text)



            else:

                response = "END Namba si sahihi, Tafadhali fika kituo chochote cha polisi kwa msaada zaidi"
        return HttpResponse(response)
