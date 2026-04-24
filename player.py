import playground
from pathlib import Path

def play():
    # Safe path building (cross-platform)
    base = Path(".")
    print(base)    # . (current directory)
    data_file = base / "data" / "users.json"   # . / data / users.json
    print(data_file)

    # __file__ is the hidden "Dunder" birth certificate of the script
    script_location = Path(__file__).resolve().parent
    print(script_location)


def main():
    print("Hello, PyKing!")
    #playground.exec7()

if __name__ == "__main__":
    main()
    play()