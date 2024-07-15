from cart.cart import Cart


def cart_total_amount(request):
    cart = request.session.get('cart', '')
    # Logic to calculate total cart amount
    total_amount = 0
    for i in cart:
        price = int(cart[i]['price'])
        quantity = cart[i]['quantity']
        total_amount += price * quantity
    return {'cart_total_amount': total_amount}



