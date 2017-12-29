from django.shortcuts import render
from website.forms import UserReg


def index(request):
    data = {'artworks': ''}
    return render(request, 'website/index.html', data)


def gallery(request):
    data = {'artworks': 'artworks'}
    return render(request, 'website/gallery.html', data)


def user_reg_view(request):
    form = UserReg()
    data = {'form': form}

    if request.method == 'POST':
        form = UserReg(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print('form invalid')
    return render(request, 'website/form.html', data)
