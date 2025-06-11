from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import User, School, ClassYear, Subject, ProgramTerm, Director, Teacher, Student, Parent, Grade, Attendance

class CoreModelsAndViewsTest(TestCase):
    def setUp(self):
        # Create school and related data
        self.school = School.objects.create(name='Test School', address='123 Test Ave')
        self.class_year = ClassYear.objects.create(school=self.school, level=5, section='A')
        self.subject = Subject.objects.create(name='Mathematics')
        self.term = ProgramTerm.objects.create(
            school=self.school,
            name='Term1',
            start_date=timezone.now().date(),
            end_date=timezone.now().date()
        )
        self.term.subjects.add(self.subject)

        # Create users for roles
        self.teacher_user = User.objects.create_user(username='teach', password='pass', role='teacher')
        self.parent_user = User.objects.create_user(username='par', password='pass', role='parent')
        self.student_user = User.objects.create_user(username='stu', password='pass', role='student')
        self.director_user = User.objects.create_user(username='dir', password='pass', role='director')
        self.admin_user = User.objects.create_user(username='adm', password='pass', role='admin')

        # Create role-specific profiles
        self.director = Director.objects.create(user=self.director_user, school=self.school)
        self.teacher = Teacher.objects.create(user=self.teacher_user, school=self.school)
        self.teacher.subjects.add(self.subject)
        self.student = Student.objects.create(user=self.student_user, school=self.school, class_year=self.class_year)
        self.parent = Parent.objects.create(user=self.parent_user)
        self.parent.children.add(self.student)

        # Create grade and attendance
        self.grade = Grade.objects.create(
            student=self.student, subject=self.subject,
            teacher=self.teacher, term=self.term, value=85
        )
        self.attendance = Attendance.objects.create(
            student=self.student, subject=self.subject,
            teacher=self.teacher, date=timezone.now().date(), status='present'
        )

    def test_str_methods(self):
        # Test __str__ outputs
        self.assertIn('Teacher:', str(self.teacher))
        self.assertIn('Student:', str(self.student))
        self.assertIn('Parent:', str(self.parent))
        self.assertIn('Director:', str(self.director))
        self.assertEqual(str(self.school), 'Test School')
        self.assertIn('Grade', str(self.grade))
        self.assertIn('present', str(self.attendance))

    def test_dashboard_teacher(self):
        self.client.login(username='teach', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Grades')
        self.assertContains(response, 'Mathematics')

    def test_dashboard_parent(self):
        self.client.login(username='par', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Children Grades')
        self.assertContains(response, 'Mathematics')

    def test_dashboard_student(self):
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Grades')
        self.assertContains(response, '85')

    def test_dashboard_director(self):
        self.client.login(username='dir', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Schools')
        self.assertContains(response, 'Test School')

    def test_dashboard_admin(self):
        self.client.login(username='adm', password='pass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Schools')
        self.assertContains(response, 'Test School')

class SchoolCRUDTests(TestCase):
    def setUp(self):
        # Create a user and initial school
        self.user = User.objects.create_user(username='user1', password='pass', role='teacher')
        self.school = School.objects.create(name='Init School', address='Addr 1')

    def test_school_list_view(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('school_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Init School')

    def test_school_create_view(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(reverse('school_add'), {'name': 'New School', 'address': 'New Addr'})
        self.assertRedirects(response, reverse('school_list'))
        self.assertTrue(School.objects.filter(name='New School').exists())

    def test_school_update_view(self):
        self.client.login(username='user1', password='pass')
        url = reverse('school_edit', kwargs={'pk': self.school.pk})
        response = self.client.post(url, {'name': 'Updated School', 'address': 'Addr 1'})
        self.assertRedirects(response, reverse('school_list'))
        self.school.refresh_from_db()
        self.assertEqual(self.school.name, 'Updated School')

    def test_school_delete_view(self):
        self.client.login(username='user1', password='pass')
        url = reverse('school_delete', kwargs={'pk': self.school.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('school_list'))
        self.assertFalse(School.objects.filter(pk=self.school.pk).exists())

class DirectorCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u', 'u@u.com', 'pass', role='admin')
        self.school = School.objects.create(name='S', address='A')
    def test_director_crud(self):
        self.client.login(username='u', password='pass')
        # Create
        resp = self.client.post(reverse('director_add'), {'user': self.user.pk, 'school': self.school.pk})
        self.assertRedirects(resp, reverse('director_list'))
        d = Director.objects.get(user=self.user)
        # List
        resp = self.client.get(reverse('director_list'))
        self.assertContains(resp, d.user.get_username())
        # Update
        resp = self.client.post(reverse('director_edit', kwargs={'pk': d.pk}), {'user': self.user.pk, 'school': self.school.pk})
        self.assertRedirects(resp, reverse('director_list'))
        # Delete
        resp = self.client.post(reverse('director_delete', kwargs={'pk': d.pk}))
        self.assertRedirects(resp, reverse('director_list'))
        self.assertFalse(Director.objects.filter(pk=d.pk).exists())

class SubjectCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u2', 'u2@u.com', 'pass', role='admin')
    def test_subject_crud(self):
        self.client.login(username='u2', password='pass')
        # Create
        resp = self.client.post(reverse('subject_add'), {'name': 'Subj'})
        self.assertRedirects(resp, reverse('subject_list'))
        s = Subject.objects.get(name='Subj')
        # List
        resp = self.client.get(reverse('subject_list'))
        self.assertContains(resp, 'Subj')
        # Update
        resp = self.client.post(reverse('subject_edit', kwargs={'pk': s.pk}), {'name': 'Subj2'})
        self.assertRedirects(resp, reverse('subject_list'))
        s.refresh_from_db()
        self.assertEqual(s.name, 'Subj2')
        # Delete
        resp = self.client.post(reverse('subject_delete', kwargs={'pk': s.pk}))
        self.assertRedirects(resp, reverse('subject_list'))
        self.assertFalse(Subject.objects.filter(pk=s.pk).exists())

class ClassYearCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u3', 'u3@u.com', 'pass', role='admin')
        self.school = School.objects.create(name='CS', address='Addr')
    def test_classyear_crud(self):
        self.client.login(username='u3', password='pass')
        # Create
        data = {'school': self.school.pk, 'level': 1, 'section': 'A'}
        resp = self.client.post(reverse('classyear_add'), data)
        self.assertRedirects(resp, reverse('classyear_list'))
        cy = ClassYear.objects.get(school=self.school)
        # List
        resp = self.client.get(reverse('classyear_list'))
        self.assertContains(resp, 'Grade 1')
        # Update
        resp = self.client.post(reverse('classyear_edit', kwargs={'pk': cy.pk}), {'school': self.school.pk, 'level': 2, 'section': 'B'})
        self.assertRedirects(resp, reverse('classyear_list'))
        cy.refresh_from_db()
        self.assertEqual(cy.level, 2)
        # Delete
        resp = self.client.post(reverse('classyear_delete', kwargs={'pk': cy.pk}))
        self.assertRedirects(resp, reverse('classyear_list'))
        self.assertFalse(ClassYear.objects.filter(pk=cy.pk).exists())

class TeacherCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u4', 'u4@u.com', 'pass', role='admin')
        self.school = School.objects.create(name='TS', address='Addr')
        self.subj = Subject.objects.create(name='Math')
    def test_teacher_crud(self):
        self.client.login(username='u4', password='pass')
        # Create
        data = {'user': self.user.pk, 'school': self.school.pk, 'subjects': [self.subj.pk]}
        resp = self.client.post(reverse('teacher_add'), data)
        self.assertRedirects(resp, reverse('teacher_list'))
        t = Teacher.objects.get(user=self.user)
        # List
        resp = self.client.get(reverse('teacher_list'))
        self.assertContains(resp, self.user.get_username())
        # Update
        resp = self.client.post(reverse('teacher_edit', kwargs={'pk': t.pk}), data)
        self.assertRedirects(resp, reverse('teacher_list'))
        # Delete
        resp = self.client.post(reverse('teacher_delete', kwargs={'pk': t.pk}))
        self.assertRedirects(resp, reverse('teacher_list'))
        self.assertFalse(Teacher.objects.filter(pk=t.pk).exists())

class ProgramTermCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u5', 'u5@u.com', 'pass', role='admin')
        self.school = School.objects.create(name='TS', address='Addr')
        self.subj = Subject.objects.create(name='Sci')
    def test_term_crud(self):
        self.client.login(username='u5', password='pass')
        data = {'school': self.school.pk, 'name': 'TermX', 'start_date': '2025-01-01', 'end_date': '2025-06-01', 'subjects': [self.subj.pk]}
        resp = self.client.post(reverse('term_add'), data)
        self.assertRedirects(resp, reverse('term_list'))
        term = ProgramTerm.objects.get(name='TermX')
        # List
        resp = self.client.get(reverse('term_list'))
        self.assertContains(resp, 'TermX')
        # Update
        data['name'] = 'TermY'
        resp = self.client.post(reverse('term_edit', kwargs={'pk': term.pk}), data)
        self.assertRedirects(resp, reverse('term_list'))
        term.refresh_from_db()
        self.assertEqual(term.name, 'TermY')
        # Delete
        resp = self.client.post(reverse('term_delete', kwargs={'pk': term.pk}))
        self.assertRedirects(resp, reverse('term_list'))
        self.assertFalse(ProgramTerm.objects.filter(pk=term.pk).exists())

class StudentCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u6', 'u6@u.com', 'pass', role='admin')
        self.school = School.objects.create(name='ST', address='Addr')
        self.cy = ClassYear.objects.create(school=self.school, level=3, section='C')
    def test_student_crud(self):
        self.client.login(username='u6', password='pass')
        data = {'user': self.user.pk, 'school': self.school.pk, 'class_year': self.cy.pk}
        resp = self.client.post(reverse('student_add'), data)
        self.assertRedirects(resp, reverse('student_list'))
        st = Student.objects.get(user=self.user)
        # List
        resp = self.client.get(reverse('student_list'))
        self.assertContains(resp, self.user.get_username())
        # Update
        resp = self.client.post(reverse('student_edit', kwargs={'pk': st.pk}), data)
        self.assertRedirects(resp, reverse('student_list'))
        # Delete
        resp = self.client.post(reverse('student_delete', kwargs={'pk': st.pk}))
        self.assertRedirects(resp, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=st.pk).exists())

class ParentCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u7', 'u7@u.com', 'pass', role='admin')
        self.school = School.objects.create(name='PT', address='Addr')
        self.cy = ClassYear.objects.create(school=self.school, level=4, section='D')
        self.child_user = User.objects.create_user('c', 'c@c.com', 'pass', role='student')
        self.child = Student.objects.create(user=self.child_user, school=self.school, class_year=self.cy)
    def test_parent_crud(self):
        self.client.login(username='u7', password='pass')
        data = {'user': self.user.pk, 'children': [self.child.pk]}
        resp = self.client.post(reverse('parent_add'), data)
        self.assertRedirects(resp, reverse('parent_list'))
        p = Parent.objects.get(user=self.user)
        # List
        resp = self.client.get(reverse('parent_list'))
        self.assertContains(resp, self.user.get_username())
        # Update
        resp = self.client.post(reverse('parent_edit', kwargs={'pk': p.pk}), data)
        self.assertRedirects(resp, reverse('parent_list'))
        # Delete
        resp = self.client.post(reverse('parent_delete', kwargs={'pk': p.pk}))
        self.assertRedirects(resp, reverse('parent_list'))
        self.assertFalse(Parent.objects.filter(pk=p.pk).exists())

class ParentAddChildTests(TestCase):
    def setUp(self):
        # create parent user and profile
        self.parent_user = User.objects.create_user('puser', password='pass', role='parent')
        self.parent_profile = Parent.objects.create(user=self.parent_user)
        # setup school and class
        self.school = School.objects.create(name='PS', address='Addr')
        self.class_year = ClassYear.objects.create(school=self.school, level=2, section='A')

    def test_get_add_child(self):
        self.client.login(username='puser', password='pass')
        response = self.client.get(reverse('parent_add_child'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Child')
    
    def test_post_add_child(self):
        self.client.login(username='puser', password='pass')
        data = {
            'username': 'child1',
            'first_name': 'Child',
            'last_name': 'One',
            'email': 'child1@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'school': self.school.pk,
            'class_year': self.class_year.pk,
        }
        response = self.client.post(reverse('parent_add_child'), data)
        # redirect to parent_list
        self.assertRedirects(response, reverse('parent_list'))
        # child user created
        child_user = User.objects.get(username='child1')
        self.assertEqual(child_user.role, 'student')
        # student profile created
        student_profile = Student.objects.get(user=child_user)
        self.assertEqual(student_profile.school, self.school)
        self.assertEqual(student_profile.class_year, self.class_year)
        # linked to parent
        self.assertIn(student_profile, self.parent_profile.children.all())

class PermissionTests(TestCase):
    def setUp(self):
        # common setup
        self.school = School.objects.create(name='Perm School', address='Addr')
        self.term = ProgramTerm.objects.create(
            school=self.school, name='PermTerm',
            start_date=timezone.now().date(), end_date=timezone.now().date()
        )
        self.subject = Subject.objects.create(name='PermSubj')
        self.term.subjects.add(self.subject)
        # users
        self.teacher_user = User.objects.create_user('t', password='pass', role='teacher')
        self.teacher = Teacher.objects.create(user=self.teacher_user, school=self.school)
        self.teacher.subjects.add(self.subject)
        self.student_user = User.objects.create_user('s', password='pass', role='student')
        self.student = Student.objects.create(user=self.student_user, school=self.school, class_year=None)
        self.parent_user = User.objects.create_user('p', password='pass', role='parent')
        self.parent = Parent.objects.create(user=self.parent_user)
        self.parent.children.add(self.student)
        self.director_user = User.objects.create_user('d', password='pass', role='director')
        self.director = Director.objects.create(user=self.director_user, school=self.school)
        self.admin_user = User.objects.create_user('a', password='pass', role='admin')

    def test_statistics_forbidden(self):
        # only director/admin allowed
        for user, should_pass in [(self.teacher_user, False), (self.student_user, False), (self.parent_user, False), (self.director_user, True), (self.admin_user, True)]:
            self.client.login(username=user.username, password='pass')
            resp = self.client.get(reverse('statistics'))
            self.assertEqual(resp.status_code, 200 if should_pass else 403)

    def test_term_detail_forbidden(self):
        # only director/admin allowed to view term detail
        url = reverse('term_detail', kwargs={'pk': self.term.pk})
        for user, should_pass in [(self.teacher_user, False), (self.student_user, False), (self.parent_user, False), (self.director_user, True), (self.admin_user, True)]:
            self.client.login(username=user.username, password='pass')
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200 if should_pass else 403)

    def test_assignment_create_forbidden(self):
        # only director/admin allowed to create assignment
        url = reverse('assignment_add')
        for user, should_pass in [(self.teacher_user, False), (self.student_user, False), (self.parent_user, False), (self.director_user, True), (self.admin_user, True)]:
            self.client.login(username=user.username, password='pass')
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200 if should_pass else 403)
