import datetime

from django.shortcuts import render, redirect

from .forms import CreateItem, PaymentForm, DepositForm, CreateStoreForm
from .models import Item, Profile, Order, PurchasedItem, Store

debug_file = open("debug.txt", "w")

# Create your views here.


def home(request):
    #print(f'Home page username: {request.user.username}, type: {type(request.user.username)}')
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect(f"/login")
        else:
            stores = request.user.store_set.all()
            return render(request, "main/home.html", {"user":request.user, "stores":stores})


def create(request, store_name):
    store = Store.objects.get(owner=request.user, name=store_name)

    if request.method == 'POST':
        form = CreateItem(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            # for image add image url upload
            stock = form.cleaned_data["stock"]
            rating = form.cleaned_data["rating"]
            image_url = form.cleaned_data["image_url"]
            item = Item(name=name, category=category, image_url=image_url, description=description, price=price, stock=stock, rating=rating, store=store)
            item.save()
            #request.user.sold_items.add(item)
        return redirect(f"/create/{store.name}") # redirect to same form
    else:
        form = CreateItem()
        return render(request, f"main/create_item.html", {"form": form})


def list_all_items(request):
    items = Item.objects.all()
    return render(request, "main/inventory.html", {"items":items})


def show_item(request, id):
    item = Item.objects.get(id=id)
    return render(request, "main/item.html", {"item": item})


def cart(request, store_name):
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
        store = Store.objects.get(name=store_name)
        cart_item_numbers =  [a for a in arguments if 'item_' in a and '_quantity' not in a]
        cart_items = [Item.objects.get(name=arguments[a]) for a in arguments if 'item_' in a and '_quantity' not in a]
        cart_item_quantities = [int(arguments[f'{item_number}_quantity']) for item_number in cart_item_numbers]
        item_info = dict()
        order = Order(user=request.user, store=store)
        order.save()
        for item, quantity in zip(cart_items, cart_item_quantities):
            item_info[item.name] = [item.price, quantity]
            purchased_item = PurchasedItem(name=item.name, description=item.description,\
                             price=item.price, quantity=quantity, purchase_date=datetime.datetime.now(),\
                            order=order)
            purchased_item.save()
            #i = Item(name=item.name, price=item.price, description=item.description, buyer=request.user.username, order=order)

        total_cost = 0
        total_quantity = 0
        for item, info in item_info.items():
            total_cost += info[0] * info[1]
            total_quantity += info[1]
        context = {"item_info":item_info,
            'total_quantity': total_quantity,
            'total_cost':total_cost,
            'order': order
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
            profile = Profile.objects.filter(user=request.user).first()
            print(f'Existing Profile: {profile.balance}')
            context = {"has_profile": has_profile, "profile":profile}
        else:
            has_profile = False
            form = PaymentForm()
            context = {
                "form": form,
                "has_profile": has_profile
            }

    return render(request, "main/account.html", context=context)

def history(request):
    orders = Order.objects.all().filter(user=request.user)
    context = {"orders":orders}
    return render(request, "main/history.html", context=context)

def checkout(request, order_id):
    # form should have purchase button
    context = {}
    if request.method == 'GET':
        debug_file = open("debug.txt", "w")
        debug_file.write('CHECK OUT GET REQUEST WORKS \n')
        order = Order.objects.get(user=request.user, id=order_id)
        store = Store.objects.get(id=order.store.id)
        total_cost = 0
        total_quantity = 0
        debug_file.write(f"{request.user.username}'s order: \n")
        for p_i in order.purchaseditem_set.all():
            debug_file.write(f"{p_i} \n")
            total_cost += p_i.quantity * p_i.price
            total_quantity += p_i.quantity
        debug_file.write(f'Total Cost: {total_cost}, Balance: {request.user.profile.balance} \n')
        
        if request.user.username != store.owner.username:
            request.user.profile.balance -= total_cost
            request.user.profile.save()
            store.revenue += total_cost
            store.save()

        
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

def create_store(request):
    if request.method == 'GET':
        form = CreateStoreForm()
        context = {"form": form}
    elif request.method == 'POST':
        form = CreateStoreForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            name = form.cleaned_data["name"]
            revenue = 0.00
            store = Store(owner=request.user, name=name, category=category, description=description, revenue=revenue)
            store.save()
            context = {"form": CreateStoreForm()}
    return render(request, "main/create_store.html", context=context)

def show_store(request, store_id):
    store = Store.objects.get(id=store_id)
    store_items = store.item_set.all()
    for i in store_items:
        print(f'Item url: {i.image_url}')
    if request.method == 'POST':
        arguments = request.POST
        debug_file = open("debug.txt", "w")
        debug_file.write("Show Store Post Arguments \n\n")
        print(arguments)
        debug_file.write(f"Arguments: {arguments}")
        debug_file.close()
    return render(request, "main/show_store.html", {"store": store, "store_items":store_items})

def marketplace(request):
    stores = Store.objects.all()
    return render(request, "main/marketplace.html", {"stores": stores})