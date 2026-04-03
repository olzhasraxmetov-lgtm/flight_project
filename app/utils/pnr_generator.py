import secrets
import string

def generate_pnr_identifier(length=6):
    characters = string.ascii_uppercase + string.digits
    pnr = ''.join(secrets.choice(characters) for _ in range(length))
    return pnr