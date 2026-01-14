from django.db import models

class Courses(models.Model):
    title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    duration_minutes = models.PositiveIntegerField(
        help_text="Total course duration in minutes"
    )

    is_active = models.BooleanField(default=True)

    image = models.ImageField(upload_to="course_images/")

    video_url = models.URLField(
        max_length=1000,
        help_text="YouTube video link for this course"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course_code} - {self.title}"

    def formatted_duration(self):
        minutes = self.duration_minutes
        days = minutes // (24 * 60)
        hours = (minutes % (24 * 60)) // 60
        mins = minutes % 60

        parts = []
        if days:
            parts.append(f"{days} day{'s' if days > 1 else ''}")
        if hours:
            parts.append(f"{hours} hr{'s' if hours > 1 else ''}")
        if mins:
            parts.append(f"{mins} min")

        return " ".join(parts)
