import database
import console


class Handling:
    def __init__(self, db: database.Database):
        self.db = db
        self.operations = {
            'CREATE': lambda x: self.db.create,
            'READ': lambda x: self.db.read,
            'UPDATE': lambda x: self.db.update,
            'DELETE': lambda x: self.db.delete,
            'QUIT': 'exit'  # Stops the program
        }

    def handle(self):
        command = input()
        args = command.split(' ')
        try:
            args.remove('WITH')
        except ValueError as e:
            pass
        if args[0] == 'CREATE':
            self.db.create(args[1::])
        elif args[0] == 'READ' and args[1] == 'ALL':
            self.db.read_all()
        elif args[0] == 'READ':
            self.db.read(args[1::])
        elif args[0] == 'UPDATE':
            self.db.update(args[1::])
        elif args[0] == 'DELETE':
            self.db.delete(args[1::])
        else:
            exit(0)


def main():
    db = database.Database('database.txt')
    h = Handling(db)
    while __name__ == "__main__":
        h.handle()


main()
