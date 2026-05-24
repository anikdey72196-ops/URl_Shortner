from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest

import string
import secrets
from .models import link 

def Short_url_generate(lenght=8):
    alphabet = string.ascii_letters + string.digits
    unique_str = ''.join(secrets.choice(alphabet) for _ in range(lenght))
    return unique_str

def home(request):
    return render(request, 'shorten_form.html')

def receive_url(request):
    if request.method == 'POST':
        long_url = request.POST.get('URl')
        if not long_url:
            return HttpResponseBadRequest("URL is required")
        while True:
            short_code = Short_url_generate()
            if not link.objects.filter(Short_url=short_code).exists():
                break
        Link = link.objects.create(
            Long_url=long_url,
            Short_url=short_code
        )
        return render(request, 'shorten_form.html', {'short_code': short_code})
    return redirect('home')

def redirect_to_long(request, short_code):
    url_entry = get_object_or_404(link, Short_url=short_code)
    url_entry.click += 1
    url_entry.save()
    return redirect(url_entry.Long_url)
