from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('excel_download', views.ExcelDownload.as_view(),
         name='excel-download'),
    path('excel_table', views.ExcelTable.as_view(),
         name='excel-table'),
    path('populate_db', views.PopulateDB.as_view(), name='Populate_db'),
    path('search_submissions', views.SearchSubmissions.as_view(),
         name='part-number-filtered-submissions')
]
