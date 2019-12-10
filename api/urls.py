from django.urls import path
import api.views as api_views

urlpatterns = [
    path('charts', api_views.ChartsListView.as_view()),
    path('update_submission_ids/<str:start_date>/<str:end_date>', api_views.UpdateSubmissionIds.as_view()),
    path('defect_origin_area_count',
         api_views.DefectOriginAreaCount.as_view()),
    path('fault_source_count', api_views.FaultSourceCount.as_view()),
    path('defect_origin_area_ncr_cost',
         api_views.DefectOriginAreaNCRCost.as_view()),
    path('supplier_ncr_cost', api_views.SupplierNCRCost.as_view()),
    path('current_area_issues',
         api_views.CurrentAreaIssues.as_view()),
    path('average_time_wasted', api_views.AverageTimeWasted.as_view()),
    path('average_time_to_done', api_views.AverageTimetoDone.as_view()),
    path('defect_categories_per_supplier',
         api_views.DefectCategoriesPerSupplier.as_view()),
    path('total_conq_cost', api_views.TotalCONQCost.as_view()),
    path('total_part_cost', api_views.TotalPartCost.as_view()),
    path('fault_source_ncr_cost', api_views.FaultSourceNCRCost.as_view()),
    path('submission_status_ncr_cost', api_views.SubmissionStatusNCRCost.as_view()),
    path('liability_count_per_month', api_views.LiabilityCountPerMonth.as_view()),
    path('liability_average_closing_time_per_month', api_views.LiabilityAverageClosingTimePerMonth.as_view()),
    path('conq_per_classification', api_views.CONQPerClassification.as_view()),
    path('conq_per_liability', api_views.CONQPerLiability.as_view()),
    path('conq_per_month', api_views.CONQPerMonth.as_view())

]
