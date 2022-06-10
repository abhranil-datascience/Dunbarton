from django.urls import path
from DunbartonApp import views
urlpatterns = [
    path('dunbarton/ScanAndAssign',views.ScanAndAssignPageFunction, name='ScanAndAssignPageFunction'),
    path('dunbarton/ScanAndAudit',views.ScanAndAuditPageFunction, name='ScanAndAuditPageFunction')
]
