from rest_framework.decorators import api_view


@api_view(['GET'])
def offers_list(request):
    return