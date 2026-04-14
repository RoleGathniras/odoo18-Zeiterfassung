from odoo import fields, models


class HrAttendanceRule(models.Model):
    _name = "hr.attendance.rule"
    _description = "Attendance Compliance Rule"
    _order = "name"

    name = fields.Char(string="Regelname", required=True)
    active = fields.Boolean(string="Aktiv", default=True)

    break_6h_threshold = fields.Float(
        string="Pause ab mehr als X Stunden",
        default=6.0,
        required=True,
    )
    break_6h_minutes = fields.Integer(
        string="Pausenminuten ab 6h",
        default=30,
        required=True,
    )

    break_9h_threshold = fields.Float(
        string="Zusätzliche Pause ab mehr als X Stunden",
        default=9.0,
        required=True,
    )
    break_9h_minutes = fields.Integer(
        string="Gesamtpausenminuten ab 9h",
        default=45,
        required=True,
    )

    break_9h_grace_minutes = fields.Integer(
        string="Kulanz nach 9h (Min.)",
        default=15,
        required=True,
    )

    max_daily_hours = fields.Float(
        string="Maximale Tagesarbeitszeit",
        default=10.0,
        required=True,
    )
