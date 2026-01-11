class Undergraduate:
    def __init__(self, name, age, group, grade):
        self.name = name
        self.age = age
        self.group = group
        self.grade = grade
    
    def show_info(self):
        print("Имя: " + self.name + "，Возраст: " + str(self.age))
    
    def get_money(self):
        if self.grade == 5:
            return 6000
        elif self.grade < 5:
            return 4000
        else:
            return 0
    
    def compare_money(self, other):
        my_money = self.get_money()
        other_money = other.get_money()
        
        if my_money > other_money:
            return "больше"
        elif my_money < other_money:
            return "меньше"
        else:
            return "равно"

class Graduate:
    def __init__(self, name, age, group, grade, paper):
        self.name = name
        self.age = age
        self.group = group
        self.grade = grade
        self.paper = paper
    
    def show_info(self):
        print("Имя: " + self.name + "，Возраст: " + str(self.age))
    
    def get_money(self):
        if self.grade == 5:
            return 8000
        elif self.grade < 5:
            return 6000
        else:
            return 0
    
    def compare_money(self, other):
        my_money = self.get_money()
        other_money = other.get_money()
        
        if my_money > other_money:
            return "больше"
        elif my_money < other_money:
            return "меньше"
        else:
            return "равно"

if __name__ == "__main__":

    student1 = Undergraduate("Иван", 20, "Группа 1", 4.5)
    student2 = Graduate("Мария", 25, "Группа аспирантов", 5.0, "Научная статья по Python")
    
    student1.show_info()
    student2.show_info()
    
    print("Стипендия Ивана: " + str(student1.get_money()))
    print("Стипендия Марии: " + str(student2.get_money()))
    
    print("Сравнение стипендий: " + student1.compare_money(student2))