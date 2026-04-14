README.md

# Odoo Zeiterfassungsmodul mit Compliance-Logik (Community Edition)

## Übersicht

Dieses Modul erweitert die Standard-Zeiterfassung von Odoo (Community Edition), um eine flexible und konfigurierbare Arbeitszeitberechnung zu ermöglichen.

Ziel ist es, sowohl reale Anwesenheitszeiten als auch betriebliche und gesetzliche Anforderungen abzubilden.

---

## Funktionen

### Erweiterte Felder in der Zeiterfassung

Jeder Zeiterfassungseintrag (`hr.attendance`) wird um folgende Felder ergänzt:

* **worked_hours_raw**
  Tatsächliche Dauer zwischen Check-in und Check-out

* **worked_hours_odoo**
  Von Odoo berechnete Arbeitszeit (abhängig vom Arbeitszeitmodell)

* **worked_hours_net**
  Arbeitszeit nach automatischer Pausenberechnung

* **break_required**
  Erforderliche Pause gemäß Regel

* **violation / violation_reason**
  Kennzeichnung und Begründung von Verstößen (z. B. Überschreitung der maximalen Arbeitszeit)

---

## Regelbasierte Konfiguration

Es wurde ein neues Modell eingeführt:

```id="w7o2xv"
hr.attendance.rule
```

Damit können Arbeitszeitregeln flexibel konfiguriert werden:

* Schwellenwerte für Pausen (z. B. ab 6 Stunden, ab 9 Stunden)
* Dauer der Pausen
* Kulanzzeit nach 9 Stunden
* Maximale tägliche Arbeitszeit

Dadurch kann das System ohne Codeänderungen an betriebliche Anforderungen angepasst werden.

---

## Zentrale Idee

Das Modul trennt bewusst drei unterschiedliche Zeitwerte:

| Typ       | Beschreibung                          |
| --------- | ------------------------------------- |
| Rohzeit   | Tatsächliche Anwesenheit              |
| Odoo-Zeit | Arbeitszeit laut Arbeitszeitmodell    |
| Nettozeit | Berechnete Arbeitszeit nach Regelwerk |

Diese Trennung ist notwendig, da Odoo Arbeitszeitmodelle berücksichtigt, die nicht immer der realen Anwesenheit entsprechen.

---

## Besonderheiten

* Odoo-Standardverhalten (`worked_hours`) bleibt unverändert
* Eigene Berechnungen basieren auf echten Zeitdifferenzen
* Regelmodell ermöglicht flexible Anpassung an betriebliche Prozesse
* Aktuell wird die erste aktive Regel verwendet

---

## Aktueller Entwicklungsstand

### Bereits umgesetzt

* Erweiterung des Attendance-Modells
* Berechnung von Roh-, Odoo- und Nettoarbeitszeit
* Einführung eines konfigurierbaren Regelmodells
* Umsetzung einer Pausenlogik mit Kulanzzeit
* Anzeige der berechneten Werte in der Oberfläche

### Geplante Erweiterungen

* Trennung zwischen:

  * gesetzlicher Pause (`break_required_legal`)
  * betrieblicher Pause (`break_required_company`)
* Tagesaggregation (mehrere Buchungen pro Tag zusammenführen)
* Prüfung von Kernarbeitszeiten
* Integration von Urlaub und Abwesenheiten
* Berichte und automatischer Mailversand

---

## Installation

1. Modul in den Addons-Ordner legen:

```bash
/mnt/extra-addons
```

2. Modul aktualisieren:

```bash id="u6ykn6"
docker compose exec web odoo -d <datenbank> -u hr_attendance_compliance --stop-after-init
docker compose restart web
```

---

## Ziel des Projekts

Ziel ist der Aufbau eines flexiblen Zeiterfassungssystems, das:

* reale Arbeitszeiten korrekt abbildet
* gesetzliche Anforderungen berücksichtigt
* betriebliche Besonderheiten unterstützt
* einfach konfigurierbar und erweiterbar ist

---

## Kontext

Dieses Modul entsteht im Rahmen einer Ausbildung im Bereich Anwendungsentwicklung und dient als praxisnahes Lernprojekt.
