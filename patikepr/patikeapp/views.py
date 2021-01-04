from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Patike, Ocene
from .forms import PatikeForm, OceneForm
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
    oc = Ocene.objects.filter(patike=tmp)
    return render(req, 'patika.html', {'patika': tmp, 'page_title': tmp.naziv, 'ocene': oc})

def delete(req, id):
    Patike.objects.filter(id=id).delete()
    tmp = Patike.objects.all()
    return render(req, 'patike.html', {'patike': tmp})


@permission_required('patikeapp.change_patike')
def edit(req, id):
    if req.method == 'POST':
        form = PatikeForm(req.POST)

        if form.is_valid():
            p = Patike.objects.get(id=id)
            p.naziv = form.cleaned_data['naziv']
            p.model = form.cleaned_data['model']
            p.velicina = form.cleaned_data['velicina']
            p.cena = form.cleaned_data['cena']
            p.save()
            return redirect('patikeapp:patike')
        else:
            return render(req, 'edit.html', {'form': form, 'id': id})
    else:
        p = Patike.objects.get(id=id)
        form = PatikeForm(instance=p)
        return render(req, 'edit.html', {'form': form, 'id': id})


@permission_required('patikeapp.add_patike')
def new(req):
    if req.method == 'POST':
        form = PatikeForm(req.POST)

        if form.is_valid():
            p = Patike(naziv=form.cleaned_data['naziv'], model=form.cleaned_data['model'], velicina=form.cleaned_data['velicina'], cena=form.cleaned_data['cena'])
            p.save()
            return redirect('patikeapp:patike')
        else:
            return render(req, 'new.html', {'form': form})
    else:
        form = PatikeForm()
        return render(req, 'new.html', {'form': form})


@login_required()
def oceni(req,id):
    if req.method == 'POST':
        form = OceneForm(req.POST)

        if form.is_valid():

            a = Ocene(ocena=form.cleaned_data['ocena'], opis=form.cleaned_data['opis'], owner=req.user, patike=Patike.objects.get(id=id))
            a.save()
            tmp = get_object_or_404(Patike, id=id)
            return redirect('/patika/'+str(id))
        else:
            tmp = get_object_or_404(Patike, id=id)
            return render(req, 'patika.html', {'patika': tmp, 'page_title': tmp.naziv, 'form': form})



def user_register(request):

    template = 'register.html'

    if request.method == 'POST':

        form = RegisterForm(request.POST)

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

                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()


                login(request, user)


                return HttpResponseRedirect('/')


    else:
        form = RegisterForm()

    return render(request, template, {'form': form})