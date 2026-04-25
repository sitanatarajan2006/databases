from db import database
from ui import app

def main():
    print("Starting application...")
    database()
    app()


if __name__ == "__main__":
    main()