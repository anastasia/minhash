import sys
import random
import binascii
import settings

def calculate(str_one, str_two):
    shingles_one = str_to_shingles(str_one)
    shingles_two = str_to_shingles(str_two)

    coeffs_a = generate_coefficients()
    coeffs_b = generate_coefficients()

    sigs_a = get_min_signatures(shingles_one, coeffs_a, coeffs_b)
    sigs_b = get_min_signatures(shingles_two, coeffs_a, coeffs_b)

    # union_count has to be float so that our minhash doesn't get cast to int
    union_count = 0.0
    for i, val in enumerate(sigs_a):
        if sigs_b[i] == val:
            union_count += 1

    return union_count / settings.HASH_NUM

def get_min_signatures(shingles, coeffs_a, coeffs_b):
    min_signatures = list()
    hash_count = 0
    while hash_count < settings.HASH_NUM:
        min_hash = settings.PRIME + 1
        for shingle in shingles:
            # hash function is (a*x + b) % c
            # Where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is our prime num
            current_hash = (coeffs_a[hash_count] * shingle + coeffs_b[hash_count]) % settings.PRIME
            if current_hash < min_hash:
                min_hash = current_hash
        min_signatures.append(min_hash)
        hash_count += 1
    return min_signatures

def str_to_shingles(string):
    shingles_in_doc = set()

    if settings.SHINGLE_TYPE == 'word':
        units = string.split(' ')
    elif settings.SHINGLE_TYPE == 'char':
        units = list(string)

    for idx in range(0, len(units) - (settings.SHINGLE_SIZE - 1)):
        shingle = create_shingle(units[idx:idx+settings.SHINGLE_SIZE])
        shingles_in_doc.add(shingle)

    return shingles_in_doc

def create_shingle(list_to_create):
    if settings.SHINGLE_TYPE == 'word':
        shingle = ' '.join(list_to_create)

    elif settings.SHINGLE_TYPE == 'char':
        shingle = ''.join(list_to_create)

    # hash the shingle to a 32-bit integer
    return binascii.crc32(shingle) & 0xffffffff

def generate_coefficients():
  # create a unique set of 'settings.HASH_NUM' random values
  rand_set = set()
  hash_num = 0

  while hash_num < settings.HASH_NUM:
    rand_num = random.randint(0, settings.MAX_SHINGLE_ID)
    rand_set.add(rand_num)

    # if rand_num not added, it means that it already exists in set
    # Try again.
    if len(rand_set) - 1 == hash_num:
        hash_num += 1

  return list(rand_set)

if __name__ == '__main__':
    str_one, str_two = ['','']
    with open(sys.argv[1], 'rb+') as f:
        str_one = f.read()

    with open(sys.argv[2], 'rb+') as f:
        str_two = f.read()

    print calculate(str_one, str_two)
