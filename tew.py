from prettytable import PrettyTable

from args import args
from reader import Reader
from worker import Worker, Skills, Overness


def get_workers(reader):
    fed_id = __get_fed_by_initials(reader, args.initials)

    worker_rows = filter(lambda x: x['FedUID'] == fed_id, reader.read_table('tblContract'))
    workers = {}
    while True:
        try:
            worker = Worker(next(worker_rows))
            workers[worker.worker_id] = worker
        except RuntimeError:
            break

    records = filter(lambda x: x['WorkerUID'] in workers.keys(), reader.read_table('tblWorkerSkill'))
    while True:
        try:
            data = Skills(next(records))
            workers[data.id].set_skills(data)
        except RuntimeError:
            break

    records = filter(lambda x: x['WorkerUID'] in workers.keys(), reader.read_table('tblWorkerOver'))
    while True:
        try:
            data = Overness(next(records))
            workers[data.worker_id].set_overness(data)
        except RuntimeError:
            break

    t = PrettyTable(['ID', 'Name', 'Disposition', 'Gender', 'Role', 'Perception', 'Momentum', 'Overness',
                     'Brawl', 'Air', 'Technical', 'Power', 'Athletic', 'Stamina', 'Psych', 'Basics', 'Tough',
                     'Sell', 'Charisma', 'Mic', 'Menace', 'Respect', 'Reputation', 'Safety', 'Looks',
                     'Star', 'Consistency', 'Act', 'Injury', 'Puroresu', 'Flash', 'Hardcore', 'Announcing',
                     'Colour', 'Refereeing', 'Experience'])

    sorted_workers = sorted(workers.values(), key=lambda x: x.get_sort_key(args.sort), reverse=args.reverse)

    for v in sorted_workers:
        t.add_row(v.get_as_row())
    print(t)


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
