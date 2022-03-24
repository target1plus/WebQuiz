# init file

import json
import random
from operator import itemgetter

with open("src/Quiz/Main_DB.json", "r", encoding='UTF8') as json_file:
    main_db = json.load(json_file)

countries_dict_article_nom = {}
countries_dict_preposition_1 = {}
countries_un_member = []
countries_un_member_and_with_border = []
countries_un_member_and_landlocked = []
countries_un_member_and_not_landlocked = []
countries_un_member_and_without_border = []
countries_un_member_and_driving_right = []
countries_un_member_and_driving_left = []
countries_un_member_and_north = []
countries_un_member_and_south = []
countries_un_member_and_east = []
countries_un_member_and_west = []
country_population_list_unordered = []
country_area_list_unordered = []
for country in main_db:
    countries_dict_article_nom[country['Alpha-2 code']] = country['Article_Nom']
    countries_dict_preposition_1[country['Alpha-2 code']] = country['Preposition_1']
    if country['Membre_ONU']:
        countries_un_member.append(country['Alpha-2 code'])
        country_population_list_unordered.append([country['Alpha-2 code'], country['Population']])
        country_area_list_unordered.append([country['Alpha-2 code'], country['Surface_Area']])
        if country['Borders'] == []:
            countries_un_member_and_without_border.append(country['Alpha-2 code'])
        else:
            countries_un_member_and_with_border.append(country['Alpha-2 code'])
        if country['Landlocked']:
            countries_un_member_and_landlocked.append(country['Alpha-2 code'])
        else:
            countries_un_member_and_not_landlocked.append(country['Alpha-2 code'])
        if country['Drive_side'] == "left":
            countries_un_member_and_driving_left.append(country['Alpha-2 code'])
        else:
            countries_un_member_and_driving_right.append(country['Alpha-2 code'])
        if country['North-South'] == "north":
            countries_un_member_and_north.append(country['Alpha-2 code'])
        if country['North-South'] == "south":
            countries_un_member_and_south.append(country['Alpha-2 code'])
        if country['East-West'] == "east":
            countries_un_member_and_east.append(country['Alpha-2 code'])
        if country['East-West'] == "west":
            countries_un_member_and_west.append(country['Alpha-2 code'])
country_population_list_unordered.sort(key=itemgetter(1), reverse=True)
country_area_list_unordered.sort(key=itemgetter(1), reverse=True)
country_population_dict = {}
for i in range(len(country_population_list_unordered)):
    country_population_dict[country_population_list_unordered[i][0]] = [f"{country_population_list_unordered[i][1]:,} (#{i + 1} des membres de l'ONU)", i+1]
country_area_dict = {}
for i in range(len(country_area_list_unordered)):
    country_area_dict[country_area_list_unordered[i][0]] = [f"{country_area_list_unordered[i][1]:,} km² (#{i + 1} des membres de l'ONU)", i+1]



def random_selection(countries_list, qty_choices=4):
    return random.sample(countries_list, qty_choices)


def capital_from_country_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Preposition_2'], country['Capitale']])
                break
    good_answer = random.choice(quiz_dict)
    plural = False
    for item in quiz_dict:
        if " et " in item[1]:
            plural = True
    question = f"Quelle est la capitale {'(Quelles sont les capitales) ' if plural else ''} {good_answer[0]}?"
    return quiz_dict, good_answer, question


def country_from_capital_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Capitale'], country['Preposition_2']])
                break
    good_answer = random.choice(quiz_dict)
    question = f"{good_answer[0]+' sont les capitales' if ' et ' in good_answer[0] else good_answer[0]+' est la capitale'} de quel pays?"
    return quiz_dict, good_answer, question


