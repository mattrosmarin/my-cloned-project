Enrollment Structure Analysis
Main Structural Issues
Issue	Why It Is A Problem
Mixed responsibilities	Several functions contain both database logic and business logic, making the backend harder to maintain.
Procedural design	The project uses standalone functions instead of grouped classes or layers.
Business rules mixed with SQL	Functions like enroll_with_key() validate enrollment rules while also updating the database.
Limited scalability	As the app grows into a Streamlit dashboard, tightly coupled logic will become harder to test and expand.
Export logic mixed into backend flow	JSON snapshot exporting is mixed into the application workflow instead of separated into a dedicated layer or utility.
Database Layer Responsibilities

The following functions mainly belong in the database layer because they focus on SQL queries, inserts, updates, or returning rows:

connect
create_tables
seed_sample_data
get_available_course_keys
get_course_by_key
get_student_enrollments
get_student_enrollment_history
get_student_course_record
get_all_enrollment_records
Service Layer Responsibilities

The following functions mainly belong in the service layer because they contain business meaning or application rules:

get_student_summary
Mixed Responsibility Functions

The following functions currently mix database logic with service-level decisions:

enroll_with_key
soft_unenroll_student
export_database_snapshot
main
Recommended Refactor Direction

The backend should move toward a layered design:

Database layer handles SQLite queries and row operations.
Service layer handles enrollment validation, summaries, enrollment rules, and student actions.
Application flow should be separated from low-level database operations.
The project can later support a Streamlit UI more cleanly after separation of concerns is improved.