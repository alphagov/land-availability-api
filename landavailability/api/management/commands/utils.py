from api.models import Address, CodePoint


def normalise_postcode(postcode):
    return postcode.replace(' ', '').upper()


def get_address_from_postcode(postcode):
    return Address.objects.filter(postcode=normalise_postcode(postcode))


def get_codepoint_from_postcode(postcode):
    try:
        return CodePoint.objects.get(postcode=normalise_postcode(postcode))
    except CodePoint.DoesNotExist:
        return None