def borders_from_country_quiz():
    selection = random_selection(countries_un_member_and_with_border, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Article_Nom'], country['Borders']])
                break
    choice_with_only_one = False
    for i in range(len(quiz_dict)):
        length = len(quiz_dict[i][1])
        if length == 1:
            choice_with_only_one = True
        borders_list = countries_dict_article_nom[quiz_dict[i][1][0]]
        if length > 1:
            for elem in range(1, length-1):
                borders_list = borders_list + ", " + countries_dict_article_nom[quiz_dict[i][1][elem]]
            borders_list = borders_list + " et " + countries_dict_article_nom[quiz_dict[i][1][-1]]
        quiz_dict[i][1] = borders_list
    good_answer = quiz_dict[-1]
    for item in quiz_dict:
        if item[0] in good_answer[1]:
            return borders_from_country_quiz()
    random.shuffle(quiz_dict)
    question = f"{good_answer[0]} {'ont' if good_answer[0].startswith('les') else 'a'} des frontières exclusivement avec {'quel(s)' if choice_with_only_one else 'quels'} pays?"
    return quiz_dict, good_answer, question


def country_from_borders_quiz():
    selection = random_selection(countries_un_member, 3)
    selection_b = random_selection(countries_un_member_and_with_border, 1)
    quiz_dict = []
    if selection_b[0] in selection:
        return country_from_borders_quiz()
    else:
        selection.append(selection_b[0])
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Borders'], country['Article_Nom']])
                break
    length = len(quiz_dict[-1][0])
    borders_list = countries_dict_article_nom[quiz_dict[-1][0][0]]
    if length > 1:
        for elem in range(1, length-1):
            borders_list = borders_list + ", " + countries_dict_article_nom[quiz_dict[-1][0][elem]]
        borders_list = borders_list + " et " + countries_dict_article_nom[quiz_dict[-1][0][-1]]
    quiz_dict[-1][0] = borders_list
    good_answer = quiz_dict[-1]
    for item in quiz_dict:
        if item[1] in good_answer[0]:
            return country_from_borders_quiz()
    random.shuffle(quiz_dict)
    question = f"Quel pays a des frontières exclusivement avec {good_answer[0]}?"
    return quiz_dict, good_answer, question


def population_from_country_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    verification_list = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Preposition_2'], country_population_dict[country['Alpha-2 code']][0]])
                verification_list.append(country_population_dict[country['Alpha-2 code']][1])
                break
    verification_list.sort()
    for i in range(len(verification_list)-1):
        if verification_list[i+1] - verification_list[i] < 15:
            return population_from_country_quiz()
    good_answer = random.choice(quiz_dict)
    question = f"Quelle est la population {good_answer[0]}?"
    return quiz_dict, good_answer, question


def country_from_population_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    verification_list = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country_population_dict[country['Alpha-2 code']][0],country['Article_Nom']])
                verification_list.append(country_population_dict[country['Alpha-2 code']][1])
                break
    verification_list.sort()
    for i in range(len(verification_list)-1):
        if verification_list[i+1] - verification_list[i] < 15:
            return country_from_population_quiz()
    good_answer = random.choice(quiz_dict)
    question = f"Quel pays a une population de {good_answer[0]}?"
    return quiz_dict, good_answer, question


def area_from_country_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    verification_list = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Preposition_2'], country_area_dict[country['Alpha-2 code']][0]])
                verification_list.append(country_area_dict[country['Alpha-2 code']][1])
                break
    verification_list.sort()
    for i in range(len(verification_list)-1):
        if verification_list[i+1] - verification_list[i] < 15:
            return area_from_country_quiz()
    good_answer = random.choice(quiz_dict)
    question = f"Quelle est la superficie {good_answer[0]}?"
    return quiz_dict, good_answer, question


def country_from_area_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    verification_list = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country_area_dict[country['Alpha-2 code']][0],country['Article_Nom']])
                verification_list.append(country_area_dict[country['Alpha-2 code']][1])
                break
    verification_list.sort()
    for i in range(len(verification_list)-1):
        if verification_list[i+1] - verification_list[i] < 15:
            return country_from_area_quiz()
    good_answer = random.choice(quiz_dict)
    question = f"Quel pays a une superficie de {good_answer[0]}?"
    return quiz_dict, good_answer, question


