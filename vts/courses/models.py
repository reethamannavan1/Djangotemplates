from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Course(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="courses/")
    duration = models.CharField(max_length=50)
    level = models.CharField(max_length=100)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    certification = models.CharField(max_length=100, blank=True)
  

    preview_image = models.ImageField(upload_to="course_preview/", blank=True, null=True)
    preview_video = models.FileField(upload_to="course_videos/", blank=True, null=True)


    detail_title = models.CharField(max_length=250, blank=True)
    detail_description = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    MODE_CHOICES = (
    ("online", "Online"),
    ("offline", "Offline"),
)

    available_modes = models.JSONField(default=list, blank=True)




    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title




#coursetechnology
class CourseTechnology(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="technologies"
    )
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="course_tech_icons/")

    def __str__(self):
        return f"{self.course.title} - {self.name}"



#courselearning
class CourseLearning(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="learning_points"
    )
    point = models.CharField(max_length=255)

    def __str__(self):
        return self.point




#Enrollment
class Enrollment(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    MODE_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=10)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

    mode = models.CharField(max_length=10, choices=MODE_CHOICES)

    message = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    razorpay_order_id = models.CharField(max_length=200, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True)
    razorpay_signature = models.CharField(max_length=200, blank=True)

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.course.title}"
