from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from . import views


urlpatterns = [
    # login logout
    path('login/', auth_views.LoginView.as_view(
        authentication_form=CustomLoginForm),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # page d'acceuil
    path('', views.dashboard, name='dashboard'),
    path('total-com-app/', views.total_com_app, name='total_com_app'),
    path('td-app/', views.td_app, name='td_app'),
    # patients autocomplete_patient
    path('autocomplete-patient/', views.autocomplete_patient, name='autocomplete_patient'),
    path('patients/', views.patients, name='patients'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('full-add-patient/', views.full_add_patient, name='full_add_patient'),
    path('add-patient-appointement/', views.add_patient_appointement, name='add_patient_appointement'),
    path('add-appointement-new-patient/<int:pk>/', views.add_appointement_new_patient, name='add_appointement_new_patient'),
    path('update-patient/<int:pk>/<int:page>/', views.edit_patient, name='edit_patient'),
    path('delete-patient/<int:pk>/<int:page>/', views.delete_patient, name='delete_patient'),
    # patient detail
    path('detail-patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('edit-patient-detail/<int:pk>/', views.edit_patient_detail, name='edit_patient_detail'),
    # appointements
    path('autocomplete-appointement/', views.autocomplete_appointement, name='autocomplete_appointement'),
    path('appointements/', views.appointements, name='appointements'),
    path('add-appointement/', views.add_appointement, name='add_appointement'),
    path('add-appointement/', views.add_appointement, name='add_appointement'),
    path('update-appointement/<int:pk>/<int:page>/',
         views.edit_appointement, name='edit_appointement'),
    path('delete-appointement/<int:pk>/<int:page>/',
         views.delete_appointement, name='delete_appointement'),
    # consultation
    path('add-patient-consultation/', views.add_patient_consultation, name='add_patient_consultation'),
    path('autocomplete-consultation/', views.autocomplete_consultation, name='autocomplete_consultation'),
    path('consultations/', views.consultations, name='consultations'),
    path('patient-consultation/', views.patient_consultation, name='patient_consultation'),
    path('add-consultation/<int:pk>/', views.add_consultation, name='add_consultation'),
    path('submit-add-consultation/<int:pk>/',
         views.submit_add_consultation, name='submit_add_consultation'),
    # # work on it now
    path('delete-consultation/<int:pk>/<int:page>/',
         views.delete_consultation, name='delete_consultation'),
    path('edit-consultation/<int:pk>/<int:page>/', views.edit_consultation, name='edit_consultation'),
    path('cancel-consultation/<int:pk>/', views.cancel_consultation, name='cancel_consultation'),
    path('add-appointement-consultation/<int:pk>/',
         views.add_appointement_consultation, name='add_appointement_consultation'),
    path('edit-appointement-consultation/<int:pk>/',
         views.edit_appointement_consultation, name='edit_appointement_consultation'),
    # ordonnance link
    path('ordonnance/<int:pk>/', views.ordonnance, name='ordonnance'),
    path('cancel-ordonnance/<int:pk>/', views.cancel_ordonnance, name='cancel_ordonnance'),
    path('add-medicament/<int:pk>/', views.add_medicament, name='add_medicament'),
    path('delete-medicament/<int:pk>/', views.delete_medicament, name='delete_medicament'),
    path('autocomplete-medicament/', views.autocomplete_medicament, name='autocomplete_medicament'),
    # Bilan links
    path('bilan/<int:pk>/', views.bilan, name='bilan'),
    path('add-test/<int:pk>/', views.add_test, name='add_test'),
    path('delete-test/<int:pk>/', views.delete_test, name='delete_test'),
    path('cancel-bilan/<int:pk>/', views.cancel_bilan, name='cancel_bilan'),
    path('autocomplete-test/', views.autocomplete_test, name='autocomplete_test'),
    # Arret de travail links
    path('arret-travail/<int:pk>/', views.arret_travail, name='arret_travail'),
    path('add-arret-travail/<int:pk>/', views.add_arret_travail, name='add_arret_travail'),
    path('edit-arret-travail/<int:pk>/', views.edit_arret_travail, name='edit_arret_travail'),
    path('arret-travail-pdf/<int:pk>/', views.arret_travail_pdf,
         name='arret_travail_pdf'),
    path('cancel-arret-travail/<int:pk>/', views.cancel_arret_travail,
         name='cancel_arret_travail'),
    # Analyses
    path('add-analyse/<int:pk>/', views.add_analyse, name='add_analyse'),
    path('analyse-plus/<int:pk>/', views.analyse_plus, name='analyse_plus'),
    path('delete-analyse/<int:pk>/', views.delete_analyse, name='delete_analyse'),
    path('add-chart/<int:pk>/', views.add_chart, name='add_chart'),
    path('chart-form/<int:pk>/', views.chart_form, name='chart_form'),
    # export_excel
    path('export-excel/', views.export_excel, name='export_excel'),
    path('change-password/', views.change_password, name='change_password'),
    # consultation auto-complete
    path('autocomplete-motif/', views.autocomplete_motif,
         name='autocomplete_motif'),
    path('autocomplete-examen/', views.autocomplete_examen,
         name='autocomplete_examen'),
    path('autocomplete-posologie/', views.autocomplete_posologie,
         name='autocomplete_posologie'),
    path('autocomplete-quantite/', views.autocomplete_quantite,
         name='autocomplete_quantite'),
]
