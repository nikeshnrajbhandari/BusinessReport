import traceback
import base64
import pandas as pd

def encrypt_token(token: str) -> str:
    try:
        if not len(token):
            return token
        token_length = len(token)
        # partition token into two halves
        first_half, second_half = token[:token_length // 2], token[token_length // 2:]
        # encode two halves and join with !!&!!
        encoding = base64.b64encode(first_half.encode('ascii')) + "!!&!!".encode('ascii') + \
                   base64.b64encode(second_half.encode('ascii'))
        # encode again
        encoding = base64.b64encode(encoding).decode('ascii')
        return encoding
    except Exception as e:
        traceback.print_exc()
        raise Exception("Error in encrypt token(): " + str(e))


def decrypt_token(cipher: str) -> str:
    try:
        if not len(cipher):
            return cipher
        # decode
        decoding = base64.b64decode(cipher.encode('ascii'))
        # split
        first_half, second_half = decoding.split(b"!!&!!")
        # decode
        decoding = base64.b64decode(first_half) + base64.b64decode(second_half)
        # convert to str
        decoding = decoding.decode('ascii')
        return decoding
    except Exception as e:
        traceback.print_exc()
        raise Exception("Error in decrypt token(): " + str(e))


def decrypt_credentials(credential: dict) -> dict:
    credential = credential.copy()
    if "user" in credential:
        credential["user"] = decrypt_token(credential["user"])
    if "password" in credential:
        credential["password"] = decrypt_token(credential["password"])
    return credential


# if __name__ == '__main__':
#     print(encrypt_token(''))


def convert_to_number_round(i):
    try:
        return round(pd.to_numeric(i))
    except Exception:
        return i