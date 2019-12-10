from django.db import models


class Chart(models.Model):
    chart_types = (
        ('bar_chart', 'Bar Chart'),
        ('pie_chart', 'Pie Chart'),
        ('radar_chart', 'Radar Chart'),
        ('constant_value', 'Constant Value'),
        ('donut_chart', 'Donut Chart'),
        ('polar_chart', 'Polar Chart'),
        ('multiple_statistics', 'Multiple Statistics'),
        ('product_line', 'Product Line'),
        ('multiple_bar_chart', 'Multiple Bar Chart'),
        ('dual_line_chart', 'Dual Line Chart'),
        ('line_chart', "Line Chart")

    )

    name = models.CharField(max_length=128)
    chart_type = models.CharField(max_length=128, choices=chart_types)
    slug = models.CharField(max_length=256, null=True, blank=True)
    end_point = models.CharField(max_length=64)
    number = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '-'.join([word.lower() for word in self.name.replace(')', '').replace('(', '').split()])

        return super().save(*args, **kwargs)
