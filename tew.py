import csv
import datetime
import sys
from dateutil.relativedelta import relativedelta

from prettytable import PrettyTable

from args import args
from reader import Reader
from worker import Worker, Skills, Overness


def __intialize_workers(reader):
    workers = {}
    fed_id = __get_fed_by_initials(reader, args.initials)
    contract_data = filter(lambda x: x['FedUID'] == fed_id, reader.read_table('tblContract'))
    while True:
        try:
            worker = Worker(next(contract_data))
            workers[worker.worker_id] = worker
        except RuntimeError:
            break
    return workers


def __get_date(year, month):
    return datetime.datetime(year=int(year), month=int(month), day=1)


def __set_worker_age(reader, workers):
    current_date = __get_current_date(reader)
    bio_data = filter(lambda x: x['UID'] in workers.keys(), reader.read_table('tblWorker'))
    while True:
        try:
            bio = next(bio_data)
            birth_date = __get_date(bio['Birth_Year'], bio['Birth_Month'])
            age = relativedelta(current_date, birth_date).years
            workers[bio['UID']].set_age(age)
        except RuntimeError:
            break


def __get_current_date(reader):
    game_info = next(reader.read_table('tblGameInfo'))
    return __get_date(game_info['CurrentDateY'], game_info['CurrentDateM'])


def __set_worker_skills(reader, workers):
    skill_data = filter(lambda x: x['WorkerUID'] in workers.keys(), reader.read_table('tblWorkerSkill'))
    while True:
        try:
            skills = Skills(next(skill_data))
            workers[skills.worker_id].set_skills(skills)
        except RuntimeError:
            break


def __set_worker_overness(reader, workers):
    over_data = filter(lambda x: x['WorkerUID'] in workers.keys(), reader.read_table('tblWorkerOver'))
    while True:
        try:
            overness = Overness(next(over_data))
            workers[overness.worker_id].set_overness(overness)
        except RuntimeError:
            break


def get_workers(reader):
    workers = __intialize_workers(reader)
    __set_worker_age(reader, workers)
    __set_worker_skills(reader, workers)
    __set_worker_overness(reader, workers)

    workers = __sort_workers(workers, args.sort, args.reverse)

    __output_data(workers, args.output)


def __output_data(workers, output):
    if output == 'csv':
        writer = csv.writer(sys.stdout)
        writer.writerow(Worker.get_header_names())
        for worker in workers:
            writer.writerow(worker.get_as_row())

    elif output == 'table':
        table = PrettyTable(Worker.get_header_names())
        for worker in workers:
            table.add_row(worker.get_as_row())
        print(table)


def __sort_workers(workers, sort_key, reverse):
    return sorted(workers.values(), key=lambda x: x.get_sort_key(sort_key), reverse=reverse)


def __get_fed_by_name(reader, name):
    records = filter(lambda x: x['Name'] == name, reader.read_table('tblFed'))
    data = next(records)
    return data['UID']


def __get_fed_by_initials(reader, initials):
    records = filter(lambda x: x['Initials'] == initials, reader.read_table('tblFed'))
    data = next(records)
    return data['UID']


if __name__ == '__main__':
    get_workers(Reader())
