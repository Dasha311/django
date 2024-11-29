from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from store.forms import DishForm, UpdateDishForm
from store.models import Dish

from django.views import View

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )