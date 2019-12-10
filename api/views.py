from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q, Count, Sum, Avg
from django.db.models.functions import TruncMonth

from submissions.models import FaultSource, Area, Submission, Classification, Supplier, IssueCategory, SubmissionStatus
from core.mixins import GeneralMixins
from core.models import Chart
from .serializers import ChartSerializer


class ChartsListView(generics.ListAPIView):
    serializer_class = ChartSerializer
    queryset = Chart.objects.order_by('number')


class UpdateSubmissionIds(GeneralMixins, views.APIView):

    def get(self, request, start_date, end_date):
        self.update_submission_ids(request, start_date, end_date)
        return Response({'success': 'submission ids updated successfully'})


class DefectOriginAreaCount(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        # query to get originator submissions count

        defect_submissions = Area.objects.filter(
            Q(defect_submissions__isnull=False) &
            Q(defect_submissions__id__in=submission_ids)
        ).annotate(
            count=Count('defect_submissions')
        ).values('name', 'count')

        return Response({
            'labels': [defect_submission['name'] for defect_submission in defect_submissions],
            'data': [defect_submission['count'] for defect_submission in defect_submissions]
        })


class FaultSourceCount(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        fault_source_submissions = FaultSource.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids)
        ).annotate(
            count=Count('submissions')
        ).values('name', 'count')

        return Response(
            dict(
                labels=[fault_source_submission['name'] for fault_source_submission in fault_source_submissions],
                data=[fault_source_submission['count'] for fault_source_submission in fault_source_submissions],
                background_colors=[f"rgba{self.get_rgba_color()}" for i in range(fault_source_submissions.count())]
            )
        )


class DefectOriginAreaNCRCost(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        defect_submissions = Area.objects.filter(
            Q(defect_submissions__isnull=False) &
            Q(defect_submissions__id__in=submission_ids) &
            Q(defect_submissions__total_ncr_cost__isnull=False)
        ).annotate(
            total_ncr_cost=Sum('defect_submissions__total_ncr_cost')
        ).values('name', 'total_ncr_cost')

        return Response({
            'labels': [defect_submission['name'] for defect_submission in defect_submissions],
            'data': [round(defect_submission['total_ncr_cost'], 2) for defect_submission in defect_submissions]
        })


class SupplierNCRCost(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        suppliers = Supplier.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids) &
            Q(submissions__total_ncr_cost__isnull=False)
        ).annotate(
            total_ncr_cost=Sum('submissions__total_ncr_cost')
        ).values('name', 'total_ncr_cost')

        return Response({
            'labels': [supplier['name'] for supplier in suppliers],
            'data': [round(supplier['total_ncr_cost'], 2) for supplier in suppliers]
        })


class SubmissionStatusNCRCost(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        statuses = SubmissionStatus.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids) &
            Q(submissions__total_ncr_cost__isnull=False)
        ).annotate(
            total_ncr_cost=Sum('submissions__total_ncr_cost')
        ).values('name', 'total_ncr_cost')

        data = [round(status['total_ncr_cost'], 2) for status in statuses]
        max_value = max(data)

        return Response({
            'labels': [status['name'] for status in statuses],
            'data': data,
            'background_colors': [f"rgba{self.get_rgba_color()}" for _ in range(statuses.count())],
            'max_value': max_value,
            'step': max(max_value / 10, 1)
        })


class CurrentAreaIssues(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        current_areas = Area.objects.filter(
            Q(current_area_submissions__id__in=submission_ids)
        ).annotate(
            count=Count('id')
        ).values('name', 'count')

        return Response(
            dict(
                labels=[current_area['name'] for current_area in current_areas],
                data=[current_area['count'] for current_area in current_areas],
                background_colors=[f"rgba{self.get_rgba_color()}" for i in range(current_areas.count())]
            )
        )


class AverageTimeWasted(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()
        average_time_wasted = Submission.objects.filter(
            Q(minutes_wasted__isnull=False) &
            Q(id__in=submission_ids)
        ).aggregate(
            average=Avg('minutes_wasted')
        )['average']

        return Response(
            dict(metric=round(average_time_wasted, 2) if average_time_wasted else None)
        )


class AverageTimetoDone(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()
        average_time_to_done = Submission.objects.filter(
            Q(time_to_close__isnull=False) &
            Q(id__in=submission_ids)
        ).aggregate(
            average=Avg('time_to_close')
        )['average']

        return Response(
            dict(metric=round(average_time_to_done, 2) if average_time_to_done else None)
        )


class DefectCategoriesPerSupplier(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()
        supplier_defect_categories = IssueCategory.objects.filter(
            issues__submissions__id__in=submission_ids,
            issues__submissions__supplier__isnull=False
        ).annotate(
            category_count=Count('id')
        ).values('name', 'issues__submissions__supplier__name', 'category_count').order_by(
            'issues__submissions__supplier__name')

        category_names = [category.name for category in IssueCategory.objects.all()]

        supplier_defect_data = dict()

        max_value = 0

        for item in supplier_defect_categories:
            supplier_name = item['issues__submissions__supplier__name']

            if supplier_name not in supplier_defect_data:
                supplier_defect_data[supplier_name] = dict(
                    label=supplier_name,
                    background_color=f"rgba{self.get_rgba_color()}",
                    data=[0 for _ in category_names]
                )

                supplier_defect_data[supplier_name]['data'][category_names.index(item['name'])] = item['category_count']

            else:
                supplier_defect_data[supplier_name]['data'][category_names.index(item['name'])] = item['category_count']

            max_value = max(max_value, max(supplier_defect_data[supplier_name]['data']))

        return Response(
            dict(
                labels=category_names,
                data=[item for _, item in supplier_defect_data.items()],
                max_value=max_value,
                step=max(max_value // 5, 1)
            )
        )


class TotalCONQCost(GeneralMixins, views.APIView):

    def get(self, request):
        """
        Calculates the total CONQ Cost

        :param request:
        :return:
        """

        submission_ids = self.get_submission_ids()
        total_cost = Submission.objects.filter(
            Q(id__in=submission_ids) &
            Q(total_ncr_cost__isnull=False)
        ).aggregate(total_cost=Sum('total_ncr_cost'))['total_cost']

        return Response(
            dict(metric=round(total_cost, 2) if total_cost else None)
        )


class TotalPartCost(GeneralMixins, views.APIView):

    def get(self, request):
        """
        Calculates the total Part Cost

        :param request:
        :return:
        """

        submission_ids = self.get_submission_ids()
        total__part_cost = Submission.objects.filter(
            Q(id__in=submission_ids) &
            Q(total_part_cost__isnull=False)
        ).aggregate(total__part_cost=Sum('total_part_cost'))['total__part_cost']

        return Response(
            dict(metric=round(total__part_cost, 2) if total__part_cost else None)
        )


class FaultSourceNCRCost(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        fault_sources = FaultSource.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids) &
            Q(submissions__total_ncr_cost__isnull=False)
        ).annotate(
            total_ncr_cost=Sum('submissions__total_ncr_cost')
        ).values('name', 'total_ncr_cost')

        return Response({
            'labels': [fault_source['name'] for fault_source in fault_sources],
            'data': [round(fault_source['total_ncr_cost'], 2) for fault_source in fault_sources],
            'background_colors': [f"rgba{self.get_rgba_color()}" for i in range(fault_sources.count())]
        })


class LiabilityCountPerMonth(GeneralMixins, views.APIView):

    def get(self, request):

        submission_ids = self.get_submission_ids()

        fault_sources = FaultSource.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids)
        )

        buhler_fault_source = fault_sources.filter(name='Buhler')
        supplier_fault_source = fault_sources.filter(name='Supplier')

        buhler_data = buhler_fault_source.annotate(
            month=TruncMonth('submissions__input_start_date')
        ).values('month').annotate(
            count=Count('id')
        ).values(
            'month', 'count'
        )

        supplier_data = supplier_fault_source.annotate(
            month=TruncMonth('submissions__input_start_date')
        ).values(
            'month'
        ).annotate(
            count=Count('id')
        ).values(
            'month', 'count'
        )

        buhler_data_as_dict = dict()
        supplier_data_as_dict = dict()

        for entry in buhler_data:
            buhler_data_as_dict[entry['month']] = entry['count']

        for entry in supplier_data:
            supplier_data_as_dict[entry['month']] = entry['count']

        months_one = [entry['month'] for entry in buhler_data]
        months_two = [entry['month'] for entry in supplier_data]

        months = sorted(list(set(months_one + months_two)))

        supplier_data = [supplier_data_as_dict[month] if month in supplier_data_as_dict else 0 for month in months]
        buhler_data = [buhler_data_as_dict[month] if month in buhler_data_as_dict else 0 for month in months]

        final_data = list()
        labels = [self.datetime_to_year_month(month) for month in months]

        final_data.append(
            dict(
                label='Supplier',
                data=supplier_data,
                background_color="rgba(66,208,163,0.2)",
                border_color=f"rgba{self.get_rgba_color()}"
            )
        )

        final_data.append(
            dict(
                label='Buhler',
                data=buhler_data,
                background_color="rgba(76,132,255,0.2)",
                border_color=f"rgba{self.get_rgba_color()}"
            )
        )

        return Response(dict(
            step_size=max([max(supplier_data), max(buhler_data)]) * 1.2 // 5,
            labels=labels,
            datasets=final_data
        ))


class LiabilityAverageClosingTimePerMonth(GeneralMixins, views.APIView):

    def get(self, request):

        submission_ids = self.get_submission_ids()

        fault_sources = FaultSource.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids) &
            Q(submissions__time_to_close__isnull=False)
        )
        buhler_fault_source = fault_sources.filter(name='Buhler')
        supplier_fault_source = fault_sources.filter(name='Supplier')

        buhler_data = buhler_fault_source.annotate(
            month=TruncMonth('submissions__input_start_date')
        ).values('month').annotate(
            average_time=Avg('submissions__time_to_close')
        ).values(
            'month', 'average_time'
        )

        supplier_data = supplier_fault_source.annotate(
            month=TruncMonth('submissions__input_start_date')
        ).values('month').annotate(
            average_time=Avg('submissions__time_to_close')
        ).values(
            'month', 'average_time'
        )

        buhler_data_as_dict = dict()
        supplier_data_as_dict = dict()

        for entry in buhler_data:
            buhler_data_as_dict[entry['month']] = entry['average_time']

        for entry in supplier_data:
            supplier_data_as_dict[entry['month']] = entry['average_time']

        months_one = [entry['month'] for entry in buhler_data]
        months_two = [entry['month'] for entry in supplier_data]

        months = sorted(list(set(months_one + months_two)))

        supplier_data = [supplier_data_as_dict[month] if month in supplier_data_as_dict else 0 for month in months]
        buhler_data = [buhler_data_as_dict[month] if month in buhler_data_as_dict else 0 for month in months]

        labels = [self.datetime_to_year_month(month) for month in months]
        final_data = list()

        final_data.append(
            dict(
                label='Supplier',
                data=supplier_data,
                border_color=f"rgba{self.get_rgba_color()}"
            )
        )

        final_data.append(
            dict(
                label='Buhler',
                data=buhler_data,
                border_color=f"rgba{self.get_rgba_color()}"
            )
        )

        return Response(dict(
            labels=labels,
            datasets=final_data
        ))


