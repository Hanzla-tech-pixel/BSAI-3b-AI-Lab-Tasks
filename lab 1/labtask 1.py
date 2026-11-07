def scholarship(marks, docs, attendance, age):

    if marks < 70:
        return "Fail", "Marks below 70"

    if not docs:
        return "Fail", "Documents incomplete"

    if attendance < 75:
        return "Fail", "Attendance below 75%"

    if age < 18:
        return "Fail", "Age below 18"

    return "Review", "All conditions satisfied"


tests = [
    ("T1_pass", 82, True, 90, 20, "Review"),
    ("T2_attendance_fail", 85, True, 70, 20, "Fail"),
    ("T3_age_fail", 88, True, 90, 17, "Fail"),
    ("T4_boundary", 70, True, 75, 18, "Review")
]


print("SYNTHETIC thresholds: marks>=70, docs complete, attendance>=75, age>=18")

for name, marks, docs, attendance, age, expected in tests:

    actual, reason = scholarship(marks, docs, attendance, age)

    print("\n", name)
    print("input    :", f"marks={marks}, docs={docs}, attendance={attendance}, age={age}")
    print("expected :", expected)
    print("actual   :", actual, "(MATCH)" if actual == expected else "(MISMATCH)")
    print("reason   :", reason)