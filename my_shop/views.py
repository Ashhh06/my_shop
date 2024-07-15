from django.shortcuts import render, redirect, get_object_or_404
from app.models import Category,Brand,Product,Contact_us,Order,ORDERSTATUS
from django.contrib.auth import authenticate,login,logout
from app.models import UserCreateForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart





def Master(request):
    return render(request, 'master.html')


def Index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand = brandID).order_by('-id')
    else:
        product = Product.objects.all()

    context = {
        'category': category,
        'product': product,
        'brand': brand,
    }
    return render(request, 'index.html', context)

#for logout
@login_required
def user_logout(request):
    logout(request)
    return render(request,'registration/logout.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()

    context = {
        'form':form,
    }
    return render(request, 'registration/signup.html',context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def Contact_Page(request):
    if request.method == "POST":
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request, 'contact.html')


def CheckOut(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        pincode = request.POST.get('pincode', '')
        cart = request.session.get('cart', '')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)

        total_amount = 0

        print(cart)

        print(name, email, city, state, address, phone, pincode, cart)
        for i in cart:
            a = int(cart[i]['price'])
            b = cart[i]['quantity']
            total = a * b
            total_amount += total
            print(i)
            order = Order(
                name=name,
                email=email,
                city=city,
                state=state,
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,
                total=total

            )
            order.save()

        request.session['cart'] = {}
        return redirect('/thanks/')


    return render(request, 'checkout.html')

def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk = uid)
    order = Order.objects.filter(user = user)
    context={
        'order':order,
    }
    return render(request,'order.html',context)


def Product_page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand = brandID).order_by('-id')
    else:
        product = Product.objects.all()

    context = {
        'category': category,
        'brand': brand,
        'product': product,
    }
    return render(request, 'product.html',context)


def Product_Detail(request,id):
    product = Product.objects.filter(id = id).first()
    context = {
        'product': product
    }
    return render(request,'product_detail.html',context)


def Search(request):
    query = request.GET['query']
    product = Product.objects.filter(name__icontains = query)
    context = {
        'product': product
    }
    return render(request,'search.html',context)

def Thanks(request):
    return render(request, 'thank_you.html')




@login_required
def OrderTracker(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    print(order_id, order)
    context = {
        'order': order
    }
    order.save()
    return render(request, 'orderstatus.html', context)

