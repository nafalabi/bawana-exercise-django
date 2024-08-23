from . import models

def create_question(question_text, choices):
    question = models.Question.objects.create(question_text=question_text)
    for choice_text in choices:
        models.Choice.objects.create(question=question, choice_text=choice_text)
