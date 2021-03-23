from pprint import pprint
import csv
import re

my_raw = "phonebook_raw.csv"
my_target = "phonebook.csv"


def convert_full_name(input_list):
    new_list = []
    for entry in input_list[0:3]:
        new_list += re.split(r'\s', entry)
    return new_list[0:3]


def convert_phone(text):
    pattern = re.compile(r"(\+7|8)?\s{0,2}(\(?)(\d{3})(\)?)(\s{0,2}|-)(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})((\s)?\(?("
                         r"доб\.)\s?(\d{4})\)?)?")
    new_text = pattern.sub(r'+7(\3)\6-\7-\8\10\11\12', text)
    return new_text


def merge_two_lists(a: list, b: list):
    d = [ij[0]
         + '/' * (ij[0] != '' and ij[1] != '' and ij[0] != ij[1])
         + ij[1] * (ij[0] != ij[1])
         for ij in list(zip(a, b))]
    return d


def merge_clones(my_list: list):
    new_list = [my_list.pop()]
    while my_list:
        item = my_list.pop()
        flag = 1
        for ii, entry in enumerate(new_list):
            if item[0] == entry[0]:
                new_list[ii] = merge_two_lists(entry, item)
                flag = 0
        if flag:
            new_list.append(item)

    return new_list


class PhoneBookProcessor:
    def __init__(self):
        self.raw = str()
        self.old_list = []
        self.new_list = []

    def read_raw(self, raw):
        self.raw = raw
        with open(self.raw, 'r', encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",")
            self.old_list = list(rows)

    def convert_book(self):
        new_list = [convert_full_name(entry)
                    + entry[3:5]
                    + [convert_phone(entry[5])]
                    + [entry[6]] for entry in self.old_list]

        self.new_list = [new_list[0]] + merge_clones(new_list[1:])
        self.new_list[1:].sort(key=lambda x: x[0])
        return self.new_list

    def write_result(self, target_path):
        with open(target_path, "w", encoding='UTF-8') as f:
            datawriter = csv.writer(f, delimiter=',', lineterminator='\r')
            datawriter.writerows(self.new_list)


if __name__ == '__main__':
    my_proc = PhoneBookProcessor()
    my_proc.read_raw(my_raw)
    my_proc.convert_book()
    my_proc.write_result(my_target)
