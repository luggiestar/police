from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.


@csrf_exempt
def ussd(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        data = text.split('')

        response = ""

        if text == "":
            response = "CON Karibu CCRMS \nTafadhali Ingiza namba yako Kuendelea \n"
            # response .= "1. My Account \n"
            # response += "1. My Phone Number"

        elif data[0]:
            response = "END My Phone number is {0}".format(data[0])

        return HttpResponse(response)
