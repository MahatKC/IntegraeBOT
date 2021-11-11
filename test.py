import numpy as np

def delete_category():
    print(0)

def print_queue_users():
    print(1)

def empty_queue_allocating_groups():
    print(2)

admin_funcs = {
    0: delete_category,
    1: print_queue_users,
    2: empty_queue_allocating_groups
}

stringzinha = "ronaldonazariodelima"

print(stringzinha.replace("ronaldo","").replace("lima",""))



