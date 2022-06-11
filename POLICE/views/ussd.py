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
        number = []
        # data = text.split('')

        response = ""

        if text == "":
            response = "CON Karibu CCRMS \nTafadhali Ingiza namba yako Kuendelea \n"
            # response .= "1. My Account \n"
            # response += "1. My Phone Number"

        elif text:

            get_code = Complainant.objects.filter(code=text).count()
            if get_code >= 1:

                response = "CON welcome {0}: -{1}-{2}"
            else:

                response = "END Namba si sahihi Tafadhali fika kituo chochote cha polisi kwa msaada zaidi"

        return HttpResponse(response)
