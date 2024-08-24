from django.utils import timezone
from . import models

class QuizSessionService:
    @staticmethod
    def startSession(quiz, user):
        session = models.QuizSession.objects.create(quiz=quiz, user=user, start_time=timezone.now())
        questions = models.Question.objects.filter(quiz=quiz)

        for question in questions:
            session_question = models.QuizSessionQuestion.objects.create(
                session=session,
                question=question,
                question_text=question.question_text
            )
            choices = models.Choice.objects.filter(question=question)
            for choice in choices:
                models.QuizSessionChoice.objects.create(
                    session=session,
                    session_question=session_question,
                    question=question,
                    choice=choice,
                    choice_text=choice.choice_text,
                    is_correct=choice.is_correct
                )

        return session

    @staticmethod
    def endSession(session):
        session.end_time = timezone.now()
        session.save()
        return session

    @staticmethod
    def answerQuestion(session, session_question, session_choice):
        models.QuizSessionChoice.objects.filter(
            session_question=session_question
        ).update(is_chosen=False)

        session_choice.is_chosen = True
        session_choice.save()

        return session
