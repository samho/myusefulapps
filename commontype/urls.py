from django.urls import path
from commontype import views
app_name = 'commontype'

urlpatterns = [
    path('list/<int:page_id>', views.listall, name='commontype_list'),
    path('add/', views.commontype_add, name='commontype_new'),
    # path('details/<int:type_id>', views.details, name='commontype_details'),
]
