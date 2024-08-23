from django.utils import timezone
from .models import Question, Choice
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

