# E-Grader

**Web-Based Electronic Gradebook**

A Django application for managing student grades and attendance, built with Bootstrap for responsive design and role-based access control. Supports administrators, directors, teachers, parents, and students.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Role Permissions](#role-permissions)
4. [Architecture & Models](#architecture--models)
5. [Views & URLs](#views--urls)
6. [Templates & Styling](#templates--styling)
7. [Setup & Installation](#setup--installation)
8. [Running the Application](#running-the-application)
9. [Testing & Coverage](#testing--coverage)
10. [Directory Structure](#directory-structure)
11. [Screenshots](#screenshots)
12. [Future Improvements](#future-improvements)
13. [Contributing](#contributing)
14. [License](#license)

---

## Overview
The **E-Grader** system allows schools to manage:
- **Schools**, **ClassYears**, and **ProgramTerms**
- **Directors**, **Teachers**, **Students**, and **Parents**
- **Grades** and **Attendance** records per student
- Per-term **TeachingAssignments** (which teacher teaches which subject in which term)

Built with Django 5 and Bootstrap 4, it provides separate dashboards and CRUD operations tailored to each user role.

## Features
- **User Registration & Login** with built-in Django auth
- **Role Selection** at signup (admin, director, teacher, parent, student)
- **Responsive** UIs using a Bootswatch theme (Cerulean)
- **CRUD** operations for all entities:
  - Schools (name, address)
  - ClassYears (grade level, section)
  - ProgramTerms (start/end dates, subjects)
  - Directors, Teachers, Students, Parents (one-to-one profiles)
  - Grades & Attendance per student
  - TeachingAssignments (teacher & subject per term)
- **Role-based Access Control**:
  - **Administrators**: Manage all data; view cross-school statistics
  - **Directors**: Manage associated school; view full statistics & term assignments
  - **Teachers**: Enter/view grades & attendance only for their assigned students
  - **Parents**: View only their children’s grades & attendance
  - **Students**: View only their own grades & attendance
- **Statistics Dashboard**:
  - Counts of schools, teachers, students, parents, subjects, grades, attendance
  - Average grade per subject
  - Assignment counts
- **Unit Tests** covering positive and negative (permission) cases; >80% coverage

## Role Permissions
| Role          | View Dashboard | CRUD Operations              | Statistics & Reports | Term Assignments    |
|---------------|----------------|------------------------------|----------------------|---------------------|
| Admin         | Yes            | All Entities                 | All Schools          | All Terms           |
| Director      | Yes            | School-specific Entities     | Own School only      | Own School Terms    |
| Teacher       | Yes            | Grades & Attendance (Own)    | No                   | No                  |
| Parent        | Yes            | None                         | No                   | No                  |
| Student       | Yes            | None                         | No                   | No                  |

## Architecture & Models
Key Django models (in `core/models.py`):
- `User`: extends `AbstractUser` with a `role` field
- `School`, `ClassYear`, `Subject`, `ProgramTerm`
- `Director`, `Teacher`, `Student`, `Parent` (profiles linked to `User`)
- `Grade`, `Attendance` (records per student)
- `TeachingAssignment` (M2M: Term × Teacher × Subject)

Relationships and validations are enforced at the form and view level.

## Views & URLs
- **Generic Class-Based Views** (ListView, CreateView, UpdateView, DeleteView, DetailView)
- **Custom Mixins** for `login_required` and role checks
- Overrides of `get_queryset`, `get_form_kwargs`, and `dispatch` for filtering and permissions
- URL patterns defined in `core/urls.py`, included in project `urls.py`

Example:
```python
path('terms/<int:pk>/', ProgramTermDetailView.as_view(), name='term_detail')
```

## Templates & Styling
- Base layout in `templates/base.html` with Bootswatch Cerulean theme
- List pages converted to responsive `<table>` layouts
- Form pages wrapped in Bootstrap `card` and `form-group` loops
- Delete confirmation dialogs styled as cards
- Contextual navigation links per user role

## Setup & Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/KiwiKit2/e-grader.git
   cd e-grader
   ```
2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser** (Admin)
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application
```bash
python manage.py runserver
# Access at http://127.0.0.1:8000/
```

## Testing & Coverage
```bash
python manage.py test
coverage run --source='.' manage.py test
coverage report
```
- Tests cover CRUD flows and permission checks.
- Coverage ≥ 80% is maintained.

## Directory Structure
```
core/           # Django app: models, views, forms, tests
e_grader/       # Project settings and entrypoints
templates/      # HTML templates by module
manage.py       # Django CLI
README.md       # This documentation
requirements.txt# Python dependencies
```

## Screenshots
*Add screenshots of each dashboard, list, form, and term detail page here.*

## Future Improvements
- **Charts** for grade distributions (e.g., Chart.js)
- **Export** reports (CSV/PDF)
- **Notifications** for attendance alerts
- **Internationalization** (i18n) for Bulgarian, English, etc.

## Contributing
Contributions are welcome! Please open issues or pull requests for enhancements or bug fixes.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
