import time
from os import path
from datetime import date
from django.shortcuts import render, redirect
from Quiz.questions import *

# Create your views here.
max_points_by_question = 20
time_limit = 20
nb_question_type = 20


def index(request):
    if request.method == 'POST':
        request.session['initial_question_choice'] = list(map(int, request.POST.getlist('questions_type[]')))
        username = request.POST["username"]
        if username.isalnum():
            if 0 < len(username) < 50:
                if not request.session['initial_question_choice']:
                    return render(request, "Quiz/index.html", context={'error_2': True})
                request.session['username'] = username
                request.session['lifes'] = 3
                request.session['points'] = 0
                request.session['question_number'] = 1
                request.session['quiz_key'] = True
                request.session['answer_key'] = False
                request.session['leaderboard_key'] = False
                request.session['question_choice'] = request.session['initial_question_choice']*5
                return redirect('quiz/')
        return render(request, "Quiz/index.html", context={'error_1': True})
    return render(request, "Quiz/index.html")


def quiz(request):
    if request.session['quiz_key']:
        request.session['quiz_key'] = False
        if request.session['lifes'] == 0:
            request.session['leaderboard_key'] = True
            return redirect('../leaderboard/')
        if not request.session['question_choice']:
            request.session['question_choice'] = request.session['initial_question_choice']*5
        random.shuffle(request.session['question_choice'])
        question_type = request.session['question_choice'].pop()
        request.session['quiz_dict'], request.session['good_answer'], request.session['question'] = random_question(question_type)
        context = {'quiz_dict': request.session['quiz_dict'],
                    'question': request.session['question'],
                    'lifes': request.session['lifes'],
                    'points': request.session['points'],
                    'question_number': request.session['question_number']}
        request.session['timer'] = time.time()
        request.session['answer_key'] = True
        return render(request, "Quiz/quiz.html", context=context)


def answer(request):
    if request.method == 'POST' and request.session['answer_key']:
        request.session['answer_key'] = False
        answer = request.POST["answer"]
        if answer == request.session['good_answer'][1]:
            delta_time = time.time() - request.session['timer']
            points_to_add = 0
            if delta_time < time_limit:
                points_to_add = int((time_limit - delta_time) / time_limit * max_points_by_question)
                request.session['points'] += points_to_add
            answer_is_good = True
        else:
            points_to_add = 0
            request.session['lifes'] -= 1
            answer_is_good = False
        context = {'quiz_dict': request.session['quiz_dict'],
                   'question': request.session['question'],
                   'lifes': request.session['lifes'],
                   'points': request.session['points'],
                   'question_number': request.session['question_number'],
                   'answer': answer,
                   'points_to_add': points_to_add,
                   'answer_is_good': answer_is_good,
                   'good_answer': request.session['good_answer'][1]}
        request.session['quiz_key'] = True
        request.session['question_number'] += 1
        return render(request, "Quiz/answer.html", context=context)


def leaderboard(request):
    if request.session['leaderboard_key']:
        request.session['leaderboard_key'] = False
        today = date.today()
        if not path.exists("src/Quiz/leaderboard_db.json"):
            with open("src/Quiz/leaderboard_db.json", "w") as json_file:
                current_position = 0
                leaderboard = [[1, request.session['username'], request.session['points'], today.strftime("%Y-%m-%d"), current_position]]
                json.dump(leaderboard, json_file, indent=4)
        else:
            with open("src/Quiz/leaderboard_db.json", "r") as json_file:
                leaderboard = json.load(json_file)
            position_list = []
            for i in range(len(leaderboard)):
                position_list.append(leaderboard[i][4])
            last_position = max(position_list)
            current_position = last_position + 1
            leaderboard.append([0, request.session['username'], request.session['points'], today.strftime("%Y-%m-%d"), current_position])
            leaderboard.sort(key=itemgetter(2), reverse=True)
            for i in range(len(leaderboard)):
                leaderboard[i][0] = i+1
                if leaderboard[i][4] == current_position:
                    current_rank = leaderboard[i][0]
            with open("src/Quiz/leaderboard_db.json", "w") as json_file:
                json.dump(leaderboard, json_file, indent=4)

        return render(request, "Quiz/leaderboard.html", context={'leaderboard': leaderboard, 'current_position': current_position, 'current_rank': current_rank})


def leaderboard_view(request):
    if path.exists("src/Quiz/leaderboard_db.json"):
        with open("src/Quiz/leaderboard_db.json", "r") as json_file:
            leaderboard = json.load(json_file)
    return render(request, "Quiz/leaderboard-view.html", context={'leaderboard': leaderboard})