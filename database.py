from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Optional


DB_PATH = Path(__file__).with_name("student_enrollment_practice.db")

STATUS_ENROLLED = "enrolled"
STATUS_UNENROLLED = "unenrolled"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def create_tables() -> None:
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                instructor TEXT NOT NULL,
                enrollment_key TEXT NOT NULL UNIQUE
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                email TEXT NOT NULL,
                course_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'enrolled',
                enrolled_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, course_id)
            )
            """
        )


def seed_sample_data(course_keys, sample_enrollments) -> None:
    with connect() as connection:
        connection.executemany(
            """
            INSERT OR IGNORE INTO courses (
                course_id, course_name, instructor, enrollment_key
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    course["course_id"],
                    course["course_name"],
                    course["instructor"],
                    course["enrollment_key"],
                )
                for course in course_keys
            ],
        )

        connection.executemany(
            """
            INSERT OR IGNORE INTO enrollments
            (user_id, email, course_id, status)
            VALUES (?, ?, ?, ?)
            """,
            sample_enrollments,
        )


def get_available_course_keys():
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT course_id, course_name, instructor, enrollment_key
            FROM courses
            ORDER BY course_id
            """
        ).fetchall()

    return rows_to_dicts(rows)


def get_course_by_key(enrollment_key: str):
    with connect() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM courses
            WHERE enrollment_key = ?
            """,
            (enrollment_key.strip().upper(),),
        ).fetchone()

    return dict(row) if row else None


def get_student_enrollments(user_id: str):
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT
                e.enrollment_id,
                e.user_id,
                e.email,
                e.course_id,
                c.course_name,
                c.instructor,
                e.status,
                e.enrolled_at
            FROM enrollments e
            JOIN courses c ON c.course_id = e.course_id
            WHERE e.user_id = ? AND e.status = ?
            """,
            (user_id, STATUS_ENROLLED),
        ).fetchall()

    return rows_to_dicts(rows)


def get_student_enrollment_history(user_id: str):
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT
                e.enrollment_id,
                e.user_id,
                e.email,
                e.course_id,
                c.course_name,
                c.instructor,
                e.status,
                e.enrolled_at
            FROM enrollments e
            JOIN courses c ON c.course_id = e.course_id
            WHERE e.user_id = ?
            """,
            (user_id,),
        ).fetchall()

    return rows_to_dicts(rows)


def get_student_course_record(user_id: str, course_id: str):
    with connect() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM enrollments
            WHERE user_id = ? AND course_id = ?
            """,
            (user_id, course_id),
        ).fetchone()

    return dict(row) if row else None


def save_enrollment(user_id, email, course_id):
    with connect() as connection:
        connection.execute(
            """
            INSERT INTO enrollments
            (user_id, email, course_id, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, course_id)
            DO UPDATE SET
                email = excluded.email,
                status = excluded.status,
                enrolled_at = CURRENT_TIMESTAMP
            """,
            (user_id, email, course_id, STATUS_ENROLLED),
        )


def update_unenrollment(user_id: str, course_id: str):
    with connect() as connection:
        cursor = connection.execute(
            """
            UPDATE enrollments
            SET status = ?
            WHERE user_id = ? AND course_id = ?
            """,
            (STATUS_UNENROLLED, user_id, course_id),
        )

    return cursor.rowcount > 0


def get_all_enrollment_records():
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT
                e.enrollment_id,
                e.user_id,
                e.email,
                e.course_id,
                c.course_name,
                c.instructor,
                e.status,
                e.enrolled_at
            FROM enrollments e
            JOIN courses c ON c.course_id = e.course_id
            """
        ).fetchall()

    return rows_to_dicts(rows)