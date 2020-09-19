import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def normalizes_fullname(data):
    result = []
    pattern = re.compile(r'^([а-яё]+)[\s|,]([а-яё]+)[\s|,]([а-яё]+)?', re.I)
    for contact in data:
        one_contact = ','.join(contact)
        normalized_contact = pattern.sub(r'\1,\2,\3', one_contact).split(',')
        if not normalized_contact[4]:
            normalized_contact.pop(4)
        if not normalized_contact[3]:
            normalized_contact.pop(3)
        result.append(normalized_contact)
    return result


def normalizes_phone_number(data):
    result = []
    pattern = re.compile(r'(\+7|8)\s?\(?(\d{3})\)?(\s|-)?(\d{3})-?(\d{2})-?(\d{2})(\s)?\(?([а-я]{3}\.\s\d{4})?\)?')
    for contact in data:
        one_contact = ','.join(contact)
        normalized_phone = pattern.sub(r'+7(\2)\4-\5-\6\7\8', one_contact).split(',')
        result.append(normalized_phone)
    return result


def remove_duplicates(data):
    temp_dict = {}
    for contact in data:
        if contact[0] in temp_dict:
            for item in range(len(contact)):
                if contact[item] and not data[temp_dict[contact[0]]][item]:
                    data[temp_dict[contact[0]]][item] = contact[item]
                elif contact[item] and data[temp_dict[contact[0]]][item] != contact[item]:
                    data[temp_dict[contact[0]]][item + 1] = contact[item]
            data.remove(contact)
        else:
            temp_dict[contact[0]] = data.index(contact)
    return data


normalized_phonebook = remove_duplicates(normalizes_phone_number(normalizes_fullname(contacts_list)))

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(normalized_phonebook)
