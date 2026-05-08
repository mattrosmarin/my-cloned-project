App Goal

Build a student-facing Streamlit app that allows a simulated student to:

view enrolled classes
enter enrollment keys
enroll or re-enroll in classes
view class details
soft-unenroll from classes

The app will use the existing backend structure from Session 1.

User Assumptions
The student is already logged in.
The simulated student is Maya Patel (u100).
The app will not include login, registration, password handling, or authentication systems.
Backend Structure

The Streamlit UI should use the existing layered backend structure:

database.py
services.py
main.py

The UI should call service-layer functions whenever possible.

Session State Design

The app should use st.session_state to store:

current page
selected class
student role
success/error feedback messages
Page 1: Student Dashboard

The dashboard page should include:

enrolled classes table
enrollment key text input
enroll button
Go To Class button
Unenroll button

Suggested Streamlit elements:

st.title
st.text_input
st.button
st.dataframe
st.success
st.error
st.warning
Page 2: Selected Class Page

The selected class page should display:

course name
instructor
course ID
enrollment status
back-to-dashboard button

Suggested Streamlit elements:

st.title
st.container
st.columns
st.button
Enrollment Behavior

When the student enters a valid enrollment key:

call the service layer enrollment function
update enrollment records
show success feedback

If the key is invalid:

show an error message
Soft Unenroll Behavior

When the student clicks Unenroll:

update the enrollment record status to "unenrolled"
keep the database row
store a short success message in st.session_state
refresh the dashboard
Implementation Goal

The UI implementation should keep business logic in the service layer and database logic in the database layer while Streamlit handles presentation and routing only.