from django_backend.users import serializers as user_serializers
from django.utils import timezone
from .models import *
from rest_framework import serializers

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct']

class QuestionPayloadSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'category', 'choices']
        read_only_fields = ['id']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data, pub_date=timezone.now())

        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)

        return question

    def update(self, instance, validated_data):
        # Update the Question instance
        instance.question_text = validated_data.get('question_text', instance.question_text)
        instance.category = validated_data.get('category', instance.category)
        instance.save()

        # Clear existing choices
        instance.choices.all().delete()

        # Create new choices
        choices_data = validated_data.get('choices', [])
        for choice_data in choices_data:
            Choice.objects.create(question=instance, **choice_data)

        return instance

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id','filter_category', 'questions', 'time']
        read_only_fields = ['id']
        depth = 1
        extra_kwargs = {
            'questions': {'required': False}  # Makes the 'questions' field optional
        }

    def __init__(self, *args, **kwargs):
        depth = kwargs.pop('depth', 1)
        super(QuizSerializer, self).__init__(*args, **kwargs)

        self.Meta.depth = depth

    def create(self, validated_data):
        validated_data.pop('questions', None)
        quiz = Quiz.objects.create(**validated_data)

        questions_data = Question.objects.filter(category__icontains=quiz.filter_category).order_by('?')[0:10]

        quiz.questions.add(*questions_data)
        quiz.save()

        return quiz

    def update(self, instance, validated_data):
        instance.filter_category = validated_data.get('filter_category', instance.filter_category)
        instance.time = validated_data.get('time', instance.time)
        instance.save()

        return instance

    def resetQuestions(self):
        instance = self.instance
        instance.questions.clear()

        questions_data = Question.objects.filter(category__icontains=instance.filter_category).order_by('?')[0:10]

        instance.questions.add(*questions_data)
        instance.save()

        return instance


class QuizSessionSerializer(serializers.ModelSerializer):
    user = user_serializers.UserSerializer()
    quiz = QuizSerializer(depth=0)

    class Meta:
        model = QuizSession
        fields = ['id', 'quiz', 'user', 'start_time', 'end_time', 'score']
        read_only_fields = ['id', 'start_time', 'end_time', 'score']
        depth = 1

class QuizSessionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSessionChoice
        fields = ['id', 'choice_text', 'is_chosen']
        read_only_fields = ['id', 'choice_text']

class QuizSessionQuestionSerializer(serializers.ModelSerializer):
    session_choices = QuizSessionChoiceSerializer(many=True)
    class Meta:
        model = QuizSessionQuestion
        fields = ['id', 'question_text', 'session_choices']
        read_only_fields = ['id', 'question_text']
        # exclude = ['session', 'question']
        depth = 1
