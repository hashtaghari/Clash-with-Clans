
from src.main import Run


if __name__ == '__main__':

    print("Welcome to Clash with Clans!")
    print("Hark! O' Holy Commander of the Village fair,\nIn dire despair, our humble hamlet cries for thee!")
    print("Choose your character: ")
    print("1. King")
    print("2. Queen")
    choice = '0'

    while choice != '1' or choice != '2':
        choice = input()
        if choice == '1':
            Run(1)
            break
        elif choice == '2':
            Run(2)
            break
        else:
            print("Invalid choice")
            print("Please choose 1 or 2")
            print("1. King")
            print("2. Queen")

