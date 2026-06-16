from random import randint
randint (1,10)
secret_number = randint(1,10)

guess = 0
while guess != secret_number:
    guess = int(input("Guess a number between 1 and 10: "))
    if guess > 10 or guess < 1:
        print(' STAY IN THE RANGE MATE')

    if guess != secret_number:
        print("wrong")
    if guess == secret_number:
        print("you guessed right")
