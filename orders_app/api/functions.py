from users_auth_app.models import UserProfile
from orders_app.models import Order

def get_business_user(business_user_id):
    """
    Validates if the business user exists.
    """
    try:
        business_user = UserProfile.objects.get(pk=business_user_id)
        if business_user.type != 'business':
            return None
        return business_user
    except UserProfile.DoesNotExist:
        return None

def count_orders(status_filter, business_user_id):
    """
    Counts the orders.
    """
    return Order.objects.filter(status=status_filter, business_user_id=business_user_id).count()

def create_order(offer_detail, customer_user):
    """
    Creates an order.
    """
    business_user = offer_detail.offer.user 
    return Order.objects.create(
        customer_user=customer_user,
        business_user=business_user,
        title=offer_detail.title,
        revisions=offer_detail.revisions,
        delivery_time_in_days=offer_detail.delivery_time_in_days,
        price=offer_detail.price,
        features=offer_detail.features,
        offer_type=offer_detail.offer_type,
        status='in_progress' 
    )
