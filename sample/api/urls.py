from django.urls import path
from . import views
app_name = 'sample'

urlpatterns = [
    path('sample/',
         views.SampleListView.as_view(),
         name='sample_list'),
    path('sample/<pk>/',
         views.SampleDetailView.as_view(),
         name='sample_detail'),
    path('get-token/', views.Login.as_view(),
         name='get-token')
]
