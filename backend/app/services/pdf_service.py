"""
pdf_service.py
==============
Clinical PDF Report Generator using ReportLab
Generates structured academic diagnostic reports for:
1. Hybrid Tabular Risk Assessments (Diabetes / Heart Disease)
2. Diabetic Retinopathy Fundus Scans
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()

    def _init_custom_styles(self):
        self.title_style = ParagraphStyle(
            "DocTitle",
            parent=self.styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f2744"),
            spaceAfter=4
        )
        self.sub_style = ParagraphStyle(
            "DocSub",
            parent=self.styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#0d9488")
        )
        self.h2_style = ParagraphStyle(
            "Heading2Custom",
            parent=self.styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#0f2744"),
            spaceBefore=12,
            spaceAfter=6
        )
        self.body_style = ParagraphStyle(
            "BodyCustom",
            parent=self.styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155")
        )
        self.disclaimer_style = ParagraphStyle(
            "DisclaimerCustom",
            parent=self.styles["Normal"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#64748b")
        )

    def generate_assessment_pdf(self, assessment_data: dict) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        elements = []

        # Header Title
        disease = assessment_data.get("disease", "Clinical Risk Assessment")
        elements.append(Paragraph(f"MediHybrid — {disease}", self.title_style))
        elements.append(Paragraph("Intelligent Hybrid Healthcare Assessment Report | MCA Soft Computing Project", self.sub_style))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0d9488"), spaceAfter=12))

        # Metadata Table
        ts = assessment_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        rec_id = assessment_data.get("record_id", "MH-AUTO")
        meta_data = [
            [Paragraph("<b>Record ID:</b>", self.body_style), Paragraph(str(rec_id), self.body_style),
             Paragraph("<b>Assessment Date:</b>", self.body_style), Paragraph(str(ts), self.body_style)],
            [Paragraph("<b>Evaluation Engine:</b>", self.body_style), Paragraph("GA + ANN + Mamdani Fuzzy Fusion", self.body_style),
             Paragraph("<b>Diagnostic Status:</b>", self.body_style), Paragraph("Experimental Soft-Computing Prototype", self.body_style)]
        ]
        meta_table = Table(meta_data, colWidths=[100, 170, 110, 160])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4)
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 14))

        # Hybrid Score Summary Block
        hybrid = assessment_data.get("hybrid", {})
        ann = assessment_data.get("ann", {})
        fuzzy = assessment_data.get("fuzzy", {})

        score = hybrid.get("score", 0.0)
        category = hybrid.get("category", "Evaluated")
        rec = hybrid.get("recommendation", "Standard lifestyle vigilance recommended.")

        score_data = [
            [
                Paragraph("<b>Integrated Hybrid Risk Score</b>", self.h2_style),
                Paragraph("<b>Component Scores</b>", self.h2_style)
            ],
            [
                Paragraph(f"<font size=24 color='#0f2744'><b>{score}%</b></font><br/><b>Category:</b> {category}", self.body_style),
                Paragraph(f"• <b>Artificial Neural Network:</b> {ann.get('score', 'N/A')}% (Weight: 70%)<br/>"
                          f"• <b>Mamdani Fuzzy Inference:</b> {fuzzy.get('fuzzy_score', 'N/A')}% (Weight: 30%)<br/>"
                          f"• <b>Fuzzy Level:</b> {fuzzy.get('risk_level', 'N/A')}", self.body_style)
            ]
        ]
        score_table = Table(score_data, colWidths=[270, 270])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdfa")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0d9488")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8)
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 14))

        # Clinical Guidance
        elements.append(Paragraph("<b>Clinical Guidance & Interpretation:</b>", self.h2_style))
        elements.append(Paragraph(rec, self.body_style))
        elements.append(Spacer(1, 10))

        # Patient Input Parameters Table
        inputs = assessment_data.get("inputs", {})
        elements.append(Paragraph("<b>Recorded Patient Input Parameters:</b>", self.h2_style))
        input_rows = [["Clinical Parameter", "Recorded Value"]]
        for k, v in inputs.items():
            input_rows.append([str(k), str(v)])

        in_table = Table(input_rows, colWidths=[270, 270])
        in_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f2744")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3)
        ]))
        elements.append(in_table)
        elements.append(Spacer(1, 14))

        # Explainable AI Contributions
        explain = assessment_data.get("explainability", [])
        if explain:
            elements.append(Paragraph("<b>Top Explainable AI (XAI) Biomarker Impacts:</b>", self.h2_style))
            exp_rows = [["Biomarker", "Value", "Baseline Ref", "Impact Direction"]]
            for f in explain[:5]:
                direction = "Elevated Risk Factor" if f.get("is_risk_factor") else ("Protective Level" if f.get("is_protective") else "Neutral")
                exp_rows.append([
                    f.get("label", f.get("feature")),
                    f"{f.get('value')} {f.get('unit')}",
                    str(f.get("reference")),
                    direction
                ])

            exp_table = Table(exp_rows, colWidths=[150, 120, 110, 160])
            exp_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0d9488")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3)
            ]))
            elements.append(exp_table)
            elements.append(Spacer(1, 16))

        # Disclaimer
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94a3b8"), spaceAfter=8))
        elements.append(Paragraph(
            "<b>NOTICE:</b> This document is an academic diagnostic simulation produced by the MediHybrid Soft Computing System. "
            "It is not a clinical medical diagnosis. All probabilistic inferences and fuzzy risk bands require validation by licensed physicians.",
            self.disclaimer_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

pdf_generator = PDFReportGenerator()
