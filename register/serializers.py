from rest_framework import serializers
from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)  # Nested serializer for choices

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'choices')

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', None)
        question = Question.objects.create(**validated_data)
        if choices_data:
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
        return question
