import random


print("hello world")
# now i am learning python programming language
"""
name = "kali linux kasdfiqwjoeijqoiroqiueroqwiuproquwwoeiu"
print(name)

this is uamir's first python program

"""
# size = "36"
# size = 36

# isAuth = True

# print(name)
# print(size)
# print(isAuth)


# data types
I = 4
i = (int)("7")
# i = 3
s = "umair's world"
f = 3.14

print(type(i), type(s), type(f), type(I), s, i, I)


def sd01():
    print("this is a function")
    return "function executed"


sd01()


x = str("Hello World")


z = 3e15
print(type(z), z)

r = random.randrange(1,7)
# print(random(1,6))
print(r)


a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a = "Hello, World!"
print(a[0:])


a = "Hello, World!"
print(len(a))


txt = "The best things in life are free!"

if "free" in txt:
  print("Yes, 'free' is present.")


# slice

b = "Hello, World!"
print(b[2:5])

b = "Hello, World!"
print(b[-5:-2])


# modify

a = "Hello, World!"

a = a.upper()
print(a)
a = a.lower()
print(a)

a = "Hello, World!"
a = a.replace("H", "J")
print(a)


a = "Hello, World!"
print(a.split("o")) 

a = "Hello"
b = "World"
c = a + " " + b
print(c)


age = 36
#This will produce an error:
txt = "My name is John, I am {age}"
print(txt)


price = 59
txt = f"The price is {price} dollars"
print(txt)


price = 59
# txt = f"The price is {price:.4f} dollars"
print(txt)

# txt = 'We are the so-called "Vikings" from the north.'
txt = "We are the \ooo  so-called \"Vikings\" from the north."
# txt = "We are the \xhh so-called \"Vikings\" from the north."
print(txt)



txt = txt.casefold()
print(txt)

txt = "Umair"

x = txt.encode()

print(x)


txt = "My name is Ståle"

print(txt.encode(encoding="ascii",errors="backslashreplace"))
print(txt.encode(encoding="ascii",errors="ignore"))
print(txt.encode(encoding="ascii",errors="namereplace"))
print(txt.encode(encoding="ascii",errors="replace"))
print(txt.encode(encoding="ascii",errors="xmlcharrefreplace"))