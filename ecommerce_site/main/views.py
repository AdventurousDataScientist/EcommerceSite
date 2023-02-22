from django.shortcuts import render, redirect
from .forms import CreateItem, PaymentForm, DepositForm
from .models import Item, Profile, Order, PurchasedItem
import datetime

debug_file = open("debug.txt", "w")

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
    context = {}
    if request.method == 'POST':
        print('Cart Post request')
        arguments = request.POST
        debug_file = open("debug.txt", "w")
        debug_file.write('CART PAGE: Cart Post request \n')
        debug_file.write('\n')
        debug_file.write(f'CART PAGE Arguments \n')
        for key, value in arguments.items():
            debug_file.write(f'Argument: {key}, value: {value} \n')
        #checkboxes = request.POST.getlist('checks[]')
        debug_file.write('\n')
        debug_file.write('\n')
        #debug_file.close()
        #debug_file.write(f'CART PAGE Checkboxes: {checkboxes} \n')
        #for c in checkboxes:
        #    debug_file.write(f'Checkbox: {c} \n')
        #cart_debug_file.write('Cart Post request')
        #cart_debug_file.write(f'Arguments: {arguments}
        # i do not have item in the item name (BIG PROBLEM)

        cart_items = [Item.objects.get(name=arguments[a]) for a in arguments if 'item_' in a and '_quantity' not in a]
        cart_item_quantities = [int(arguments[a]) for a in arguments if '_quantity' in a]
        item_info = dict()
        order = Order(username=request.user.username)
        order.save()
        for item, quantity in zip(cart_items, cart_item_quantities):
            item_info[item.name] = [item.price, quantity]
            purchased_item = PurchasedItem(name=item.name, description=item.description, price=item.price, quantity=quantity, purchase_date=datetime.datetime.now(), order=order)
            purchased_item.save()
            #i = Item(name=item.name, price=item.price, description=item.description, buyer=request.user.username, order=order)

        total_cost = 0
        total_quantity = 0
        for item, info in item_info.items():
            total_cost += info[0] * info[1]
            total_quantity += info[1]
            context = {"item_info":item_info,
                'total_quantity': total_quantity,
               'total_cost':total_cost
                       }
    #cart_debug_file.close()
    elif request.method == 'GET':
        context = {}

    debug_file.write(f'CART PAGE Context: {context}')
    debug_file.close()

    return render(request, "main/cart.html", context)

def account(request):
    context = {}
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        has_profile = False
        if form.is_valid():
            """
            demo data
            cc# = 4444333322221111
            expiration date 11111
            cvv 111
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
                if not hasattr(request.user, 'profile'):

                    profile = Profile(user=request.user,\
                            credit_card_number=credit_card_number,\
                            expiration_date=expiration_date,\
                            cvv=cvv)
                    profile.save() # created credit card information
                    print('Credit Card Info uploaded')
                    print(f'Now add balance')
                    return redirect(f"/balance")
                """# need to add balance amount to website
                if not hasattr(request.user, 'profile'):
                    p = Profile(user=request.user, balance=balance)"""
    else:
        # if there is an account display that information, account username, balance
        # otherwise show the create account form
        has_profile = False
        if hasattr(request.user, 'profile'):
            has_profile = True
            context = {"has_profile": has_profile}
        else:
            has_profile = False
            form = PaymentForm()
            context = {
                "form": form,
                "has_profile": has_profile
            }

    return render(request, "main/account.html", context=context)

def history(request):
    orders = Order.objects.all().filter(username=request.user.username)
    context = {"orders":orders}
    return render(request, "main/history.html", context=context)

def checkout(request):
    # form should have purchase button
    context = {}
    if request.method == 'GET':
        debug_file = open("debug.txt", "w")
        debug_file.write('CHECK OUT GET REQUEST WORKS \n')
        order = Order.objects.get(username=request.user.username)
        total_cost = 0
        total_quantity = 0
        debug_file.write(f"{request.user.username}'s order: \n")
        for p_i in order.purchaseditem_set.all():
            debug_file.write(f"{p_i} \n")
            total_cost += p_i.quantity * p_i.price
            total_quantity += p_i.quantity
        debug_file.write(f'Total Cost: {total_cost}, Balance: {request.user.profile.balance} \n')
        request.user.profile.balance -= total_cost
        request.user.profile.save()
        debug_file.write(f'Balance After Purchase: {request.user.profile.balance} \n')
        debug_file.close()
        context = {
                    "profile":request.user.profile,
                    "order": order,
                   "total_cost": total_cost,
                "total_quantity": total_quantity
                   }
    return render(request, "main/checkout.html", context)

def balance(request):
    # MUST HAVE PROFILE BEFORE THIS FUNCTION IS EXECUTED
    # should throw an error, do error handling later
    if request.method == 'POST':
        debug_file = open("debug.txt", "w")
        debug_file.write(f'BALANCE PAGE: POST REQUEST WORKS')
        form = DepositForm(request.POST)
        if form.is_valid():
            # adding money to new account
            balance = form.cleaned_data["balance"]
            if not hasattr(request.user, 'profile'):
                # should throw an error, do error handling later
                p = Profile(user=request.user, balance=balance)
                p.save()
            # adding money to existing account
            else:
                request.user.profile.balance += balance
                request.user.profile.save()
            context = {"form": form, "balance": request.user.profile.balance}
            debug_file.write(f'BALANCE PAGE: USER PROFILE ADDED')
            debug_file.write(f'BALANCE PAGE: ADDING BALANCE BALANCE {request.user.profile.balance}, {type(balance)}')
            debug_file.close()
            return render(request, "main/balance.html", context)
        #return render(request, "main/balance.html")
    elif request.method == 'GET':
        print(f'BALANCE PAGE: GET REQUEST WORKS')
        debug_file = open("debug.txt", "w")
        debug_file.write(f'BALANCE PAGE: GET REQUEST WORKS')
        form = DepositForm()
        balance = 0
        if hasattr(request.user, 'profile'):
            balance = request.user.profile.balance
        context = {"form": form, "balance": balance}
        debug_file.write(f'BALANCE PAGE: BALANCE {balance}, {type(balance)}')
        debug_file.close()
        return render(request, "main/balance.html", context=context)

def end(request):
    return render(request, "main/end.html")