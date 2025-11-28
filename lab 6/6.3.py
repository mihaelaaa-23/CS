from Crypto.Hash import MD4
from secrets import randbelow
from math import gcd

p = int("""
32317006071311007300153513477825163362488057133489075174588434139269806834136210002792056362640164685458556357935330816928829023080573472625273554742461245741026202527916572972862706300325263428213145766931414223654220941111348629991657478268034230553086349050635557712219187890332729569696129743856241741236237225197346402691855797767976823014625397933058015226858730761197532436467475855460715043896844940366130497697812854295958659597567051283852132784468522925504568272879113720098931873959143374175837826000278034973198552060607533234122603254684088120031105907484281003994966956119696956248629032338072839127039
""".replace("\n", "").replace(" ", ""))

g = 2

m = """The addition of secrecy to the transformations produced cryptography. True, it \
was more of a game than anything else—it sought to delay comprehension for only the \
shortest possible time, not the longest—and the cryptanalysis was, likewise, just a puzzle. \
Egypt's was thus a quasi cryptology in contrast to the deadly serious science of today. \
Yet great things have small beginnings, and these hieroglyphs did include, though in an \
imperfect fashion, the two elements of secrecy and transformation that comprise the \
essential attributes of the science. And so cryptology was born. In its first 3,000 years, \
it did not grow steadily. Cryptology arose independently in many places, and in most of \
them it died the deaths of its civilizations. In other places, it survived, embedded in a \
literature, and from this the next generation could climb to higher levels. But progress \
was slow and jerky. More was lost than retained. Much of the history of cryptology of this \
time is a patchwork, a crazy quilt of unrelated items, sprouting, flourishing, withering. \
Only toward the Western Renaissance does the accreting knowledge begin to build up a \
momentum. The story of cryptology during these years is, in other words, exactly the story \
of mankind. China, the only high civilization of antiquity to use ideographic writing, \
seems never to have developed much real cryptography—perhaps for that reason. In one case \
known for military purposes, the 11th-century compilation, Wu-ching tsung-yao ("Essentials \
from Military Classics"), recommended a true if small code. To a list of 40 plaintext \
items, ranging from requests for bows and arrows to the report of a victory, the \
correspondents would assign the first 40 ideograms of a poem. Then, when a lieutenant \
wished, for example, to request more arrows, he was to write the corresponding ideogram at \
a specified place on an ordinary dispatch and stamp his seal on it. In China's great \
neighbor to the west, India, several forms of secret communications were known and \
practiced. The Artha-sastra recommended that officers give spies their assignments using \
secret writing. Most interesting is that the Kamasutra lists secret writing among the 64 \
arts women should know and practice. The Mesopotamian civilization paralleled Egypt early \
in cryptographic evolution but eventually surpassed it. In the last period of cuneiform \
writing, scribes sometimes converted their names into numbers—possibly for amusement or \
display."""
m_bytes = m.encode("utf-8")

md4 = MD4.new()
md4.update(m_bytes)
h_bytes = md4.digest()
h = int.from_bytes(h_bytes, "big")

print("MD4 hash (hex):", h_bytes.hex())
print("MD4 as integer:", h)
print("MD4 bit length:", h.bit_length())

h_mod = h % (p - 1)

# ElGamal key generation
x = randbelow(p - 2) + 1
y = pow(g, x, p)

print("\nPrivate key x:", x)
print("Public key y:", y)

# Signing
while True:
    k = randbelow(p - 2) + 1
    if gcd(k, p - 1) == 1:
        break

r = pow(g, k, p)
k_inv = pow(k, -1, p - 1)
s = ((h_mod - x * r) * k_inv) % (p - 1)

print("\nRandom k:", k)
print("k inverse:", k_inv)
print("r =", r)
print("s =", s)

# 6. Verification
v1 = pow(g, h_mod, p)
v2 = (pow(y, r, p) * pow(r, s, p)) % p

print("\nVerification left:", v1)
print("Verification right:", v2)
print("\nValid signature?", v1 == v2)