def landlocked_quiz():
    selection_a = random_selection(countries_un_member_and_landlocked, 1)
    selection_b = random_selection(countries_un_member_and_not_landlocked, 3)
    good_answer = [countries_dict_article_nom[selection_a[0]], countries_dict_article_nom[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_article_nom[selection_b[i]], countries_dict_article_nom[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Lequel de ces pays est enclavé?"
    return quiz_dict, good_answer, question


def non_landlocked_quiz():
    selection_a = random_selection(countries_un_member_and_not_landlocked, 1)
    selection_b = random_selection(countries_un_member_and_landlocked, 3)
    good_answer = [countries_dict_article_nom[selection_a[0]], countries_dict_article_nom[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_article_nom[selection_b[i]], countries_dict_article_nom[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Lequel de ces pays n'est pas enclavé?"
    return quiz_dict, good_answer, question


def right_driving_quiz():
    selection_a = random_selection(countries_un_member_and_driving_right, 1)
    selection_b = random_selection(countries_un_member_and_driving_left, 3)
    good_answer = [countries_dict_preposition_1[selection_a[0]], countries_dict_preposition_1[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_preposition_1[selection_b[i]], countries_dict_preposition_1[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Dans lequel de ces pays les automobilistes conduisent-ils à droite?"
    return quiz_dict, good_answer, question


def left_driving_quiz():
    selection_a = random_selection(countries_un_member_and_driving_left, 1)
    selection_b = random_selection(countries_un_member_and_driving_right, 3)
    good_answer = [countries_dict_preposition_1[selection_a[0]], countries_dict_preposition_1[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_preposition_1[selection_b[i]], countries_dict_preposition_1[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Dans lequel de ces pays les automobilistes conduisent-ils à gauche?"
    return quiz_dict, good_answer, question


def subregion_from_country_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Article_Nom'], country['Subregion']])
                break
    verification = dict(quiz_dict)
    if len(list(set(list(verification.values())))) == 4:
        good_answer = random.choice(quiz_dict)
        question = f"{good_answer[0]} est situé dans quelle sous-région?"
        return quiz_dict, good_answer, question
    else:
        return subregion_from_country_quiz()


def country_from_subregion_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Article_Nom'], country['Subregion']])
                break
    verification = dict(quiz_dict)
    if len(list(set(list(verification.values())))) == 4:
        for i in range(len(quiz_dict)):
            temporary = quiz_dict[i][1]
            quiz_dict[i][1] = quiz_dict[i][0]
            quiz_dict[i][0] = temporary
        good_answer = random.choice(quiz_dict)
        question = f"Quel pays est situé en {good_answer[0]}"
        return quiz_dict, good_answer, question
    else:
        return country_from_subregion_quiz()


def north_quiz():
    selection_a = random_selection(countries_un_member_and_north, 1)
    selection_b = random_selection(countries_un_member_and_south, 3)
    good_answer = [countries_dict_article_nom[selection_a[0]], countries_dict_article_nom[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_article_nom[selection_b[i]], countries_dict_article_nom[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Lequel de ces pays est situé dans l'hémisphère nord?"
    return quiz_dict, good_answer, question


def south_quiz():
    selection_a = random_selection(countries_un_member_and_south, 1)
    selection_b = random_selection(countries_un_member_and_north, 3)
    good_answer = [countries_dict_article_nom[selection_a[0]], countries_dict_article_nom[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_article_nom[selection_b[i]], countries_dict_article_nom[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Lequel de ces pays est situé dans l'hémisphère sud?"
    return quiz_dict, good_answer, question


def east_quiz():
    selection_a = random_selection(countries_un_member_and_east, 1)
    selection_b = random_selection(countries_un_member_and_west, 3)
    good_answer = [countries_dict_article_nom[selection_a[0]], countries_dict_article_nom[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_article_nom[selection_b[i]], countries_dict_article_nom[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Lequel de ces pays est situé dans l'hémisphère est?"
    return quiz_dict, good_answer, question


def west_quiz():
    selection_a = random_selection(countries_un_member_and_west, 1)
    selection_b = random_selection(countries_un_member_and_east, 3)
    good_answer = [countries_dict_article_nom[selection_a[0]], countries_dict_article_nom[selection_a[0]]]
    quiz_dict = [good_answer]
    for i in range(len(selection_b)):
        quiz_dict.append([countries_dict_article_nom[selection_b[i]], countries_dict_article_nom[selection_b[i]]])
    random.shuffle(quiz_dict)
    question = "Lequel de ces pays est situé dans l'hémisphère ouest?"
    return quiz_dict, good_answer, question

def flag_from_country_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Preposition_2'], country['Alpha-2 code']])
                break
    good_answer = random.choice(quiz_dict)
    question = f"Quelle est le drapeau {good_answer[0]}?"
    return quiz_dict, good_answer, question


def country_from_flag_quiz():
    selection = random_selection(countries_un_member, 4)
    quiz_dict = []
    for item in selection:
        for country in main_db:
            if country['Alpha-2 code'] == item:
                quiz_dict.append([country['Alpha-2 code'], country['Preposition_2']])
                break
    good_answer = random.choice(quiz_dict)
    question = good_answer[0]
    return quiz_dict, good_answer, question


def random_question(question_choice):
    if question_choice == 0:
        quiz_dict, good_answer, question = capital_from_country_quiz()
    if question_choice == 1:
        quiz_dict, good_answer, question = country_from_capital_quiz()
    if question_choice == 2:
        quiz_dict, good_answer, question = borders_from_country_quiz()
    if question_choice == 3:
        quiz_dict, good_answer, question = country_from_borders_quiz()
    if question_choice == 4:
        quiz_dict, good_answer, question = population_from_country_quiz()
    if question_choice == 5:
        quiz_dict, good_answer, question = country_from_population_quiz()
    if question_choice == 6:
        quiz_dict, good_answer, question = area_from_country_quiz()
    if question_choice == 7:
        quiz_dict, good_answer, question = country_from_area_quiz()
    if question_choice == 8:
        quiz_dict, good_answer, question = landlocked_quiz()
    if question_choice == 9:
        quiz_dict, good_answer, question = non_landlocked_quiz()
    if question_choice == 10:
        quiz_dict, good_answer, question = right_driving_quiz()
    if question_choice == 11:
        quiz_dict, good_answer, question = left_driving_quiz()
    if question_choice == 12:
        quiz_dict, good_answer, question = subregion_from_country_quiz()
    if question_choice == 13:
        quiz_dict, good_answer, question = country_from_subregion_quiz()
    if question_choice == 14:
        quiz_dict, good_answer, question = north_quiz()
    if question_choice == 15:
        quiz_dict, good_answer, question = south_quiz()
    if question_choice == 16:
        quiz_dict, good_answer, question = east_quiz()
    if question_choice == 17:
        quiz_dict, good_answer, question = west_quiz()
    if question_choice == 18:
        quiz_dict, good_answer, question = flag_from_country_quiz()
    if question_choice == 19:
        quiz_dict, good_answer, question = country_from_flag_quiz()
    return quiz_dict, good_answer, question