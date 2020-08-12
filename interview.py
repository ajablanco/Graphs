# Implement functionality to reverse an input string. Print out the reversed string.
# For example, given a string "cool", print out the string "looc".
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solvi



word = input("Enter a string:")
print(word)
new_list = list()
for i in reversed(range(len(word))):
    letter = word[i]
    new_list.append(letter)


end_string = "".join(new_list)
print(end_string)

# way faster
print(word[::-1])