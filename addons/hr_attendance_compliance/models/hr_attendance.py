from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    worked_hours_raw = fields.Float(
        string="Rohstunden",
        compute="_compute_compliance_data",
    )
    worked_hours_odoo = fields.Float(
        string="Odoo-Arbeitsstunden",
        compute="_compute_compliance_data",
    )
    break_required = fields.Float(
        string="Pflichtpause (Std.)",
        compute="_compute_compliance_data",
    )
    worked_hours_net = fields.Float(
        string="Nettostunden",
        compute="_compute_compliance_data",
    )
    violation = fields.Boolean(
        string="Verstoß",
        compute="_compute_compliance_data",
    )
    violation_reason = fields.Char(
        string="Verstoßgrund",
        compute="_compute_compliance_data",
    )
    rule_id = fields.Many2one(
        "hr.attendance.rule",
        string="Angewendete Regel",
        compute="_compute_compliance_data",
    )
    break_required_legal = fields.Float(
        string="Gesetzliche Pflichtpause (Std.)",
        compute="_compute_compliance_data",
    )
    break_required_company = fields.Float(
        string="Firmenpflichtpause (Std.)",
        compute="_compute_compliance_data",
    )
    worked_hours_net_legal = fields.Float(
        string="Nettostunden gesetzlich",
        compute="_compute_compliance_data",
    )
    worked_hours_net_company = fields.Float(
        string="Nettostunden Firma",
        compute="_compute_compliance_data",
    )

    @api.depends("check_in", "check_out", "worked_hours")
    def _compute_compliance_data(self):
        Rule = self.env["hr.attendance.rule"]
        active_rule = Rule.search([("active", "=", True)], limit=1)

        for rec in self:
            raw = 0.0
            if rec.check_in and rec.check_out:
                duration = rec.check_out - rec.check_in
                raw = duration.total_seconds() / 3600.0

            odoo_hours = rec.worked_hours or 0.0

            break_required = 0.0
            break_required_legal = 0.0
            break_required_company = 0.0
            worked_hours_net_legal = 0.0
            worked_hours_net_company = 0.0
            violation = False
            violation_reason = ""

            if active_rule:
                # Schwellen aus Regel lesen
                break_6h_threshold = active_rule.break_6h_threshold or 6.0
                break_6h_minutes = active_rule.break_6h_minutes or 30

                break_9h_threshold = active_rule.break_9h_threshold or 9.0
                break_9h_minutes = active_rule.break_9h_minutes or 45
                break_9h_grace_minutes = active_rule.break_9h_grace_minutes or 15

                max_daily_hours = active_rule.max_daily_hours or 10.0

                # Minuten in Stunden umrechnen
                break_6h_hours = break_6h_minutes / 60.0
                break_9h_hours = break_9h_minutes / 60.0
                grace_hours = break_9h_grace_minutes / 60.0

                # Firmenlogik mit Kulanz (9h zuerst!)
                if raw > (break_9h_threshold + grace_hours):
                    break_required_company = break_9h_hours
                    company_raw = raw

                elif raw > break_9h_threshold:
                    break_required_company = break_6h_hours
                    company_raw = break_9h_threshold

                # 6h-Logik
                elif raw > (
                    break_6h_threshold + (active_rule.break_6h_grace_minutes / 60.0)
                ):
                    break_required_company = break_6h_hours
                    company_raw = raw

                elif raw > break_6h_threshold:
                    break_required_company = 0.0
                    company_raw = break_6h_threshold

                else:
                    break_required_company = 0.0
                    company_raw = raw

                # Nettostunden berechnen
                worked_hours_net_legal = max(raw - break_required_legal, 0.0)
                worked_hours_net_company = max(
                    company_raw - break_required_company, 0.0
                )

                # Altes Feld vorerst auf Firmenlogik abbilden
                break_required = break_required_company
                net = worked_hours_net_company

                # Maximalarbeitszeit prüfen
                if raw > max_daily_hours:
                    violation = True
                    violation_reason = "Maximale Tagesarbeitszeit überschritten"

            else:
                net = 0.0
                violation = True
                violation_reason = "Keine aktive Arbeitszeitregel gefunden"

            # Fehlender Checkout prüfen
            if rec.check_in and not rec.check_out:
                violation = True
                violation_reason = "Kein Check-out vorhanden"

            rec.worked_hours_raw = raw
            rec.worked_hours_odoo = odoo_hours
            rec.break_required = break_required
            rec.break_required_legal = break_required_legal
            rec.break_required_company = break_required_company
            rec.worked_hours_net = net
            rec.worked_hours_net_legal = worked_hours_net_legal
            rec.worked_hours_net_company = worked_hours_net_company
            rec.violation = violation
            rec.violation_reason = violation_reason
            rec.rule_id = active_rule.id if active_rule else False
