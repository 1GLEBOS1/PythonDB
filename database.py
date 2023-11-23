import file as f


class Database:

    def __init__(self, path: str):
        self.path = path
        self.db = f.File(self.path)
        self.tables = []
        self.cash = {}
        self.__get_info__()
        pass

    def create(self, args):
        name = args[0]
        try:
            self.cash[name] += f'/{args[1]}|{args[2]}|{args[3]}'
        except ValueError as e:
            print(e)
        self.__update_file__()

    def read(self, args):
        self.__get_info__()
        name = args[0]
        table = self.cash[name]
        table = table.split('/')
        table = table[1:]
        for table_line in table:
            table_args = table_line.split('|')
            if table_args[0] == args[1]:
                for item in table_line.split('|'):
                    print(item, end=' ')
                print()

    def read_all(self):
        self.__get_info__()
        output = self.db.read()
        output = output.replace('@', '')
        output = output.replace('|', ' ', )
        print(output)

    def update(self, args):
        name = args[0]
        id_ = args[1]
        new_row = '|'.join(args[2:])
        table = self.cash[name]
        table = table.split('/')
        for i in range(len(table)):
            line_args = table[i].split('|')
            if line_args[0] == id_:
                table[i] = new_row
        self.cash[name] = '/'+'/'.join(table)
        if self.cash[name][0] == '/' and self.cash[name][1] == '/':
            self.cash[name] = self.cash[name][1:]
        self.__update_file__()

    def delete(self, args):
        self.__get_info__()
        name = args[0]
        table = self.cash[name]
        table = table.split('/')
        table = table[1:]
        for table_line in table:
            table_args = table_line.split('|')
            if table_args[0] == args[1]:
                table.remove(table_line)
                self.cash[name] = '/'+'/'.join(table)

                self.__update_file__()

    def __get_info__(self):
        database = self.db.read()
        database = database.split('\n')
        names = []
        for table in self.tables:
            names.append(table[0])
        print(end='')
        for line in database:
            if line == '':
                continue

            if line[0] == '@':
                nameline = line.split('|')
                name = nameline[1]
                if name not in names:
                    self.cash[name] = ''
                    args = {}
                    for i in range(2, len(nameline)):
                        item = nameline[i]
                        item = item.split(' ')
                        args[item[0]] = item[1]
                    self.tables.append([nameline[1], len(nameline)-2, args])

            else:
                if f'{line[0]}' not in self.cash[name]:
                    self.cash[name] += ('/' + line)

    def __get_count_of_args__(self, name):
        for i in self.tables:
            if i[0] == name:
                return i[1]

    def __update_file__(self):
        output = ''
        for table in self.tables:
            table_string = ''
            legend = ''
            for line in self.cash[table[0]].split('/'):
                table_string += line + '\n'
            for key, value in table[2].items():
                legend += f'|{key} {value}'
            output += f'@TABLE|{table[0]}{legend}{table_string}\n'

        while output[-1] == '\n':
            output = output[:-1]
        self.db.write(output)
        self.__get_info__()

