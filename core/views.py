from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, SchoolForm, ClassYearForm, TeacherForm, SubjectForm, ProgramTermForm
from .models import School, Grade, Attendance, ClassYear, Teacher, Subject, ProgramTerm, Director, Student, Parent
from django.views import View
from .forms import ChildUserForm, ChildStudentForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = user.role
        context['role'] = role
        if role == 'teacher':
            context['grades'] = Grade.objects.filter(teacher__user=user)
            context['attendance'] = Attendance.objects.filter(teacher__user=user)
        elif role == 'parent':
            context['grades'] = Grade.objects.filter(student__parents__user=user)
            context['attendance'] = Attendance.objects.filter(student__parents__user=user)
        elif role == 'student':
            context['grades'] = Grade.objects.filter(student__user=user)
            context['attendance'] = Attendance.objects.filter(student__user=user)
        elif role in ['director', 'admin']:
            context['schools'] = School.objects.all()
            context['grades'] = Grade.objects.all()
            context['attendance'] = Attendance.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class SchoolListView(ListView):
    model = School
    template_name = 'schools/school_list.html'
    context_object_name = 'schools'

@method_decorator(login_required, name='dispatch')
class SchoolCreateView(CreateView):
    model = School
    form_class = SchoolForm
    template_name = 'schools/school_form.html'
    success_url = reverse_lazy('school_list')

@method_decorator(login_required, name='dispatch')
class SchoolUpdateView(UpdateView):
    model = School
    form_class = SchoolForm
    template_name = 'schools/school_form.html'
    success_url = reverse_lazy('school_list')

@method_decorator(login_required, name='dispatch')
class SchoolDeleteView(DeleteView):
    model = School
    template_name = 'schools/school_confirm_delete.html'
    success_url = reverse_lazy('school_list')

@method_decorator(login_required, name='dispatch')
class ClassYearListView(ListView):
    model = ClassYear
    template_name = 'classyears/classyear_list.html'
    context_object_name = 'classyears'

@method_decorator(login_required, name='dispatch')
class ClassYearCreateView(CreateView):
    model = ClassYear
    form_class = ClassYearForm
    template_name = 'classyears/classyear_form.html'
    success_url = reverse_lazy('classyear_list')

@method_decorator(login_required, name='dispatch')
class ClassYearUpdateView(UpdateView):
    model = ClassYear
    form_class = ClassYearForm
    template_name = 'classyears/classyear_form.html'
    success_url = reverse_lazy('classyear_list')

@method_decorator(login_required, name='dispatch')
class ClassYearDeleteView(DeleteView):
    model = ClassYear
    template_name = 'classyears/classyear_confirm_delete.html'
    success_url = reverse_lazy('classyear_list')

@method_decorator(login_required, name='dispatch')
class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'

@method_decorator(login_required, name='dispatch')
class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')

@method_decorator(login_required, name='dispatch')
class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')

@method_decorator(login_required, name='dispatch')
class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')

