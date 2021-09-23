def generate_prime(n):
    """A function to generate prime numbers. Receives as input a natural n and generate
    a (probably) prime number p satisfying 10**n < p < 10**(n+2), randomly drawing p at
    the desired interval and running 10 Miller–Rabin primality tests with random bases b
    in the interval 1 < b < p − 1 (of course, p should only be accepted as probably prime
    if all tests are inconclusive)."""

    from random import randrange

    while True:
        p = randrange((10**n)+1, (10**(n+2))-1, 2) # Our odd random number in wich we will test primality

        tests = []
        for i in range(10):
            b = randrange(1, p-1) # Our random base b between 1 and p-1, generated at each test
            test = Miller_Rabin_test(p,b)

            # If this round's test is True, append and continue.
            # Otherwise, appends False before breaking to avoid exiting with only True in the list.
            if test == True:
                tests.append(test)
            else:
                tests.append(False)
                break

        if False not in tests:
            break

    return p

def generate_keys():
    """A function to generate RSA keys. It generates primes p and q, p with approximately 50 digits
    and q with approximately 100 digits, and returns:

    n = p*q
    An e number, inversible modulo φ = (p − 1)(q − 1)
    The inverse d of e modulo φ"""

    p = generate_prime(50)
    q = generate_prime(100)

    n = p*q

    phi = (p-1)*(q-1)

    e = 3
    while EEA(e, phi)['div'] != 1:
        e += 2

    d = EEA(e, phi)['A']

    # We sum the modulo in case the inverse d of e is a negative number
    if d < 0:
        d = d + phi

    return {'n':n, 'd':d, 'e':e}

def encrypt(text, n, e):
    """The encryption function. It receives as input a string and numbers n and e,
    and returns a list containing a valid sequence of numeric blocks resulting from
    the string encryption with public key of modulo n and exponent e."""

    symbols_to_codes = {'0': 111, '1': 112, '2': 113, '3': 114, '4': 115,
    '5': 116, '6': 117, '7': 118, '8': 119, '9': 121, '=': 122, '+': 123,
    '-': 124, '/': 125, '*': 126, 'a': 127, 'b': 128, 'c': 129, 'd': 131,
    'e': 132, 'f': 133, 'g': 134, 'h': 135, 'i': 136, 'j': 137, 'k': 138,
    'l': 139, 'm': 141, 'n': 142, 'o': 143, 'p': 144, 'q': 145, 'r': 146,
    's': 147, 't': 148, 'u': 149, 'v': 151, 'w': 152, 'x': 153, 'y': 154,
    'z': 155, 'á': 156, 'à': 157, 'â': 158, 'ã': 159, 'é': 161, 'ê': 162,
    'í': 163, 'ó': 164, 'ô': 165, 'õ': 166, 'ú': 167, 'ç': 168, 'A': 169,
    'B': 171, 'C': 172, 'D': 173, 'E': 174, 'F': 175, 'G': 176, 'H': 177,
    'I': 178, 'J': 179, 'K': 181, 'L': 182, 'M': 183, 'N': 184, 'O': 185,
    'P': 186, 'Q': 187, 'R': 188, 'S': 189, 'T': 191, 'U': 192, 'V': 193,
    'W': 194, 'X': 195, 'Y': 196, 'Z': 197, 'Á': 198, 'À': 199, 'Â': 211,
    'Ã': 212, 'É': 213, 'Ê': 214, 'Í': 215, 'Ó': 216, 'Ô': 217, 'Õ': 218,
    'Ú': 219, 'Ç': 221, ',': 222, '.': 223, '!': 224, '?': 225, ';': 226,
    ':': 227, '_': 228, '(': 229, ')': 231, '"': 232, '#': 233, '$': 234,
    '%': 235, '@': 236, ' ': 237, '\n': 238}

    b = ''

    for symbol in text:
        b += str(symbols_to_codes[symbol])

    batches = len(b)
    batch_size = len(str(n))-1

    # Divides b in parts to be encrypted
    parts = [int(b[i:i+batch_size]) for i in range(0, batches, batch_size)]

    # Encrypts each part with the public exponent e and modulus n
    parts[:] = [pow(part, e, n) for part in parts]

    return parts

