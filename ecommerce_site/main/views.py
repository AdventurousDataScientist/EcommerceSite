from django.shortcuts import render, redirect
from .forms import CreateItem, PaymentForm
from .models import Item, PaymentModel

cart_debug_file = open("cart_debug.txt", "w")

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

def cart(request):
    if request.method == 'POST':
        #print('Cart Post request')
        arguments = request.POST
        print('Cart Post request')
        print(f'Arguments: {arguments}')
        cart_debug_file.write('Cart Post request')
        cart_debug_file.write(f'Arguments: {arguments}')
        cart_items = [Item.objects.get(name=a) for a in arguments if 'item' in a and '_quantity' not in a]
        cart_item_quantities = [int(arguments[a]) for a in arguments if '_quantity' in a]
        item_info = dict()
        for item, quantity in zip(cart_items, cart_item_quantities):
            item_info[item.name] = [item.price, quantity]
        total_cost = 0
        total_quantity = 0
        for item, info in item_info.items():
            #cart_debug_file.write(f'Item: {item}, Quantity: {info[1]}')

            total_cost += info[0] * info[1]
            total_quantity += info[1]
            context = {"item_info":item_info,
                'total_quantity': total_quantity,
               'total_cost':total_cost
                       }
    #cart_debug_file.close()
    elif request.method == 'GET':
        context = {}
    return render(request, "main/cart.html", context)

def account(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            """
            demo data
            cc# = 4444333322221111
            expiration date 02/23
            cvv 000
            """
            credit_card_number = form.cleaned_data["cc_number"]
            expiration_date = form.cleaned_data["cc_expiry"]
            cvv = form.cleaned_data["cc_code"]

            username = 'N/A'
            email = 'N/A'
            print(f'user authenticated? {request.user.is_authenticated}')
            if request.user.is_authenticated:
                username = request.user.username
                email = request.user.email
                payment = PaymentModel(name=username,\
                            credit_card_number=credit_card_number,\
                            expiration_date=expiration_date,\
                            cvv=cvv)
                payment.save()
                print(f'Saved payment instance: {payment}')
                print('')
                print(PaymentModel.objects.all())
    else:
        form = PaymentForm()

    context = {"form": form}
    return render(request, "main/account.html", context=context)

def history(request):
    return render(request, "main/history.html")

def checkout(request):
    return render(request, "main/checkout.html")