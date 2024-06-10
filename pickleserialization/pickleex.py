import pickle

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def get_info(self):
        print(self.name)
        print(self.age)

if __name__ == '__main__':
    # Serialization - Convert Object to Byte Stream
    naga = Person("Naga", 35)
    with open('naga.pickle', mode='wb') as f:
        pickle.dump(naga, f)

    # deserialization - Convert Byte Stream to Object
    with open('naga.pickle', mode='rb') as f:
        deser_per :  Person = pickle.load(f)

    deser_per.get_info()


