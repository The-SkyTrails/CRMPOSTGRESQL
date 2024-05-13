# import uuid


# def generate_ref_code():
#     code = str(uuid.uuid4()).replace("-", "")[:6]
#     return code


import random


def generate_ref_code():
    code = random.randint(100, 999)
    return code
