from __future__ import annotations

from database import (
    STATUS_ENROLLED,
    STATUS_UNENROLLED,
    get_course_by_key,
    get_student_course_record,
    get_student_enrollment_history,
    save_enrollment,
    update_unenrollment,
)


def enroll_with_key(user_id: str, email: str, enrollment_key: str):
    if not user_id:
        return None

    if not email or "@" not in email:
        return None

    if not enrollment_key:
        return None

    course = get_course_by_key(enrollment_key)

    if not course:
        return None

    save_enrollment(
        user_id=user_id,
        email=email,
        course_id=course["course_id"],
    )

    return get_student_course_record(
        user_id,
        course["course_id"],
    )


def soft_unenroll_student(user_id: str, course_id: str):
    if not user_id or not course_id:
        return False

    return update_unenrollment(user_id, course_id)


def get_student_summary(user_id: str):
    summary = {
        "total_records": 0,
        STATUS_ENROLLED: 0,
        STATUS_UNENROLLED: 0,
    }

    records = get_student_enrollment_history(user_id)

    for record in records:
        summary["total_records"] += 1

        status = record["status"]

        if status in summary:
            summary[status] += 1

    return summary