{
    "name": "HR Attendance Compliance",
    "version": "18.0.1.0.0",
    "summary": "Erweiterung für Pausen- und Arbeitszeitregeln",
    "category": "Human Resources",
    "author": "Eure Firma",
    "license": "LGPL-3",
    "depends": ["hr_attendance", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_attendance_views.xml",
        "views/attendance_rule_views.xml",
    ],
    "installable": True,
    "application": False,
}
