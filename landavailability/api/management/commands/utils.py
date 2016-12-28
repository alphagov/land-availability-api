from api.models import Address, CodePoint


def get_address_from_postcode(postcode):
    return Address.objects.filter(postcode=postcode)


def get_codepoint_from_postcode(postcode):
    try:
        return CodePoint.objects.get(postcode=postcode)
    except CodePoint.DoesNotExist:
        return None
