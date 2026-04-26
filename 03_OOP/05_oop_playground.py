class Animal():
    def __init__(self, name, height, weight, color):
        self.name = name
        self.height = height
        self.weight = weight
        self.color = color
    
    def speaks(self):
        return "Makes Sound"


class Lion(Animal):
    def __init__(self, height, weight):
        super().__init__("Lion", height, weight, "Brown")

    def speaks(self):
        return "Roars"


################CIRCUS#######################
def describeAnimal(animal:Animal):
    print(f"Animal name is {animal.name}")
    print(f"Animal height is {animal.height}")
    print(f"Animal weight is {animal.weight}")
    print(f"Animal color is {animal.color}")
    print(f"Animal {animal.speaks()}")

ant = Animal("Ant", 1, 1, "Black")
lion = Lion(10, 100)

describeAnimal(animal=ant)
describeAnimal(animal=lion)


