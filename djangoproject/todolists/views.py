from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolists.models import Item


# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/unique-list/')
    return render(request, 'home_page.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