@method_decorator(login_required, name='dispatch')
class SubjectListView(ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'

@method_decorator(login_required, name='dispatch')
class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subject_list')

@method_decorator(login_required, name='dispatch')
class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subject_list')

@method_decorator(login_required, name='dispatch')
class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

@method_decorator(login_required, name='dispatch')
class ProgramTermListView(ListView):
    model = ProgramTerm
    template_name = 'terms/term_list.html'
    context_object_name = 'terms'

@method_decorator(login_required, name='dispatch')
class ProgramTermCreateView(CreateView):
    model = ProgramTerm
    form_class = ProgramTermForm
    template_name = 'terms/term_form.html'
    success_url = reverse_lazy('term_list')

@method_decorator(login_required, name='dispatch')
class ProgramTermUpdateView(UpdateView):
    model = ProgramTerm
    form_class = ProgramTermForm
    template_name = 'terms/term_form.html'
    success_url = reverse_lazy('term_list')

@method_decorator(login_required, name='dispatch')
class ProgramTermDeleteView(DeleteView):
    model = ProgramTerm
    template_name = 'terms/term_confirm_delete.html'
    success_url = reverse_lazy('term_list')

from .models import Director, Student, Parent, Grade, Attendance
from .forms import DirectorForm, StudentForm, ParentForm, GradeForm, AttendanceForm

# Director CRUD
@method_decorator(login_required, name='dispatch')
class DirectorListView(ListView):
    model = Director
    template_name = 'directors/director_list.html'
    context_object_name = 'directors'

@method_decorator(login_required, name='dispatch')
class DirectorCreateView(CreateView):
    model = Director
    form_class = DirectorForm
    template_name = 'directors/director_form.html'
    success_url = reverse_lazy('director_list')

@method_decorator(login_required, name='dispatch')
class DirectorUpdateView(UpdateView):
    model = Director
    form_class = DirectorForm
    template_name = 'directors/director_form.html'
    success_url = reverse_lazy('director_list')

@method_decorator(login_required, name='dispatch')
class DirectorDeleteView(DeleteView):
    model = Director
    template_name = 'directors/director_confirm_delete.html'
    success_url = reverse_lazy('director_list')

# Student CRUD
@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

@method_decorator(login_required, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

@method_decorator(login_required, name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

@method_decorator(login_required, name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

# Parent CRUD
@method_decorator(login_required, name='dispatch')
class ParentListView(ListView):
    model = Parent
    template_name = 'parents/parent_list.html'
    context_object_name = 'parents'

@method_decorator(login_required, name='dispatch')
class ParentCreateView(CreateView):
    model = Parent
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')

@method_decorator(login_required, name='dispatch')
class ParentUpdateView(UpdateView):
    model = Parent
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')

@method_decorator(login_required, name='dispatch')
class ParentDeleteView(DeleteView):
    model = Parent
    template_name = 'parents/parent_confirm_delete.html'
    success_url = reverse_lazy('parent_list')

# Grade CRUD
from .models import Grade
from .forms import GradeForm

@method_decorator(login_required, name='dispatch')
class GradeListView(ListView):
    model = Grade
    template_name = 'grades/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'teacher':
            return qs.filter(teacher__user=self.request.user)
        if self.request.user.role == 'parent':
            return qs.filter(student__parents__user=self.request.user)
        if self.request.user.role == 'student':
            return qs.filter(student__user=self.request.user)
        return qs  # director/admin see all

@method_decorator(login_required, name='dispatch')
class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grades/grade_form.html'
    success_url = reverse_lazy('grade_list')

@method_decorator(login_required, name='dispatch')
class GradeUpdateView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grades/grade_form.html'
    success_url = reverse_lazy('grade_list')

@method_decorator(login_required, name='dispatch')
class GradeDeleteView(DeleteView):
    model = Grade
    template_name = 'grades/grade_confirm_delete.html'
    success_url = reverse_lazy('grade_list')

# Attendance CRUD
from .models import Attendance
from .forms import AttendanceForm

@method_decorator(login_required, name='dispatch')
class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendance'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'teacher':
            return qs.filter(teacher__user=self.request.user)
        if self.request.user.role == 'parent':
            return qs.filter(student__parents__user=self.request.user)
        if self.request.user.role == 'student':
            return qs.filter(student__user=self.request.user)
        return qs

@method_decorator(login_required, name='dispatch')
class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

@method_decorator(login_required, name='dispatch')
class AttendanceUpdateView(UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

@method_decorator(login_required, name='dispatch')
class AttendanceDeleteView(DeleteView):
    model = Attendance
    template_name = 'attendance/attendance_confirm_delete.html'
    success_url = reverse_lazy('attendance_list')

class ParentAddChildView(LoginRequiredMixin, View):
    template_name = 'parents/parent_add_child.html'

    def get(self, request):
        user_form = ChildUserForm()
        student_form = ChildStudentForm()
        return render(request, self.template_name, {'user_form': user_form, 'student_form': student_form})

    def post(self, request):
        user_form = ChildUserForm(request.POST)
        student_form = ChildStudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            # create child user
            child_user = user_form.save(commit=False)
            child_user.role = 'student'
            child_user.save()
            # create student profile
            child_profile = student_form.save(commit=False)
            child_profile.user = child_user
            child_profile.save()
            # link to parent
            parent_profile = Parent.objects.get(user=request.user)
            parent_profile.children.add(child_profile)
            return redirect('parent_list')
        return render(request, self.template_name, {'user_form': user_form, 'student_form': student_form})