class CONQPerLiability(GeneralMixins, views.APIView):

    def get(self, request):

        submission_ids = self.get_submission_ids()

        fault_sources = FaultSource.objects.filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids) &
            Q(submissions__total_ncr_cost__isnull=False)
        )
        buhler_fault_source = fault_sources.filter(name='Buhler')
        supplier_fault_source = fault_sources.filter(name='Supplier')

        buhler_data = buhler_fault_source.annotate(
            month=TruncMonth('submissions__input_start_date')
        ).values('month').annotate(
            total_cost=Sum('submissions__total_ncr_cost')
        ).values(
            'month', 'total_cost'
        )

        supplier_data = supplier_fault_source.annotate(
            month=TruncMonth('submissions__input_start_date')
        ).values('month').annotate(
            total_cost=Sum('submissions__total_ncr_cost')
        ).values(
            'month', 'total_cost'
        )

        buhler_data_as_dict = dict()
        supplier_data_as_dict = dict()

        for entry in buhler_data:
            buhler_data_as_dict[entry['month']] = entry['total_cost']

        for entry in supplier_data:
            supplier_data_as_dict[entry['month']] = entry['total_cost']

        months_one = [entry['month'] for entry in buhler_data]
        months_two = [entry['month'] for entry in supplier_data]

        months = sorted(list(set(months_one + months_two)))

        supplier_data = [supplier_data_as_dict[month] if month in supplier_data_as_dict else 0 for month in months]
        buhler_data = [buhler_data_as_dict[month] if month in buhler_data_as_dict else 0 for month in months]

        labels = [self.datetime_to_year_month(month) for month in months]
        final_data = list()

        final_data.append(
            dict(
                label='Supplier',
                data=supplier_data,
                border_color=f"rgba{self.get_rgba_color()}"
            )
        )

        final_data.append(
            dict(
                label='Buhler',
                data=buhler_data,
                border_color=f"rgba{self.get_rgba_color()}"
            )
        )

        return Response(dict(
            labels=labels,
            datasets=final_data
        ))


