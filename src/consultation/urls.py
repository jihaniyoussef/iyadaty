from django.urls import path
from . import views

urlpatterns = [
    # certificat medical
    path('certificat-medical/<int:pk>/', views.certificat_medical,
     name='certificat_medical'),
    path('add-certificat-medical/<int:pk>/', views.add_certificat_medical,
     name='add_certificat_medical'),
    path('cancel-certificat-medical/<int:pk>/', views.cancel_certificat_medical,
     name='cancel_certificat_medical'),
    path('edit-certificat-medical/<int:pk>/', views.edit_certificat_medical,
     name='edit_certificat_medical'),
    path('certificat-medical-pdf/<int:pk>/', views.certificat_medical_pdf,
     name="certificat_medical_pdf"),
    # lettre d'orientation
    path('lettre-orientation/<int:pk>/', views.lettre_orientation,
     name='lettre_orientation'),
    path('add-lettre-orientation/<int:pk>/', views.add_lettre_orientation,
     name='add_lettre_orientation'),
    path('cancel-lettre-orientation/<int:pk>/', views.cancel_lettre_orientation,
     name='cancel_lettre_orientation'),
    path('edit-lettre-orientation/<int:pk>/', views.edit_lettre_orientation,
     name='edit_lettre_orientation'),
    path('lettre-orientation-pdf/<int:pk>/', views.lettre_orientation_pdf,
     name="lettre_orientation_pdf"),
    # Bilan pdf
    path('bilan-pdf/<int:pk>/', views.bilan_pdf,
     name="bilan_pdf"),
    # Bilan pdf
    path('ordonnance-pdf/<int:pk>/', views.ordonnance_pdf,
     name="ordonnance_pdf"),
    #### facture links
    path('facture/<int:pk>/', views.facture,
     name="facture"),
    path('cancel-facture/<int:pk>/', views.cancel_facture,
     name="cancel_facture"),
    path('add-payment/<int:pk>/', views.add_payment,
     name="add_payment"),
    path('delete-payment/<int:pk>/', views.delete_payment,
     name="delete_payment"),
    path('facture-pdf/<int:pk>/', views.facture_pdf,
     name="facture_pdf"),
    # Consultation document list
    path('consultation-document/<int:pk>/', views.consultation_document,
     name="consultation_document"),
    path('add-consultation-document/<int:pk>/', views.add_consultation_document,
     name="add_consultation_document"),
    path('delete-consultation-document/<int:pk>/', views.delete_consultation_document,
     name="delete_consultation_document"),
    path('show-consultation-document/<int:pk>/', views.show_consultation_document,
     name="show_consultation_document"),
    # Salle d'attent
    path('salle-attent/', views.salle_attent,
     name="salle_attent"),
    path('delete-attent/<int:pk>/', views.delete_attent,
     name="delete_attent"),
    path('add-attent/<int:pk>/', views.add_attent,
     name="add_attent"),
    path('patient-en-attente/', views.patient_en_attente,
     name="patient_en_attente"),
     # Info doctor
     path('render-info-doctor/', views.render_info_doctor,
      name="render_info_doctor"),
     path('add-info-doctor/', views.add_info_doctor,
      name="add_info_doctor"),
     # num delegues
     path('delegue/', views.delegue,
      name="delegue"),
     path('add-delegue/', views.add_delegue,
      name="add_delegue"),
     # Pdfs in medical folder
     path('patient-detail-ordonnance/<int:pk>/', views.patient_detail_ordonnance,
      name="patient_detail_ordonnance"),
     path('patient-detail-bilan/<int:pk>/', views.patient_detail_bilan,
      name="patient_detail_bilan"),
     path('patient-detail-arret-travail/<int:pk>/', views.patient_detail_arret_travail,
      name="patient_detail_arret_travail"),
     path('patient-detail-certificat-medical/<int:pk>/', views.patient_detail_certificat_medical,
      name="patient_detail_certificat_medical"),
     path('patient-detail-lettre-orientation/<int:pk>/', views.patient_detail_lettre_orientation,
      name="patient_detail_lettre_orientation"),
     path('patient-detail-facture/<int:pk>/', views.patient_detail_facture,
      name="patient_detail_facture"),
        ]