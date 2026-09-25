# def sumFunc(a, b):
#     print(a + b)


# sumFunc(4, 3)

# vowels = "aeiouAEIOU"

# name = input("Enter your name: ")

# vowelCount = 0
# consonantCount = 0

# for eachChar in name:
#     if eachChar.isalpha():
#         if eachChar in vowels:
#             vowelCount += 1
#         else:
#             consonantCount += 1

# print("Vowels:", vowelCount)
# print("Consonants:", consonantCount)

# vowels = "aeiouAEIOU"

# name = input("Enter your name: ")


# def countVowelsAndConsonants():
#     vowelCount = 0
#     consonantCount = 0

#     for eachChar in name:
#         if eachChar.isalpha():
#             if eachChar in vowels:
#                 vowelCount += 1
#             else:
#                 consonantCount += 1

#     return vowelCount, consonantCount


# vowelCount, consonantCount = countVowelsAndConsonants()

# print("vowels" ,vowelCount, "consonant",consonantCount)


# if we dont use return in funtion then we see none

def greet():
    print("Salam")

salam = greet()
print(salam)