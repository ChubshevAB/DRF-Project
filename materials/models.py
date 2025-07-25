from django.db import models


class Course(models.Model):
    title = models.CharField(
        verbose_name="Название курса",
        max_length=150,
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        verbose_name="Превью курса",
        blank=True,
        null=True,
        upload_to="materials/previews",
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        max_length=250,
        help_text="Введите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return {self.title}


class Lesson(models.Model):
    title = models.CharField(
        verbose_name="Урок", max_length=150, help_text="Укажите название урока"
    )
    preview = models.ImageField(
        verbose_name="Превью урока",
        blank=True,
        null=True,
        upload_to="materials/previews",
        help_text="Загрузите превью урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        max_length=250,
        help_text="Введите описание урока",
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        null=True,
        blank=True,
        help_text="Укажите ссылку на видео",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return {self.title}
