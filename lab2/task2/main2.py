def my_function(filter_lambda, string_list):
    new_list = []

    for i in range(len(string_list)):
        if filter_lambda(string_list[i]):
            new_list.append(string_list[i])
    return new_list

if __name__ == "__main__":
    my_strings = ["apple", "banana split", "cherry", "avocado", "grape", "kiwi fruit", "aardvark", "orange", "plum"]

    print(my_strings)
    print()
    
    # Исключить строки с пробелами
    print("Исключить строки с пробелами:")
    func1 = lambda s: s.find(" ") == -1 
    result1 = my_function(func1, my_strings)
    print(result1)
    print()
    
    # Исключить строки, начинающиеся с буквы “a” 
    print("Исключить строки, начинающиеся с буквы “a” :")
    func2 = lambda s: s[0] != "a" 
    result2 = my_function(func2, my_strings)
    print(result2)
    print()
    
    # Исключить строки, длина которых меньше 5 
    print("Исключить строки, длина которых меньше 5 :")
    func3 = lambda s: len(s) >= 5  
    result3 = my_function(func3, my_strings)
    print(result3)