import random

def generate_otp():
  number = random.randint(1000, 9999)
  return str(number)
