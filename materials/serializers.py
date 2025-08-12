from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import YouTubeURLValidator
from users.permissions import IsModerator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            'owner': {'read_only': True},
            'video_link': {'validators': [YouTubeURLValidator()]},
        }

    def validate(self, attrs):
        request = self.context.get('request')

        if request and request.method == 'POST':
            if request.user.groups.filter(name="moderators").exists():
                raise serializers.ValidationError(
                    "Модераторы не могут создавать уроки"
                )

        if self.instance and request:
            if not IsModerator().has_permission(request, None):
                if self.instance.owner != request.user:
                    raise serializers.ValidationError(
                        "Вы можете редактировать только свои уроки"
                    )

        return attrs


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(
        many=True,
        read_only=True,
        source="lessons.all"
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def get_lesson_count(self, instance):
        """Возвращает количество уроков в курсе"""
        return instance.lessons.count()

    def validate(self, attrs):
        request = self.context.get('request')

        if request and request.method == 'POST':
            if request.user.groups.filter(name="moderators").exists():
                raise serializers.ValidationError(
                    "Модераторы не могут создавать курсы"
                )

        if self.instance and request:
            if not IsModerator().has_permission(request, None):
                if self.instance.owner != request.user:
                    raise serializers.ValidationError(
                        "Вы можете редактировать только свои курсы"
                    )

        return attrs

    def get_is_subscribed(self, instance):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=instance
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('user', 'subscribed_at')
