from django.db import models
from django.contrib.auth.models import AbstractUser

# User roles choices
ROLE_CHOICES = [
    ('admin', 'Administrator'),
    ('director', 'Director'),
    ('teacher', 'Teacher'),
    ('parent', 'Parent'),
    ('student', 'Student'),
]

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# School model
typical_class_levels = [(i, f"Grade {i}") for i in range(1, 13)]

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class ClassYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    level = models.IntegerField(choices=typical_class_levels)
    section = models.CharField(max_length=5, blank=True)

    def __str__(self):
        sec = f" {self.section}" if self.section else ''
        return f"{self.school.name} - {self.get_level_display()}{sec}"

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProgramTerm(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    subjects = models.ManyToManyField(Subject, related_name='terms')

    def __str__(self):
        return f"{self.school.name} - {self.name}"

class Director(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.OneToOneField(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"Director: {self.user.get_full_name()} ({self.school.name})"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_year = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name()}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField(Student, related_name='parents')

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    term = models.ForeignKey(ProgramTerm, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Grade: {self.student}: {self.subject} = {self.value}"

ATTENDANCE_STATUS = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
]

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)

    def __str__(self):
        return f"{self.date} - {self.student}: {self.status}"
