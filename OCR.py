import json
import os

import requests
from PIL import Image
from pytesseract import image_to_string

from variable import PARTIES_LIST


def removeNumbers(string_numbers):
    for i, el in enumerate(string_numbers):
        if not string_numbers[-int(i) - 1].isdigit():
            return string_numbers[-int(i - 1) - 1:]
            break


with open('results.json', 'w+') as f:
    f.write('[')
    for bureau_index, folder in enumerate(os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE'))):
        for pv_index, image in enumerate(os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder))):
            img = [str(elt) for elt in
                   image_to_string(
                       Image.open(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, image))).split(
                       '\n') if not elt.replace(" ", "") == ""]
            bureau_de_Vote = img[0].replace("O", '0').replace('I', '1').replace(" ", "").split("_")[-1]
            enrolled_number = img[1].split(':')[-1].replace("I", "1").replace(" ", "")
            print(bureau_de_Vote)
            print(enrolled_number)
            print(img)
            print(folder + image)
            party = [int(removeNumbers(elt.replace(" ", ""))) for elt in
                     img[4:len(PARTIES_LIST) + 4]]
            print(party)
            global_id = 11 * bureau_index + pv_index
            print(folder)
            if folder == "ELECAM":
                real_id, party_name = "elecam", None
            elif folder == "REAL_RESULT":
                real_id, party_name = "bon", None
            else:
                real_id, party_name = global_id, PARTIES_LIST.index(folder)
            data_format = dict(id=global_id, bureau=bureau_de_Vote, nbreInscrits=enrolled_number,
                               nbreVotants=enrolled_number,
                               voix=party, idScrutateur=global_id,
                               nomScrutateur=real_id, parti=party_name)
            json.dump(data_format, f)
            f.write(',')
            # r = requests.post('http://localhost:4000/', data=data_format)

    f.write(']')