class CONQPerClassification(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()

        classifications = Classification.objects.prefetch_related('submissions').filter(
            Q(submissions__isnull=False) &
            Q(submissions__id__in=submission_ids) &
            Q(submissions__total_ncr_cost__isnull=False)
        )

        classification_names = [classification['name'] for classification in Classification.objects.values('name')]
        classification_dicts = list()
        months = list()

        for name in classification_names:
            current_classifications = classifications.filter(
                name=name
            ).annotate(
                month=TruncMonth('submissions__input_start_date')
            ).values('month').annotate(
                total_cost=Sum('submissions__total_ncr_cost')
            ).values(
                'name', 'month', 'total_cost'
            )

            dict_data = dict()

            for classification in current_classifications:
                dict_data[classification['month']] = classification['total_cost']

            months = list(set(months + [classification['month'] for classification in current_classifications]))
            classification_dicts.append(dict_data)

        months = sorted(months)

        final_data = list()
        max_height = 0
        for i in range(len(classification_dicts)):
            classification_dict = classification_dicts[i]

            data = [classification_dict[month] if month in classification_dict else 0 for month in months]
            max_height = max(max_height, max(data) * 1.2)
            final_data.append(
                dict(
                    label=classification_names[i],
                    data=data,
                    background_color=f"rgba{self.get_rgba_color()}",
                    border_color=f"rgba{self.get_rgba_color()}"
                )
            )

        labels = [self.datetime_to_year_month(month) for month in months]

        return Response(dict(
            max_height=max_height,
            labels=labels,
            datasets=final_data
        ))


class CONQPerMonth(GeneralMixins, views.APIView):

    def get(self, request):
        submission_ids = self.get_submission_ids()
        submissions = Submission.objects.filter(
            id__in=submission_ids,
            total_ncr_cost__isnull=False
        ).annotate(
            month=TruncMonth('input_start_date')
        ).values(
            'month'
        ).annotate(
            total_cost=Sum('total_ncr_cost')
        ).values(
            'month', 'total_cost'
        )

        months = [self.datetime_to_year_month(submission['month']) for submission in submissions]
        data = [submission['total_cost'] for submission in submissions]

        return Response(
            dict(
                labels=months,
                data=data
            )
        )
