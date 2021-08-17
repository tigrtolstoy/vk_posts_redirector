import os
import re
import json
import atexit
from functools import partial


def clean_text(text):
    clear_text = re.sub(r'http\S+', '', text)
    clear_text = re.sub('[^A-Za-zА-Яа-я0-9]+', ' ', clear_text)
    clear_text = clear_text.lower()
    clear_text = clear_text.strip()
    return clear_text


def remove_short_words(text, min_word_len=3):
    words = text.split(' ')
    words = [word for word in words if len(word) >= min_word_len]
    return ' '.join(words)


def clear():
    os.system('clear')


def get_text(path_to_file):
    with open(path_to_file, 'r') as text_file:
        text = text_file.read()
    return text


def save_text(path_to_save, text):
    with open(path_to_save, 'w') as text_file:
        text_file.write(text)



path_to_texts = os.path.join(os.getcwd(), 'texts', 'raw_texts')
path_to_save = os.path.join(os.getcwd(), 'texts', 'dataset')

raw_texts_files = os.listdir(path_to_texts)

file_counter = 0 

labels_fname = 'labels.json'
labels = dict()


def save_labels_dict(fname):
    if not len(labels):
        return
    with open(fname, 'w') as labels_file:
        json.dump(labels, labels_file)


atexit.register(partial(save_labels_dict, fname=labels_fname))


if os.path.exists(labels_fname):
    with open(labels_fname, 'r') as labels_file:
        labels = json.load(labels_file)
    labeled_texts = list(labels.keys())
    raw_texts_files = [file for file in raw_texts_files if file not in labeled_texts]


files_num = len(raw_texts_files)

categories_dict = {
    0: 'Пост',
    1: 'Реклама',
}


while file_counter <= files_num:
    fname = raw_texts_files[file_counter]
    path_to_file = os.path.join(path_to_texts, fname)
    text = get_text(path_to_file)
    
    print(text)

    user_input = input('Press the key!\n')
    if user_input == '':
        label = 0
    else:
        label = 1

    labels[fname] = label
    
    clear_text = clean_text(text)
    clear_text = remove_short_words(clear_text, min_word_len=3)

    fname_to_save = os.path.join(path_to_save, fname)
    save_text(fname_to_save, clear_text)
    clear()
    print(f'Файл {fname} помечен как {categories_dict[label]}')
    print(f'Всего файлов: {files_num}. Помечено файлов: {file_counter + 1}', end='\n'*3)
    file_counter += 1

save_labels_dict(labels, labels_fname)
