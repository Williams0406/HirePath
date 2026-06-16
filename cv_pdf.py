"""
cv_pdf.py  —  Generador de CV en PDF
======================================
Uso:
    python cv_pdf.py datos.json                  → genera CV_<nombre>.pdf
    python cv_pdf.py datos.json -o mi_cv.pdf     → nombre personalizado
    python cv_pdf.py --demo                      → genera CV de ejemplo

Estructura del JSON de entrada: ver cv_schema.json
"""

import json
import sys
import os
import argparse
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    KeepTogether, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Paleta de colores ──────────────────────────────────────────────────────────
BLUE       = HexColor("#1F5C99")
BLUE_LIGHT = HexColor("#E8F0F8")
DARK       = HexColor("#1A1A1A")
GRAY       = HexColor("#555555")
LIGHTGRAY  = HexColor("#888888")
RULE_GRAY  = HexColor("#DDDDDD")
WHITE      = white

# ── Márgenes página A4 ────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_TOP    = 18 * mm
MARGIN_BOTTOM = 16 * mm
MARGIN_LEFT   = 18 * mm
MARGIN_RIGHT  = 18 * mm
CONTENT_W     = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT


# ─────────────────────────────────────────────────────────────────────────────
# Flowable personalizado: línea horizontal con color
# ─────────────────────────────────────────────────────────────────────────────
class ColorRule(Flowable):
    def __init__(self, width, color=RULE_GRAY, thickness=0.5, space_before=2, space_after=4):
        super().__init__()
        self.rule_width   = width
        self.color        = color
        self.thickness    = thickness
        self.space_before = space_before
        self.space_after  = space_after
        self.height       = space_before + thickness + space_after

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space_after, self.rule_width, self.space_after)


# ─────────────────────────────────────────────────────────────────────────────
# Flowable: barra de acento izquierda (para el perfil profesional)
# ─────────────────────────────────────────────────────────────────────────────
class AccentBox(Flowable):
    def __init__(self, text, width, style):
        super().__init__()
        self.text   = text
        self.width  = width
        self.style  = style
        self._para  = Paragraph(text, style)
        self._para.wrap(width - 14, 9999)
        self.height = self._para.height + 14

    def wrap(self, available_width, available_height):
        self._para.wrap(available_width - 14, available_height)
        self.height = self._para.height + 14
        return available_width, self.height

    def draw(self):
        c = self.canv
        h = self.height
        # fondo tenue
        c.setFillColor(BLUE_LIGHT)
        c.setStrokeColor(BLUE_LIGHT)
        c.roundRect(0, 0, self.width, h, 3, fill=1, stroke=0)
        # barra izquierda azul
        c.setFillColor(BLUE)
        c.rect(0, 0, 4, h, fill=1, stroke=0)
        # texto
        self._para.drawOn(c, 12, 7)


# ─────────────────────────────────────────────────────────────────────────────
# Estilos de texto
# ─────────────────────────────────────────────────────────────────────────────
def build_styles():
    s = {}

    base = dict(fontName="Helvetica", fontSize=9, leading=13,
                textColor=DARK, alignment=TA_LEFT)

    s["name"] = ParagraphStyle("name", fontName="Helvetica-Bold",
                               fontSize=18, leading=22, textColor=BLUE,
                               alignment=TA_CENTER, spaceAfter=2)

    s["tagline"] = ParagraphStyle("tagline", fontName="Helvetica",
                                  fontSize=9, leading=12, textColor=GRAY,
                                  alignment=TA_CENTER, spaceAfter=2)

    s["contact"] = ParagraphStyle("contact", fontName="Helvetica",
                                  fontSize=8.5, leading=12, textColor=GRAY,
                                  alignment=TA_CENTER, spaceAfter=6)

    s["section"] = ParagraphStyle("section", fontName="Helvetica-Bold",
                                  fontSize=10, leading=14, textColor=BLUE,
                                  spaceBefore=10, spaceAfter=2)

    s["job_title"] = ParagraphStyle("job_title", fontName="Helvetica-Bold",
                                    fontSize=9.5, leading=13, textColor=DARK,
                                    spaceBefore=7, spaceAfter=1)

    s["job_meta"] = ParagraphStyle("job_meta", fontName="Helvetica-Oblique",
                                   fontSize=8.5, leading=12, textColor=LIGHTGRAY,
                                   spaceAfter=3)

    s["bullet"] = ParagraphStyle("bullet", fontName="Helvetica",
                                 fontSize=9, leading=13, textColor=DARK,
                                 leftIndent=12, firstLineIndent=-8,
                                 spaceAfter=2, alignment=TA_JUSTIFY)

    s["profile"] = ParagraphStyle("profile", fontName="Helvetica",
                                  fontSize=9, leading=14, textColor=DARK,
                                  alignment=TA_JUSTIFY)

    s["skills_label"] = ParagraphStyle("skills_label", fontName="Helvetica-Bold",
                                       fontSize=9, leading=13, textColor=DARK)

    s["skills_value"] = ParagraphStyle("skills_value", fontName="Helvetica",
                                       fontSize=9, leading=13, textColor=DARK)

    s["cert_item"] = ParagraphStyle("cert_item", fontName="Helvetica",
                                    fontSize=8.5, leading=13, textColor=DARK,
                                    spaceAfter=1)

    s["edu_title"] = ParagraphStyle("edu_title", fontName="Helvetica-Bold",
                                    fontSize=9, leading=13, textColor=DARK,
                                    spaceBefore=4, spaceAfter=1)

    s["edu_meta"] = ParagraphStyle("edu_meta", fontName="Helvetica-Oblique",
                                   fontSize=8.5, leading=12, textColor=LIGHTGRAY,
                                   spaceAfter=2)

    s["footer"] = ParagraphStyle("footer", fontName="Helvetica",
                                 fontSize=7.5, leading=10, textColor=LIGHTGRAY,
                                 alignment=TA_CENTER)

    return s


