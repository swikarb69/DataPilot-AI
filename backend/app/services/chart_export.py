from pathlib import Path
from typing import Dict

import plotly.graph_objects as go


class ChartExporter:
    def __init__(self):
        self.output_dir = Path("reports/charts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, figures: Dict[str, go.Figure]) -> list[str]:
        """
        Save Plotly figures as PNG files.

        Parameters
        ----------
        figures : {
            "histogram": Figure,
            "heatmap": Figure,
            ...
        }

        Returns
        -------
        List of image paths.
        """

        image_paths = []

        for name, fig in figures.items():

            file_path = self.output_dir / f"{name}.png"

            fig.write_image(
                str(file_path),
                width=1200,
                height=700,
                scale=2
            )

            image_paths.append(str(file_path))

        return image_paths