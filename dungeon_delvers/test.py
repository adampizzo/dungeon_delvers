# name = '1Jonah'
# for char in name:
#     if char.isdigit():
#         print('Digit Found!')

# for x in range(1):
#     print(x)

# import pickle
# from random import randint


# def roll_x(x):
#     rolls = []
#     for i in range(1, x):
#         rolls.append(fighter_starting_cr())
#     print(sum(rolls) // x)


# def fighter_starting_cr():
#     total_roll = 0
#     for i in range(1, 8):
#         roll = randint(1, 4)
#         # print(f'Roll {i}: {roll}')
#         total_roll += roll
#     #print(f'Total Credits = {total_roll} * 100:\n{total_roll*100} CR')
#     return total_roll * 100


# roll_x(5)

# list_dict = [{"name": "test", "description": "descript"}]
# list_dict2 = [{"name": "test2", "description": "script2"}]
# list_dict.append(list_dict2[0])
# print(list_dict)


class A:
    def set_attribute_bonuses(self):
        print("1")
        print("2")
        print("3")

    def level_up_job(self):
        self.set_attribute_bonuses()
        print("4")
        print("5")
        print("Done")


class B(A):
    def set_attribute_bonuses(self):
        print("40")

a = B()
a.level_up_job()

