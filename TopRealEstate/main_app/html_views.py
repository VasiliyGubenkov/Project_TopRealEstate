from django.http import HttpResponse

def start(request):
    return HttpResponse("Привет, это сайт TopRealEstate!")