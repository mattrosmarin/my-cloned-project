import streamlit as st

from database import get_student_enrollments
from services import (
    enroll_with_key,
    get_student_summary,
    soft_unenroll_student,
)


CURRENT_STUDENT = {
    "user_id": "u100",
    "name": "Maya Patel",
    "email": "maya.patel@example.edu",
}


if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "selected_class" not in st.session_state:
    st.session_state.selected_class = None

if "message" not in st.session_state:
    st.session_state.message = ""


def show_dashboard():
    st.title("Student Enrollment Dashboard")

    user_id = CURRENT_STUDENT["user_id"]
    email = CURRENT_STUDENT["email"]

    st.caption(f"Logged in as: {CURRENT_STUDENT['name']}")

    if st.session_state.message:
        st.success(st.session_state.message)

    st.divider()

    st.subheader("Enroll In A Class")

    enrollment_key = st.text_input("Enter Enrollment Key")

    if st.button("Enroll"):
        result = enroll_with_key(
            user_id,
            email,
            enrollment_key,
        )

        if result:
            st.session_state.message = "Successfully enrolled in class."
            st.rerun()
        else:
            st.error("Invalid enrollment key.")

    st.divider()

    st.subheader("Current Enrollments")

    enrollments = get_student_enrollments(user_id)

    if not enrollments:
        st.warning("No enrolled classes found.")
        return

    for enrollment in enrollments:
        with st.container():
            st.write(f"Course: {enrollment['course_name']}")
            st.write(f"Instructor: {enrollment['instructor']}")
            st.write(f"Course ID: {enrollment['course_id']}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    f"Go To Class {enrollment['course_id']}"
                ):
                    st.session_state.selected_class = enrollment
                    st.session_state.page = "class_page"
                    st.rerun()

            with col2:
                if st.button(
                    f"Unenroll {enrollment['course_id']}"
                ):
                    soft_unenroll_student(
                        user_id,
                        enrollment["course_id"],
                    )

                    st.session_state.message = (
                        "Successfully unenrolled."
                    )

                    st.rerun()

            st.divider()

    st.subheader("Student Summary")

    summary = get_student_summary(user_id)

    st.write(summary)


def show_class_page():
    enrollment = st.session_state.selected_class

    st.title("Class Page")

    st.write(f"Course: {enrollment['course_name']}")
    st.write(f"Instructor: {enrollment['instructor']}")
    st.write(f"Course ID: {enrollment['course_id']}")
    st.write(f"Status: {enrollment['status']}")

    if st.button("Back To Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


if st.session_state.page == "dashboard":
    show_dashboard()
else:
    show_class_page()