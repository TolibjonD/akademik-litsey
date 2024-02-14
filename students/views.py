from django.shortcuts import render, redirect
from education.forms import ContactForm
from education.models import Contact


def home_page(request):
    
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request , "index.html", {"form": form})
    else:
        form = ContactForm()
        messages = Contact.objects.all()
        return render(request , "index.html", {"form": form, "messages": messages})
    
def landing_page(request):
    return render(request, "landing_page.html")