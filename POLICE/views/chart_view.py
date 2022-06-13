from django.shortcuts import render
from plotly.offline.offline import plot

from ..models import *
import pandas as pd
from plotly.offline import *
import plotly.express as px


def chart_view(request):
    qs = Chart.objects.all()
    try:

        projects_data = [
            {
                'complaint': x.complaint.code,
                'Start': x.start_date,
                'Finish': x.finish_date,
                'crime': x.crime.name
            } for x in qs
        ]
        df = pd.DataFrame(projects_data)
        fig = px.timeline(
            df, x_start="Start", x_end="Finish", y="complaint", color="crime"
        )
        fig.update_yaxes(autorange="reversed")
        gantt_plot = plot(fig, output_type="div")
    except:
        gantt_plot = None
    context = {'plot_div': gantt_plot, 'chart': qs}
    return render(request, 'chart/index.html', context)
