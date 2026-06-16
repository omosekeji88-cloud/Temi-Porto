import random


def choose_difficulty():
    difficulty = input('Choose a difficulty: easy or hard: ').strip().lower()
    if difficulty == 'hard':
        return 5
    return 10


def play_game():
    secret_number = random.randint(1, 100)
    attempts = choose_difficulty()

    print('I am thinking of a number between 1 and 100.')

    while attempts > 0:
        print(f'You have {attempts} attempts remaining.')

        try:
            guess = int(input('Make a guess: '))
        except ValueError:
            print('Please enter a whole number.')
            continue

        if guess == secret_number:
            print(f'Correct. The number was {secret_number}.')
            return

        if guess < secret_number:
            print('Too low.')
        else:
            print('Too high.')

        attempts -= 1

    print(f'Out of attempts. The number was {secret_number}.')


if __name__ == '__main__':
    play_game()
