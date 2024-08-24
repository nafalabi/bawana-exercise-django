from django.db import models
from django_backend.users.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    category = models.CharField(max_length=200)

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Quiz(models.Model):
    filter_category = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question, max_length=10)
    time = models.DurationField(default=0)

class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="quiz_sessions", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    score = models.FloatField(default=None, null=True)

class QuizSessionQuestion(models.Model): # Intentional Redundancy
    session = models.ForeignKey(QuizSession, related_name="session_questions", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    question_text = models.CharField(max_length=200)

class QuizSessionChoice(models.Model): # Intentional Redundancy
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    session_question = models.ForeignKey(QuizSessionQuestion, related_name="session_choices", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    is_chosen = models.BooleanField(default=False)
