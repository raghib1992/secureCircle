list_1 = ["a", "b"]
list_2 = ["a", "b", "c"]
list_2 = ["a", "b", "c", 'd']

for element in list_1:
    if element in list_2:
        list_2.remove(element)

print(list_2)
x = 'a'
x = 'b'
print(x)