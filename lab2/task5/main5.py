import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time() 
        result = func(*args, **kwargs)  
        end = time.time()  
        print("Время выполнения функции：", end - start, "s")
        return result
    return wrapper

@timer
def add_and_print(a, b):
    result = a + b
    print(f"{a} + {b} = {result}")
    return result

@timer
def read_calculate_write():
    with open("task5/input.txt", "r") as f:
        lines = f.readlines()
        a = int(lines[0].strip())
        b = int(lines[1].strip())
    
    result = a + b
    
    with open("task5/output.txt", "w") as f:
        f.write(f"{a} + {b} = {result}\n")
    
    print(f"Читает из файла input.txt: a={a}, b={b}")
    print(f"Результат вычисления: {result}")
    print("Записывает результат вычисления в файл output.txt")
    return result

if __name__ == "__main__":
    add_and_print(10, 20)
    read_calculate_write()