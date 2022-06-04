from django.shortcuts import render
# Create your views here.
def LandingPageFunction(request):
    context = {'id':123}
    return render(request, "HTML/LandingPage.html", context=context)
