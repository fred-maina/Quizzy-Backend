from rest_framework import serializers
from .models import Quiz, Question, Choice, Score


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'quiz')

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'created_by')

    def create(self, validated_data):
        quiz = Quiz.objects.create(**validated_data)
        return quiz


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        models = Score
        fields = ('user', 'score', 'quiz')
    def create(self, validated_data):
        score = Score.objects.create(**validated_data)
        return score


