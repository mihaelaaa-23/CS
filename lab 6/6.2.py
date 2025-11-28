from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

m = """The addition of secrecy to the transformations produced cryptography. True, it was more of a game than anything else—it sought to delay comprehension for only the shortest possible time, not the longest—and the cryptanalysis was, likewise, just a puzzle. Egypt's was thus a quasi cryptology in contrast to the deadly serious science of today. Yet great things have small beginnings, and these hieroglyphs did include, though in an imperfect fashion, the two elements of secrecy and transformation that comprise the essential attributes of the science. And so cryptology was born. In its first 3,000 years, it did not grow steadily. Cryptology arose independently in many places, and in most of them it died the deaths of its civilizations. In other places, it survived, embedded in a literature, and from this the next generation could climb to higher levels. But progress was slow and jerky. More was lost than retained. Much of the history of cryptology of this time is a patchwork, a crazy quilt of unrelated items, sprouting, flourishing, withering. Only toward the Western Renaissance does the accreting knowledge begin to build up a momentum. The story of cryptology during these years is, in other words, exactly the story of mankind. China, the only high civilization of antiquity to use ideographic writing, seems never to have developed much real cryptography—perhaps for that reason. In one case known for military purposes, the 11th-century compilation, Wu-ching tsung-yao ("Essentials from Military Classics"), recommended a true if small code. To a list of 40 plaintext items, ranging from requests for bows and arrows to the report of a victory, the correspondents would assign the first 40 ideograms of a poem. Then, when a lieutenant wished, for example, to request more arrows, he was to write the corresponding ideogram at a specified place on an ordinary dispatch and stamp his seal on it. In China's great neighbor to the west, India, whose civilization likewise developed early and to high estate, several forms of secret communications were known and, apparently, practiced. The Artha-sastra, a classic work on statecraft attributed to Kautilya, in describing the espionage service of India as practically riddling the country with spies, recommended that the officers of the institutes of espionage give their spies their assignments by secret writing. Perhaps most interesting to cryptologists, amateur or professional, is that Vatsyayana's famous textbook of erotics, the Kamasutra, lists secret writing as one of the 64 arts, or yogas, that women should know and practice. The fourth great civilization of antiquity, the Mesopotamian, rather paralleled Egypt early in its cryptographic evolution, but then surpassed it. Thus, in the last period of cuneiform writing, in colophons written at Uruk (in present-day Iraq) under the Seleucid kings in the last few score years before the Christian era, occasional scribes converted their names into numbers. The encipherment—if such it be—may have been only for amusement or to show off."""

# convert to bytes (UTF-8)
m_bytes = m.encode("utf-8")

# Hash MD5
digest = hashes.Hash(hashes.MD5())
digest.update(m_bytes)
h = digest.finalize()
print("MD5 hash:", h.hex())

# Generate RSA 3072-bit key
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072
)
private_key = key
public_key = key.public_key()

# 4. Sign hash
signature = private_key.sign(
    h,
    padding.PKCS1v15(),
    hashes.MD5()
)

print("Signature (hex):", signature.hex())

# Verify signature
try:
    public_key.verify(
        signature,
        h,
        padding.PKCS1v15(),
        hashes.MD5()
    )
    print("✔️ Signature is VALID")
except Exception:
    print("❌ Signature is INVALID")
