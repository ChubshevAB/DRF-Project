from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ("title", "description")


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField
    lessons = LessonSerializer(many=True, read_only=True, source="lessons.all")

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, instance):
        return instance.lessons.count()
