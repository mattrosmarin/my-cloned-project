from __future__ import annotations

import json
from pathlib import Path

from database import (
    create_tables,
    get_all_enrollment_records,
    get_available_course_keys,
    get_student_enrollments,
    seed_sample_data,
)
from services import enroll_with_key, get_student_summary


SNAPSHOT_PATH = Path(__file__).with_name("student_enrollment_snapshot.json")

CURRENT_STUDENT = {
    "user_id": "u100",
    "name": "Maya Patel",
    "email": "maya.patel@example.edu",
}

STATUS_ENROLLED = "enrolled"
STATUS_UNENROLLED = "unenrolled"

AVAILABLE_COURSE_KEYS = [
    {
        "course_id": "MISY350",
        "course_name": "Python for Business Analytics",
        "instructor": "Dr. Rivera",
        "enrollment_key": "MISY350-SPRING",
    },
    {
        "course_id": "DATA210",
        "course_name": "Data Storytelling",
        "instructor": "Prof. Morgan",
        "enrollment_key": "DATA210-SPRING",
    },
    {
        "course_id": "WEB220",
        "course_name": "Web Apps With Streamlit",
        "instructor": "Dr. Chen",
        "enrollment_key": "WEB220-SPRING",
    },
]

SAMPLE_ENROLLMENTS = [
    ("u100", "maya.patel@example.edu", "MISY350", STATUS_ENROLLED),
    ("u100", "maya.patel@example.edu", "DATA210", STATUS_UNENROLLED),
    ("u101", "alex@example.edu", "MISY350", STATUS_ENROLLED),
    ("u102", "blair@example.edu", "WEB220", STATUS_ENROLLED),
]


def export_database_snapshot(path: Path = SNAPSHOT_PATH) -> None:
    snapshot = {
        "current_student": CURRENT_STUDENT,
        "available_course_keys": get_available_course_keys(),
        "enrollment_table": get_all_enrollment_records(),
    }

    path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")


def main() -> None:
    create_tables()
    seed_sample_data(AVAILABLE_COURSE_KEYS, SAMPLE_ENROLLMENTS)

    user_id = CURRENT_STUDENT["user_id"]
    email = CURRENT_STUDENT["email"]

    print("Current student:")
    print(CURRENT_STUDENT)

    print("\nAvailable enrollment keys:")
    print(get_available_course_keys())

    print("\nInitial enrolled classes:")
    print(get_student_enrollments(user_id))

    print("\nStudent enters key DATA210-SPRING:")
    print(enroll_with_key(user_id, email, "DATA210-SPRING"))

    print("\nUpdated enrolled classes:")
    print(get_student_enrollments(user_id))

    print("\nStudent summary:")
    print(get_student_summary(user_id))

    export_database_snapshot()
    print(f"\nDatabase snapshot written to: {SNAPSHOT_PATH}")


if __name__ == "__main__":
    main()