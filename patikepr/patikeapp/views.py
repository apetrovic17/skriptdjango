from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Patike
from .forms import PatikeForm


def index(req):
    return render(req, 'index.html', {'page_title': 'Patikeapp'})




def patike(req):
    tmp = Patike.objects.all()
    return render(req, 'patike.html', {'patike': tmp})

def patika(req, id):
    tmp = get_object_or_404(Patike, id=id)
    return render(req, 'patika.html', {'patika': tmp, 'page_title': tmp.naziv})

@permission_required('patikeapp.add_patika')
def new(req):
    return None


@permission_required('demo_app.change_patike')
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


@permission_required('demo_app.add_article')
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