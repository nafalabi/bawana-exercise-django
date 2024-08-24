from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from django_backend.quiz.serializers import *
from django_backend.quiz.models import *

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
