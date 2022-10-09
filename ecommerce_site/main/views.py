from django.shortcuts import render, redirect
from .forms import CreateItem
from .models import Item
# Create your views here.
def home(request):
    return render(request, "main/home.html")

def create(request):
    if request.method == 'POST':
        form = CreateItem(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            item = Item(name=name, description=description, price=price)
            item.save()
            request.user.sold_items.add(item)
        return redirect(f"/item/{item.id}")
    else:
        form = CreateItem()
        return render(request, "main/create_item.html", {"form": form})

def list_all_items(request):
    items = Item.objects.all()
    return render(request, "main/inventory.html", {"items":items})

def show_item(request, id):
    item = Item.objects.get(id=id)
    return render(request, "main/item.html", {"item": item})