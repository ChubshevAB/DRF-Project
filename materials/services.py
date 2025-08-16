import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name, description=None):
    """Создает продукт в Stripe."""

    product = stripe.Product.create(
        name=name,
        description=description,
    )
    return product.id


def create_stripe_price(product_id, amount, currency="usd"):
    """Создает цену для продукта в Stripe."""

    amount_in_cents = int(amount * 100)

    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount_in_cents,
        currency=currency,
    )
    return price.id


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создает сессию оплаты в Stripe."""

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url
