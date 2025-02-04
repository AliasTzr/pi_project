import random, string

key_val = "".join([random.choice(string.printable) for _ in range(24)])

escaped_secret_key = (
    key_val.encode("unicode_escape").decode("utf-8")
)

print("Clé générer :", key_val)
print("Clé échappée :", escaped_secret_key)