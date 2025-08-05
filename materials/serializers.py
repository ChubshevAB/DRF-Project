from rest_framework import serializers
from materials.models import Course, Lesson
from users.permissions import IsModerator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {"owner": {"read_only": True}}

    def validate(self, attrs):
        if self.instance and not IsModerator().has_permission(
            self.context["request"], None
        ):
            if self.instance.owner != self.context["request"].user:
                raise serializers.ValidationError(
                    "Вы можете редактировать только свои уроки"
                )
        return attrs


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lessons.all")

    class Meta:
        model = Course
        fields = "__all__"
        extra_kwargs = {"owner": {"read_only": True}}

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    def validate(self, attrs):
        if self.instance and not IsModerator().has_permission(
            self.context["request"], None
        ):
            if self.instance.owner != self.context["request"].user:
                raise serializers.ValidationError(
                    "Вы можете редактировать только свои курсы"
                )
        return attrs
