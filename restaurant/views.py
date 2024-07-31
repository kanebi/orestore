from django.shortcuts import render,get_object_or_404
from .models import MenuItem
# Create your views here.


def menuitem_view(request, id):
    menuitem = get_object_or_404(MenuItem, id=id)
    context ={'menuitem':menuitem}
    return render(request, 'restaurant/menuitem.html', context)