from rest_framework.decorators import api_view


@api_view(['GET'])
def orders_list(request):
    return