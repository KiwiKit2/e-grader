from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, School, ClassYear, Teacher, Subject, ProgramTerm, Director, Student, Parent, Grade, Attendance, TeachingAssignment

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address']

class ClassYearForm(forms.ModelForm):
    class Meta:
        model = ClassYear
        fields = ['school', 'level', 'section']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'school', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class ProgramTermForm(forms.ModelForm):
    class Meta:
        model = ProgramTerm
        fields = ['school', 'name', 'start_date', 'end_date', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['user', 'school']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'school', 'class_year']

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['user', 'children']
        widgets = {'children': forms.CheckboxSelectMultiple}

class GradeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'teacher':
            from .models import Teacher, Student
            teacher = Teacher.objects.get(user=user)
            # only subjects the teacher teaches
            self.fields['subject'].queryset = teacher.subjects.all()
            # only students from this teacher's classes
            self.fields['student'].queryset = Student.objects.filter(school=teacher.school)
            # restrict and hide teacher field
            self.fields['teacher'].queryset = Teacher.objects.filter(user=user)
            self.fields['teacher'].widget = forms.HiddenInput()
            # set initial teacher so hidden field is not empty
            self.initial['teacher'] = teacher
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'teacher', 'term', 'value']
        widgets = {'student': forms.Select, 'subject': forms.Select,
                   'teacher': forms.Select, 'term': forms.Select}

class AttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'teacher':
            from .models import Teacher, Student
            teacher = Teacher.objects.get(user=user)
            self.fields['subject'].queryset = teacher.subjects.all()
            self.fields['student'].queryset = Student.objects.filter(school=teacher.school)
            # restrict and hide teacher field
            self.fields['teacher'].queryset = Teacher.objects.filter(user=user)
            self.fields['teacher'].widget = forms.HiddenInput()
            # set initial teacher so hidden field is not empty
            self.initial['teacher'] = teacher
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'teacher', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select
        }

class ChildUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ChildStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('school', 'class_year')
        widgets = {
            'class_year': forms.Select,
        }

class TeachingAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeachingAssignment
        fields = ['term', 'teacher', 'subject']