# ─────────────────────────────────────────────────────────────────────────────
# Helpers para construir flowables
# ─────────────────────────────────────────────────────────────────────────────
def section_heading(title, styles, w=CONTENT_W):
    """Encabezado de sección con línea inferior azul."""
    elems = []
    elems.append(Paragraph(title.upper(), styles["section"]))
    elems.append(ColorRule(w, color=BLUE, thickness=1.5, space_before=0, space_after=4))
    return elems


def bullet_item(text, styles):
    return Paragraph(f"• {text}", styles["bullet"])


def skills_row(label, value, styles):
    """Una fila de habilidades: Label en negrita + valor."""
    combined = f'<b>{label}:</b>  {value}'
    return Paragraph(combined, styles["skills_value"])


# ─────────────────────────────────────────────────────────────────────────────
# Constructor principal del PDF
# ─────────────────────────────────────────────────────────────────────────────
def build_cv(data: dict, output_path: str):
    styles = build_styles()
    story  = []

    # ── CABECERA ──────────────────────────────────────────────────────────────
    p = data.get("personal", {})
    story.append(Paragraph(p.get("name", "Nombre Apellido").upper(), styles["name"]))
    story.append(Paragraph(p.get("tagline", ""), styles["tagline"]))

    contact_parts = []
    if p.get("location"):  contact_parts.append(p["location"])
    if p.get("phone"):     contact_parts.append(p["phone"])
    if p.get("email"):     contact_parts.append(p["email"])
    if p.get("linkedin"):  contact_parts.append(p["linkedin"])
    story.append(Paragraph("  |  ".join(contact_parts), styles["contact"]))
    story.append(ColorRule(CONTENT_W, color=BLUE, thickness=2, space_before=2, space_after=6))

    # ── PERFIL PROFESIONAL ────────────────────────────────────────────────────
    if data.get("profile"):
        story += section_heading("Perfil Profesional", styles)
        story.append(AccentBox(data["profile"], CONTENT_W, styles["profile"]))
        story.append(Spacer(1, 4))

    # ── HABILIDADES TÉCNICAS ──────────────────────────────────────────────────
    if data.get("skills"):
        story += section_heading("Habilidades Técnicas", styles)
        for skill_group in data["skills"]:
            story.append(skills_row(skill_group["label"], skill_group["value"], styles))
        story.append(Spacer(1, 2))

    # ── EXPERIENCIA LABORAL ───────────────────────────────────────────────────
    if data.get("experience"):
        story += section_heading("Experiencia Laboral", styles)
        for job in data["experience"]:
            block = []
            # Título + empresa + fecha
            title_line = f'<b>{job.get("title", "")}</b>'
            block.append(Paragraph(title_line, styles["job_title"]))
            meta_parts = []
            if job.get("company"):  meta_parts.append(job["company"])
            if job.get("period"):   meta_parts.append(job["period"])
            if meta_parts:
                block.append(Paragraph("  —  ".join(meta_parts), styles["job_meta"]))
            # Bullets
            for b in job.get("bullets", []):
                block.append(bullet_item(b, styles))
            block.append(Spacer(1, 2))
            story.append(KeepTogether(block))

    # ── FORMACIÓN ACADÉMICA ───────────────────────────────────────────────────
    if data.get("education"):
        story += section_heading("Formación Académica", styles)
        for edu in data["education"]:
            block = []
            block.append(Paragraph(edu.get("degree", ""), styles["edu_title"]))
            meta_parts = []
            if edu.get("institution"): meta_parts.append(edu["institution"])
            if edu.get("period"):      meta_parts.append(edu["period"])
            block.append(Paragraph("  —  ".join(meta_parts), styles["edu_meta"]))
            story.append(KeepTogether(block))

    # ── CERTIFICACIONES ───────────────────────────────────────────────────────
    if data.get("certifications"):
        story += section_heading("Certificaciones", styles)
        for cert in data["certifications"]:
            line = f'<b>{cert.get("name", "")}</b>'
            if cert.get("issuer"): line += f'  —  {cert["issuer"]}'
            if cert.get("date"):   line += f'  ({cert["date"]})'
            story.append(Paragraph(line, styles["cert_item"]))

    # ── IDIOMAS ───────────────────────────────────────────────────────────────
    if data.get("languages"):
        story += section_heading("Idiomas", styles)
        langs = "   •   ".join(
            f'{l["language"]} — {l["level"]}' for l in data["languages"]
        )
        story.append(Paragraph(langs, styles["cert_item"]))

    # ── PDF ───────────────────────────────────────────────────────────────────
    name_slug = p.get("name", "CV").replace(" ", "_")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title=f"CV — {p.get('name', '')}",
        author=p.get("name", ""),
    )

    def on_page(canvas, doc):
        canvas.saveState()
        # franja azul superior
        canvas.setFillColor(BLUE)
        canvas.rect(0, PAGE_H - 6 * mm, PAGE_W, 6 * mm, fill=1, stroke=0)
        # número de página
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(LIGHTGRAY)
        canvas.drawCentredString(PAGE_W / 2, 8 * mm,
                                 f"Página {doc.page}  —  Generado el {datetime.now().strftime('%d/%m/%Y')}")
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# Datos de demo (Williams Rodriguez)
# ─────────────────────────────────────────────────────────────────────────────
DEMO_DATA = {
    "personal": {
        "name": "Williams Uriel Junior Rodriguez Caceres",
        "tagline": "Ingeniería Industrial  |  Automatización de Procesos  |  Análisis de Datos  |  Lean Six Sigma",
        "location": "Lima, Perú",
        "phone": "962 162 027",
        "email": "Williams.rc04@gmail.com",
        "linkedin": "linkedin.com/in/williams-rodriguez-438ba8238"
    },
    "profile": (
        "Egresado de Ingeniería Industrial (Universidad de Lima) con más de 2 años de experiencia "
        "en optimización y automatización de procesos en entornos industriales, energéticos y comerciales. "
        "Especializado en el análisis y rediseño de flujos operativos, implementación de metodologías "
        "Lean Six Sigma (certificado) y desarrollo de herramientas de automatización con Python para la "
        "eliminación de actividades sin valor agregado. Con experiencia aplicando TPM en la gestión de "
        "mantenimiento y elaborando modelos predictivos para anticipar fallas y optimizar recursos. "
        "Orientado a la mejora continua con base técnica sólida para traducir ineficiencias en soluciones "
        "medibles y sostenibles."
    ),
    "skills": [
        {"label": "Lenguajes & Frameworks",
         "value": "Python (Django) · JavaScript (Next.js)"},
        {"label": "Datos & BI",
         "value": "Power BI · Excel Avanzado · pandas · NumPy · matplotlib · scikit-learn · SQL"},
        {"label": "Metodologías",
         "value": "Lean Six Sigma · Lean Manufacturing · TPM · Kanban · Teoría de Restricciones"},
        {"label": "Otros",
         "value": "Git · Modelado de BD · Gestión de Proyectos Ágiles"}
    ],
    "experience": [
        {
            "title": "Asistente Comercial",
            "company": "Harbor Supplies S.A.C.",
            "period": "Dic 2025 – Actualidad",
            "bullets": [
                "Gestioné el ciclo completo de facturación y control de inventarios para clientes del sector marítimo, reduciendo errores de emisión en ~30% mediante checklists y validaciones cruzadas.",
                "Elaboré cotizaciones técnicas para clientes del sector marítimo analizando planos técnicos y base de datos Mitsubishi, garantizando precisión en selección de repuestos y suministros.",
                "Optimicé control de stock e inventario de almacén con registro sistemático, reduciendo quiebres de inventario y mejorando la trazabilidad de productos en tiempo real.",
                "Generé informes de rendición de cuentas y seguimiento operativo, asegurando visibilidad del flujo comercial y facilitando la toma de decisiones gerenciales."
            ]
        },
        {
            "title": "Analista e Implementador de Gestión Operacional (Part-time)",
            "company": "Peruvian Group Fredal S.A.C.",
            "period": "Ene 2026 – Actualidad",
            "bullets": [
                "Realicé el levantamiento y mapeo de procesos de mantenimiento, almacén y compras para la línea de alquiler de maquinaria pesada, diseñando flujos de trabajo óptimos que establecieron la base operativa para la gestión ordenada y trazable de las operaciones.",
                "Diseñé e implementé sistema web integral (Python/Django + Next.js) para centralizar el control de mantenimientos preventivos/correctivos, preparación de repuestos, control de inventarios y reabastecimiento, eliminando el registro manual y habilitando trazabilidad en tiempo real.",
                "Diseñé el flujo de coordinación de mantenimientos y asignación de repuestos, habilitando reportaje de trabajos y generación de métricas operativas (KPIs de flota) para la toma de decisiones en la gestión de maquinaria pesada.",
                "Actualicé la plataforma de gestión de la línea de cochera, adaptando módulos de control operativo y garantizando escalabilidad del sistema ante los requerimientos cambiantes del negocio."
            ]
        },
        {
            "title": "Practicante – Excelencia Operacional",
            "company": "Corporación Qroma S.A.",
            "period": "Mar – Ago 2025",
            "bullets": [
                "Automaticé plantillas de seguimiento de desempeño para la gestión de la matriz de competencias, reduciendo el tiempo de actualización manual en ~40%.",
                "Desarrollé dashboards e indicadores en Excel/Power BI para seguimiento de KPIs operacionales, mejorando la visibilidad de resultados para la toma de decisiones de jefatura.",
                "Apoyé diseño y ejecución de procesos de onboarding y capacitación, contribuyendo a la estandarización de rutinas bajo metodología Lean Manufacturing."
            ]
        },
        {
            "title": "Analista de Monitoreo",
            "company": "Vighia Perú / Control de Combustible Perú",
            "period": "Ago 2023 – Ago 2024",
            "bullets": [
                "Supervisé sensores de combustible en tiempo real para cartera de clientes, detectando anomalías que previnieron pérdidas críticas de combustible mediante análisis de patrones.",
                "Elaboré reportes de consumo, viajes y detección de irregularidades, mejorando la velocidad de respuesta ante alertas y reduciendo tiempos de gestión de incidencias.",
                "Gestioné ciclo de facturación y seguimiento de pagos, manteniendo control de morosidad y asegurando continuidad en la relación comercial con clientes asignados."
            ]
        },
        {
            "title": "Practicante Preprofesional",
            "company": "Vighia Perú / Control de Combustible Perú",
            "period": "Mar – Ago 2023",
            "bullets": [
                "Implementé tablero Kanban para gestión de actividades operativas del equipo, mejorando visibilidad de tareas y reduciendo tiempos de seguimiento de equipos instalados.",
                "Gestioné ciclo de facturación y emisión de notas de crédito, garantizando precisión documental y reduciendo inconsistencias en la documentación contable.",
                "Elaboré informes operativos y constancias de instalación, asegurando documentación completa y oportuna del proceso de implementación de sensores en campo."
            ]
        }
    ],
    "education": [
        {
            "degree": "Ingeniería Industrial (Egresado)",
            "institution": "Universidad de Lima",
            "period": "2018 – 2025"
        },
        {
            "degree": "Especialización en Industria Sostenible",
            "institution": "Universidad de Lima",
            "period": "2022 – 2025"
        }
    ],
    "certifications": [
        {"name": "Six Sigma Principles & Tools (Define, Measure & Analyze)",
         "issuer": "Kennesaw State University", "date": "Oct 2025"},
        {"name": "Data Analytics for Lean Six Sigma",
         "issuer": "University of Amsterdam", "date": "Oct 2025"},
        {"name": "Python & Statistics for Financial Analysis",
         "issuer": "HKUST", "date": "Nov 2025"},
        {"name": "Power BI & Gestión Ágil y Lean",
         "issuer": "Fundación Telefónica Movistar", "date": "Mar 2024"}
    ],
    "languages": [
        {"language": "Español", "level": "Nativo"},
        {"language": "Inglés", "level": "Intermedio (B1)"}
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generador de CV en PDF")
    parser.add_argument("input", nargs="?", help="Ruta al JSON de datos del CV")
    parser.add_argument("-o", "--output", help="Ruta del PDF de salida (opcional)")
    parser.add_argument("--demo", action="store_true", help="Genera CV de demostración")
    args = parser.parse_args()

    if args.demo or args.input is None:
        data = DEMO_DATA
        out  = args.output or "CV_Demo_Williams_Rodriguez.pdf"
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("personal", {}).get("name", "CV").replace(" ", "_")
        out  = args.output or f"CV_{name}.pdf"

    path = build_cv(data, out)
    print(f"✅  CV generado: {path}")


if __name__ == "__main__":
    main()