def decrypt(parts, n, d):
    """The decryption function. It receives a list of parts and numbers n and d. It returns
    the string resulting of the decryption of the parts sequence using the private key with
    modulo n and exponent d."""

    codes_to_symbols = {111: '0', 112: '1', 113: '2', 114: '3', 115: '4',
    116: '5', 117: '6', 118: '7', 119: '8', 121: '9', 122: '=', 123: '+',
    124: '-', 125: '/', 126: '*', 127: 'a', 128: 'b', 129: 'c', 131: 'd',
    132: 'e', 133: 'f', 134: 'g', 135: 'h', 136: 'i', 137: 'j', 138: 'k',
    139: 'l', 141: 'm', 142: 'n', 143: 'o', 144: 'p', 145: 'q', 146: 'r',
    147: 's', 148: 't', 149: 'u', 151: 'v', 152: 'w', 153: 'x', 154: 'y',
    155: 'z', 156: 'á', 157: 'à', 158: 'â', 159: 'ã', 161: 'é', 162: 'ê',
    163: 'í', 164: 'ó', 165: 'ô', 166: 'õ', 167: 'ú', 168: 'ç', 169: 'A',
    171: 'B', 172: 'C', 173: 'D', 174: 'E', 175: 'F', 176: 'G', 177: 'H',
    178: 'I', 179: 'J', 181: 'K', 182: 'L', 183: 'M', 184: 'N', 185: 'O',
    186: 'P', 187: 'Q', 188: 'R', 189: 'S', 191: 'T', 192: 'U', 193: 'V',
    194: 'W', 195: 'X', 196: 'Y', 197: 'Z', 198: 'Á', 199: 'À', 211: 'Â',
    212: 'Ã', 213: 'É', 214: 'Ê', 215: 'Í', 216: 'Ó', 217: 'Ô', 218: 'Õ',
    219: 'Ú', 221: 'Ç', 222: ',', 223: '.', 224: '!', 225: '?', 226: ';',
    227: ':', 228: '_', 229: '(', 231: ')', 232: '"', 233: '#', 234: '$',
    235: '%', 236: '@', 237: ' ', 238: '\n'}

    decrypted_parts = []
    decrypted_parts[:] = [str(pow(part, d, n)) for part in parts]
    b = ''.join(decrypted_parts)
    b = [b[i:i+3] for i in range(0, len(b), 3)]

    message = ''
    for code in b:
        message += codes_to_symbols[int(code)]

    return message

""" Support functions: """

def Miller_Rabin_test(n, base):
	"""Receives an odd number n and a base, with 1 < base < n. Returns False if n is 'compound'
	or True if n is 'inconclusive' according to the Miller–Rabin primality test.
	https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test"""
	
	k, q = even_part(n-1)
	i = 0
	r = pow(base,q,n)

	if r in (1,n-1):
		return True

	while i < k:
		i += 1
		r = pow(r,2,n)
		if r == n-1:
			return True
		elif r == 1:
			return False

	return False

def even_part(m):
	"""Returns the numbers k and q, such that m = (2**k)*q, with q odd."""

	k = 0
	q = m
	while q % 2 == 0:
		k += 1
		q //= 2
	return k,q

def EEA(a, b):
    """Extended Euclidean Algorithm. Using a and b, returns A and B such that A*a+B*b = 1,
	in case a and b are coprimes."""

    divider, remainder = a,b
    old_x, new_x = 1,0
    ond_y, new_y = 0,1
    while remainder != 0:
        dividend, divider = divider, remainder
        quotient, remainder = dividend//divider, dividend%divider
        old_x, new_x = new_x, old_x - (new_x*quotient)
        ond_y, new_y = new_y, ond_y - (new_y*quotient)
    return {'div':divider, 'A':old_x, 'B':ond_y}
