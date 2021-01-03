from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Patike
from .forms import PatikeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import RegisterForm


def index(req):
    return render(req, 'index.html', {'page_title': 'Patikeapp'})

@login_required()
def patike(req):
    tmp = Patike.objects.all()
    return render(req, 'patike.html', {'patike': tmp})

def patika(req, id):
    tmp = get_object_or_404(Patike, id=id)
    return render(req, 'patika.html', {'patika': tmp, 'page_title': tmp.naziv})

def delete(req, id):
    Patike.objects.filter(id=id).delete()
    tmp = Patike.objects.all()
    return render(req, 'patike.html', {'patike': tmp})


@permission_required('patikeapp.change_patike')
def edit(req, id):
    if req.method == 'POST':
        form = PatikeForm(req.POST)

        if form.is_valid():
            a = Patike.objects.get(id=id)
            a.naziv = form.cleaned_data['naziv']
            a.model = form.cleaned_data['model']
            a.velicina = form.cleaned_data['velicina']
            a.cena = form.cleaned_data['cena']
            a.save()
            return redirect('patikeapp:patike')
        else:
            return render(req, 'edit.html', {'form': form, 'id': id})
    else:
        a = Patike.objects.get(id=id)
        form = PatikeForm(instance=a)
        return render(req, 'edit.html', {'form': form, 'id': id})


@permission_required('patikeapp.add_patike')
def new(req):
    if req.method == 'POST':
        form = PatikeForm(req.POST)

        if form.is_valid():
            a = Patike(naziv=form.cleaned_data['naziv'], model=form.cleaned_data['model'], velicina=form.cleaned_data['velicina'], cena=form.cleaned_data['cena'])
            a.save()
            return redirect('patikeapp:patike')
        else:
            return render(req, 'new.html', {'form': form})
    else:
        form = PatikeForm()
        return render(req, 'new.html', {'form': form})


def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Vec postoji to korisnicko ime.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Vec postoj taj email.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Sifra se ne poklapa.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()

                # Login the user
                login(request, user)

                # redirect to accounts page:
                return HttpResponseRedirect('/')

    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})