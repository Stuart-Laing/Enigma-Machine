from enigma import *


if __name__ == '__main__':
    s1 = Scrambler("uwygadfpvzbeckmthxslrinqoj")
    s2 = Scrambler("ajpczwrlfbdkotyuqgenhxmivs")
    s3 = Scrambler("tagbpcsdqeufvnzhyixjwlrkom")

    s1.tick(4)
    s3.tick(1)

    r = Reflector("yruhqsldpxngokmiebfzcwvjat")

    p = Plugboard("asugle", "bzyhqn")
    m = Machine(r, p, s2, s1, s3)

    plain_text = "gyhrvflrxy"
    cipher_text = m.compute(plain_text)

    print(f"'{plain_text}' encoded as '{cipher_text}'")

    m.reset()
    decoded_plain_text = m.compute(cipher_text)
    print(f"'{cipher_text}' decoded as '{decoded_plain_text}'")
