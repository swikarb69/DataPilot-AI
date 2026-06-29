from pathlib import Path
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


class PDFService:

    def __init__(self):
        self.template_dir = Path("app/templates")
        self.output_dir = Path("reports")

        self.output_dir.mkdir(exist_ok=True)

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir)
        )

    def generate_report(
    self,
    dataset_summary,
    cleaning_summary,
    insights,
    chart_paths,
    statistics,
):

        template = self.env.get_template("report.html")

        html = template.render(
    generated_at=datetime.now(),
    dataset=dataset_summary,
    cleaning=cleaning_summary,
    insights=insights,
    charts=chart_paths,
    statistics=statistics,
)

        output_file = (
            self.output_dir
            / f"report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        )

        HTML(string=html).write_pdf(output_file)

        return output_file