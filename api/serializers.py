# serializers.py
# serializers.py
from rest_framework import serializers
from .models import Quiz, Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    # Remove the 'choices' field from the serializer
    # choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text')  # Remove the 'choices' field from the serializer

    def to_representation(self, instance):
        # Override to_representation method to include choices data
        representation = super().to_representation(instance)
        choices = Choice.objects.filter(question=instance)
        representation['choices'] = ChoiceSerializer(choices, many=True).data
        return representation

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')  # Using QuestionSerializer to serialize related questions

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'code', 'questions')

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            choices_data = question_data.pop('choices', [])
            question = Question.objects.create(quiz=quiz, **question_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
        return quiz
