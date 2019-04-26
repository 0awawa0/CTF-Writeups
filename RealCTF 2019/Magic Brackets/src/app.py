import random

print("Welcome, traveller!")
print("I have a task for you.")
print("I will give you some numbers.")
print("The only thing you have to do is send them back to me.")
print("If you do everything correctly, I will give you the flag.")
print("Sounds easy, right?")
print("However, to prove that you are the true bracket master, you can only use the following symbols: ()[]<>|")
print("Well here we go:")

for _ in range(100):
    num = random.randint(100, 100000)
    print(num)
    try:
        if num != eval("".join([c for c in input() if c in "()[]<>|"])):
            print("Sorry, that's wrong :c")
            exit(0)
    except:
        print("Ouch, that hurts :c")
        exit(0)
print("Good job!")
print("Your flag is [REDACTED]")
