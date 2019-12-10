from django.db.models import Q
from submissions.models import Submission
from django.core.cache import cache

import random
import datetime
import json


class GeneralMixins:

    @staticmethod
    def get_rgba_color():
        return tuple([random.randint(0, 256) for _ in range(4)])

    @staticmethod
    def update_submission_ids(request, start_date, end_date):
        filters = dict(
            start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
            end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
            progress_ids=[int(id) for id in request.GET.getlist('progressFilter[]', list())],
            supplier_ids=[int(id) for id in request.GET.getlist('supplierFilter[]', list())],
            liability_ids=[int(id) for id in request.GET.getlist('liabilityFilter[]', list())],
            classification_ids=[int(id) for id in request.GET.getlist('classificationFilter[]', list())]
        )

        submissions = Submission.objects.filter(
            Q(input_start_date__gte=start_date) &
            Q(input_start_date__lte=end_date)
        ).filter(
            Q(progress_id__in=filters['progress_ids'])
        ).filter(
            Q(defect_origin_area_id__in=filters['liability_ids'])
        ).filter(
            supplier_id__in=filters['supplier_ids']
        ).filter(classification_id__in=filters['classification_ids']).values('id')

        print(submissions.count())

        cache.set('submission_ids', json.dumps([submission['id'] for submission in submissions]))

    @staticmethod
    def get_submission_ids():

        submission_ids = cache.get('submission_ids')

        if submission_ids:
            return json.loads(submission_ids)

        else:
            return [submission['id'] for submission in Submission.objects.values('id')]

    def datetime_to_year_month(self, date):
        return date.strftime("%b-%Y")
