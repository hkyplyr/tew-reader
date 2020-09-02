import os

from meza import io

from args import args

args = args.parse_args()


class Reader:
    def __init__(self):
        self.database_path = self.__get_database_path()

    def read_table(self, table):
        return io.read_mdb(self.database_path, table=table)

    def __get_database_path(self):
        tew_path = self.__get_or_prompt_value(args.tew_home, 'TEW_PATH', 'Enter path to the TEW2020 folder: ')
        tew_db = self.__get_or_prompt_value(args.tew_db, 'TEW_DB', 'Enter the name of your TEW2020 database: ')
        tew_save = self.__get_or_prompt_value(args.tew_save, 'TEW_SAVE', 'Enter the name of the TEW save game: ')
        return f'{tew_path}/Databases/{tew_db}/SaveGames/{tew_save}/TEW2020.mdb'

    def __get_or_prompt_value(self, arg_variable, env_variable, prompt):
        if arg_variable is not None:
            value = arg_variable
        else:
            value = os.environ.get(env_variable)
        if value is None:
            value = input(prompt)
        return value
