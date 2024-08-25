from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status, authentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from django_backend.quiz.serializers import *
from django_backend.quiz.models import *
from django_backend.quiz.services import *

class QuestionViewSet(viewsets.ViewSet):
    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        category = request.query_params.get('category', None)

        if category:
            questions = Question.objects.filter(category__icontains=category)
        else:
            questions = Question.objects.all()

        paginator = PageNumberPagination()
        paginated_questions = paginator.paginate_queryset(questions, request)

        serializer = QuestionPayloadSerializer(paginated_questions, many=True)

        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = QuestionPayloadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionPayloadSerializer(question, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response({'message': 'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class QuizViewSet(viewsets.ViewSet):
    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        quizs = Quiz.objects.all()

        paginator = PageNumberPagination()
        paginated_questions = paginator.paginate_queryset(quizs, request)

        serializer = QuizSerializer(paginated_questions, many=True, depth=0)

        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        quizpayload = request.data
        serializer = QuizSerializer(data=quizpayload)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # Retrieve a specific quiz
        quiz = get_object_or_404(Quiz, pk=pk)
        serializer = QuizSerializer(quiz, depth=1)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Update a specific quiz
        quiz = get_object_or_404(Quiz, pk=pk)
        serializer = QuizSerializer(quiz, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        quiz = get_object_or_404(Quiz, pk=pk)
        serializer = QuizSerializer(quiz, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        quiz = get_object_or_404(Quiz, pk=pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def reset_questions(self, request, pk=None):
        quiz = get_object_or_404(Quiz, pk=pk)
        serializer = QuizSerializer(quiz)
        serializer.resetQuestions()

        return Response(serializer.data, status=status.HTTP_200_OK)

class QuizSessionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        quiz_sessions = QuizSession.objects.filter(user=user)

        paginator = PageNumberPagination()
        paginated_sessions = paginator.paginate_queryset(quiz_sessions, request)

        serializer = QuizSessionSerializer(paginated_sessions, many=True)

        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        quiz_session = get_object_or_404(QuizSession, pk=pk)
        serializer = QuizSessionSerializer(quiz_session)
        data = serializer.data

        questions = QuizSessionQuestion.objects.filter(session=quiz_session).order_by('id')
        serialized_questions = QuizSessionQuestionSerializer(questions, many=True)

        data['session_questions'] = serialized_questions.data

        return Response(data)


    def create(self, request):
        user = request.user

        quiz_id = request.data.get('quiz_id')

        if not quiz_id:
            return Response({'error': 'quiz_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        quiz = get_object_or_404(Quiz, id=quiz_id)

        quiz_session = QuizSessionService.startSession(quiz, user)

        serializer = QuizSessionSerializer(quiz_session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def answer_question(self, request, pk=None):
        user = request.user
        quiz_session = get_object_or_404(QuizSession, id=pk)

        if quiz_session.user != user:
            return Response(
                {'error': 'You are not authorized to answer this quiz session'},
                status=status.HTTP_403_FORBIDDEN
            )

        question_id = request.data.get('question_id')
        choice_id = request.data.get('choice_id')

        if not question_id or not choice_id:
            return Response(
                {'error': 'question_id and choice_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session_question = get_object_or_404(QuizSessionQuestion, id=question_id)
        session_choice = get_object_or_404(QuizSessionChoice, id=choice_id)

        QuizSessionService.answerQuestion(quiz_session, session_question, session_choice)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        user = request.user
        quiz_session = get_object_or_404(QuizSession, id=pk)

        if quiz_session.user != user:
            return Response(
                {'error': 'You are not authorized to end this quiz session'},
                status=status.HTTP_403_FORBIDDEN
            )

        QuizSessionService.endSession(quiz_session)

        return Response(status=status.HTTP_200_OK)
