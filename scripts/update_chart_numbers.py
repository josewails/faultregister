from core.models import Chart


def update_chart_numbers(start_number):
    chart = Chart.objects.filter(number=start_number).last()
    chart_id = chart.id

    charts = Chart.objects.exclude(id=chart_id).filter(number__gte=start_number)

    for chart in charts:
        chart.number = chart.number + 1
        chart.save()


def run():
    update_chart_numbers(4)
