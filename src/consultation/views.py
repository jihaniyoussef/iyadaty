from django.shortcuts import (render, redirect,
                              get_object_or_404, resolve_url)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import datetime, date
from django.contrib import messages

from .models import (CertificatMedical, PdfStore, LettreOrientation,
                    PdfLettreStore, PdfBilanStore, PdfOrdonnanceStore,
                    Payment, PdfFactureStore, ConsultationDocument,
                    SalleAttente, InfoDoctor, DelegNum)
from .forms import (CertificatMedicalForm, LettreOrientationForm,
                    PaymentForm, ConsultationDocumentForm,
                    InfoDoctorForm, DelegNumForm, SalleAttenteForm)
from first_app.models import Consultation, Profile, Patient
from first_app.forms import TodayForm

from django.template import RequestContext
import os

### delegue medicaux
@login_required
def delegue(request):
    list_deleg_num = DelegNum.objects.all()
    num_delegues = 0
    if list_deleg_num:
        deleg = list_deleg_num.first()
        num_delegues = deleg.nums
    return HttpResponse(f'{num_delegues}')

@login_required
def add_delegue(request):
    # get table or create new one
    list_deleg_num = DelegNum.objects.all()
    if list_deleg_num:
        deleg = list_deleg_num.first()
    else:
        deleg = DelegNum.objects.create(nums=0)
    # handel submit form
    if request.method == 'POST':
        form = DelegNumForm(request.POST, instance=deleg)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204,
                headers={'HX-Trigger': 'delegueChanged'})
    else:
        form = DelegNumForm(instance=deleg)
    return render(request, 'delegue/add_delegue.html',
                {'form': form})

####### update info doctor
@login_required
def render_info_doctor(request):
    info_doctor = InfoDoctor.objects.all()
    doctor = None
    if info_doctor:
        doctor = info_doctor.first()
    return render(request,
                    'info_doctor/render_info_doctor.html',
                    {'doctor': doctor,
                    'section': 'render_info_doctor'})

@login_required
def add_info_doctor(request):
    info_doctor = InfoDoctor.objects.all()
    # patient = consultation.patient
    if request.method == 'POST':
        if info_doctor:
            doctor = info_doctor.first()
            form = InfoDoctorForm(request.POST, request.FILES, instance=doctor)
        else:
            form = InfoDoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('render_info_doctor')
    else:
        if info_doctor:
            doctor = info_doctor.first()
            form = InfoDoctorForm(instance=doctor)
        else:
            form = InfoDoctorForm()
    return render(request,
                    'info_doctor/add_info_doctor.html',
                    {'form': form,
                    'info_doctor': info_doctor,
                    'section': 'render_info_doctor'})



    if info_doctor:
        doctor = info_doctor.first()
    return render(request,
                    'info_doctor/render_info_doctor.html',
                    {'doctor': doctor,
                    'section': 'render_info_doctor'})

############## Salle d'attente #######
@login_required
def patient_en_attente(request):
    td = datetime.now()
    td_max = datetime(td.year, td.month, td.day)
    salle_attent = []
    for p in  SalleAttente.objects.all():
        date_time = datetime(p.created.year, p.created.month, p.created.day)
        if date_time < td_max:
            p.delete()
        else:
            salle_attent.append(p)
    html = f'{len(salle_attent)}'
    return HttpResponse(html)

@login_required
def salle_attent(request):
    td = datetime.now()
    td_max = datetime(td.year, td.month, td.day)
    salle_attent = []
    for p in  SalleAttente.objects.all():
        date_time = datetime(p.created.year, p.created.month, p.created.day)
        if date_time < td_max:
            p.delete()
        else:
            salle_attent.append(p)
    return render(request,
                'salle_attent/salle_attent.html',
                {'salle_attent': salle_attent})

@login_required
def delete_attent(request, pk):
    attent = get_object_or_404(SalleAttente, pk=pk)
    name = attent.patient.full_name
    if request.method == 'POST':
        attent.delete()
        return HttpResponse(status=204,
                            headers={'HX-Trigger': 'SalleAttenteChanged'})
    return render(request, 'salle_attent/delete_attent.html',
                           {'name': name})


@login_required
def add_attent(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = SalleAttenteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.patient = patient
            user.save()
            name = patient.full_name
            resolved_url = resolve_url('dashboard')
            messages.success(request, f"{name} a été ajouté à la salle d'attente")
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})
    return render(request, 'salle_attent/add_attent.html',
                        {'form': form})

############################ certificat médical ###########################
@login_required
def certificat_medical(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    try:
        certificat = consultation.certificatmedical
        form = CertificatMedicalForm(instance=certificat)
    except ObjectDoesNotExist:
        text = f'<p>&emsp;Je soussigne, Certifie avoir examine ce jour, <strong>{patient.full_name}</strong>, Agé de <strong>{patient.age} ans.</strong></p>'\
                '<p>Qui présente</p>'
        form = CertificatMedicalForm({'text': text })
    return render(request, 'certificat_medical/certificat_medical.html',
                            {'patient': patient,
                            'consultation': consultation,
                            'date_form': TodayForm(),
                            'form': form,
                            })

# submit certificat medical
@login_required
def add_certificat_medical(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    # patient = consultation.patient
    if request.method == 'POST':
        form = CertificatMedicalForm(request.POST)
        if form.is_valid():
            try:
                certificat = consultation.certificatmedical
                certificat.text = form.cleaned_data['text']
                certificat.save()
            except:
                certificat = form.save(commit=False)
                certificat.consultation = consultation
                certificat.save()
            response = render(request,
                        'certificat_medical/certificat_medical_added.html',
                        {'certificat': certificat,
                         'consultation': consultation,
                         })
            response['HX-Trigger'] = 'certificatChanged'
            return response
        else:
            return render(request, 'certificat_medical/certificat_medical_fail.html',
                {
                'consultation': consultation,
                'form': form,
                })

@login_required
def cancel_certificat_medical(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        certificat = consultation.certificatmedical
        certificat.delete()
        return HttpResponse(status=204,)
    except:
        return HttpResponse(status=204,)

@login_required
def edit_certificat_medical(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    certificat = consultation.certificatmedical
    form = CertificatMedicalForm(instance=certificat)
    return render(request, 'certificat_medical/certificat_medical_fail.html',
        {
        'consultation': consultation,
        'form': form,
        })

@login_required
def certificat_medical_pdf(request, pk):
    # get doctor info
    doctor = None
    info_doctor = InfoDoctor.objects.all()
    if info_doctor:
        doctor = info_doctor.first()
    # Get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # Get certificate if it exist
    try:
        certificat = consultation.certificatmedical
    except:
        certificat = None
    # construct html string
    html_string = render_to_string('certificat_medical/certificat_medical_template.html',
                            {'consultation': consultation,
                            'certificat': certificat,
                            'doctor': doctor})
    result = HTML(string=html_string, base_url='http://localhost/').write_pdf()
    # stylesheets=[CSS(settings.STATIC_ROOT +  '/css/generate_html.css')]
    patient_name = consultation.patient.full_name.replace(" ", "_")
    pdf_name = f'certificat_médical_{ patient_name }.pdf'
    pdf_content = ContentFile(result, pdf_name)
    try:
        PdfStore.objects.all().delete()
    except:
        pass
    pdf = PdfStore.objects.create(file=pdf_content)
    return render(request, 'certificat_medical/overview_certificat_medical.html',
        {
        'pdf_url': pdf.file.url,
        })

################## Lettre d'orientation ########
@login_required
def lettre_orientation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    try:
        lettre = consultation.lettreorientation
        form = LettreOrientationForm(instance=lettre)
    except ObjectDoesNotExist:
        text = f'<h3>&emsp;Cher confrère / consoeur</h3>'\
                f'<p>Permuttez moi de vous adressez <strong>{patient.full_name}</strong></p>'\
                '<p>Pour...</p>'
        form = LettreOrientationForm({'text': text })

    return render(request, 'lettre_orientation/lettre_orientation.html',
                            {'patient': patient,
                            'consultation': consultation,
                            'date_form': TodayForm(),
                            'form': form,
                            })

# submit lettre orientation
@login_required
def add_lettre_orientation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    # patient = consultation.patient
    if request.method == 'POST':
        form = LettreOrientationForm(request.POST)
        if form.is_valid():
            try:
                lettre = consultation.lettreorientation
                lettre.text = form.cleaned_data['text']
                lettre.save()
            except:
                lettre = form.save(commit=False)
                lettre.consultation = consultation
                lettre.save()
            response = render(request,
                        'lettre_orientation/lettre_orientation_added.html',
                        {'lettre': lettre,
                         'consultation': consultation,
                         })
            response['HX-Trigger'] = 'lettreChanged'
            return response
        else:
            return render(request, 'lettre_orientation/lettre_orientation_fail.html',
                {
                'consultation': consultation,
                'form': form,
                })

@login_required
def cancel_lettre_orientation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        lettre = consultation.lettreorientation
        lettre.delete()
        return HttpResponse(status=204)
    except:
        return HttpResponse(status=204)

@login_required
def edit_lettre_orientation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    lettre = consultation.lettreorientation
    form = LettreOrientationForm(instance=lettre)
    return render(request, 'lettre_orientation/lettre_orientation_fail.html',
        {
        'consultation': consultation,
        'form': form,
        })

@login_required
def lettre_orientation_pdf(request, pk):
    # get doctor info
    doctor = None
    info_doctor = InfoDoctor.objects.all()
    if info_doctor:
        doctor = info_doctor.first()
    # Get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # Get lettre if it exist
    try:
        lettre = consultation.lettreorientation
    except:
        lettre = None
    # construct html string
    html_string = render_to_string('lettre_orientation/lettre_orientation_template.html',
                            {'consultation': consultation,
                            'lettre': lettre,
                            'doctor': doctor})
    result = HTML(string=html_string, base_url='http://localhost/').write_pdf()
    patient_name = consultation.patient.full_name.replace(" ", "_")
    pdf_name = f'lettre_orientation_{ patient_name }.pdf'
    pdf_content = ContentFile(result, pdf_name)
    try:
        PdfLettreStore.objects.all().delete()
    except:
        pass
    pdf = PdfLettreStore.objects.create(file=pdf_content)
    return render(request, 'lettre_orientation/overview_lettre_orientation.html',
        {
        'pdf_url': pdf.file.url,
        })

################## Bilan pdf ########
@login_required
def bilan_pdf(request, pk):
    # get doctor info
    doctor = None
    info_doctor = InfoDoctor.objects.all()
    if info_doctor:
        doctor = info_doctor.first()
    # Get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # Get bilan list
    bilan = consultation.tests.all()
    # construct html string
    html_string = render_to_string('bilan/bilan_template.html',
                            {'consultation': consultation,
                            'bilan': bilan,
                            'doctor': doctor})
    result = HTML(string=html_string, base_url='http://localhost/').write_pdf()
    patient_name = consultation.patient.full_name.replace(" ", "_")
    pdf_name = f'bilan_pour_{ patient_name }.pdf'
    pdf_content = ContentFile(result, pdf_name)
    try:
        PdfBilanStore.objects.all().delete()
    except:
        pass
    pdf = PdfBilanStore.objects.create(file=pdf_content)
    return render(request, 'lettre_orientation/overview_lettre_orientation.html',
        {
        'pdf_url': pdf.file.url,
        })

################## Ordonnance pdf ########
@login_required
def ordonnance_pdf(request, pk):
    # get doctor info
    doctor = None
    info_doctor = InfoDoctor.objects.all()
    if info_doctor:
        doctor = info_doctor.first()
    # Get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # Get medicament list
    ordonnance = consultation.medicaments.all()
    # construct html string
    html_string = render_to_string('ordonnance/ordonnance_template.html',
                            {'consultation': consultation,
                            'ordonnance': ordonnance,
                            'doctor': doctor})
    result = HTML(string=html_string, base_url='http://localhost/').write_pdf()
    patient_name = consultation.patient.full_name.replace(" ", "_")
    pdf_name = f'ordonnance_pour_{ patient_name }.pdf'
    pdf_content = ContentFile(result, pdf_name)
    try:
        PdfOrdonnanceStore.objects.all().delete()
    except:
        pass
    pdf = PdfOrdonnanceStore.objects.create(file=pdf_content)
    return render(request, 'lettre_orientation/overview_lettre_orientation.html',
        {
        'pdf_url': pdf.file.url,
        })

############################ Facture #####################
@login_required
def facture(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    payments = consultation.payments.all()
    form = PaymentForm()
    response = render(request, 'facture/facture.html',
                            {'patient': patient,
                            'consultation': consultation,
                            'date_form': TodayForm(),
                            'payments': payments,
                            'form': form})
    response['HX-Trigger'] = 'factureChanged'
    return response

@login_required
def cancel_facture(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.payments.all().delete()
    return HttpResponse(status=204, headers={'HX-Trigger': 'factureChanged'})

@login_required
def add_payment(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid:
            payment = form.save(commit=False)
            payment.consultation = consultation
            payment.save()

    payments = consultation.payments.all()
    response = render(request, 'facture/add_payment.html',
                        {'payments': payments})
    response['HX-Trigger'] = 'factureChanged'
    return response

@login_required
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    consultation_id = payment.consultation.id
    payment.delete()
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    payments = consultation.payments.all()
    response = render(request, 'facture/add_payment.html',
                        {'payments': payments})
    response['HX-Trigger'] = 'factureChanged'
    return response

@login_required
def facture_pdf(request, pk):
    # get doctor info
    doctor = None
    info_doctor = InfoDoctor.objects.all()
    if info_doctor:
        doctor = info_doctor.first()
    # Get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # Get medicament list
    payments = consultation.payments.all()
    total = 0
    for payment in payments:
        total += payment.subtotal
    # construct html string
    html_string = render_to_string('facture/facture_template.html',
                            {'consultation': consultation,
                            'payments': payments,
                            'total': total,
                            'doctor': doctor})
    result = HTML(string=html_string, base_url='http://localhost/').write_pdf()
    patient_name = consultation.patient.full_name.replace(" ", "_")
    pdf_name = f'facture_pour_{ patient_name }.pdf'
    pdf_content = ContentFile(result, pdf_name)
    try:
        PdfFactureStore.objects.all().delete()
    except:
        pass
    pdf = PdfFactureStore.objects.create(file=pdf_content)
    return render(request, 'lettre_orientation/overview_lettre_orientation.html',
        {
        'pdf_url': pdf.file.url,
        })

########################### consultation document ################
@login_required
def consultation_document(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    document_list = consultation.documents.all()
    return render(request, 'consultation_document/consultation_document.html',
                            {'consultation': consultation,
                            'documents': document_list,
                            })


@login_required
def add_consultation_document(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST" and request.FILES:
        form = ConsultationDocumentForm(request.POST, request.FILES)
        if form.is_valid:
            document = form.save(commit=False)
            document.consultation = consultation
            document.save()
            form = ConsultationDocumentForm()
            response = render(request, 'consultation_document/add_consultation_document.html',
                                {'form': form})
            response['HX-Trigger'] = 'documentListChanged'
            return response
    else:
        form = ConsultationDocumentForm()
    return render(request, 'consultation_document/add_consultation_document.html',
                        {'form': form})

@login_required
def delete_consultation_document(request, pk):
    document = get_object_or_404(ConsultationDocument, pk=pk)
    if request.method == 'POST':
        document.delete()
        return HttpResponse(status=204,
            headers={'HX-Trigger': 'documentListChanged'})
    return render(request, 'consultation_document/document_delete.html')


@login_required
def show_consultation_document(request, pk):
    document = get_object_or_404(ConsultationDocument, pk=pk)
    document_url = document.file.url
    title = document.name
    extension = document_url.rsplit('.')[-1]
    ex_list = ['doc', 'docx', 'xlsx', 'xlx', 'pptx', 'ppt', 'pptm']
    ex_img = ['png', 'jpeg', 'jpe', 'jpg']
    return render(request, 'consultation_document/show_document.html',
                {'document_url': document_url,
                'title': title,
                'ex_img': ex_img,
                'ex_list': ex_list,
                'extension': extension.lower()})


################# pdfs in consultation details ####
def patient_detail_ordonnance(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        pdf_url = consultation.ordonnacepdf.pdf.url
    except Exception as e:
        pdf_url = None
    return render(request, 'patient_detail/patient_detail_ordonnance.html',
                    {'pdf_url': pdf_url})

def patient_detail_bilan(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        pdf_url = consultation.bilanpdf.pdf.url
    except Exception as e:
        pdf_url = None
    return render(request, 'patient_detail/patient_detail_bilan.html',
                    {'pdf_url': pdf_url})

def patient_detail_arret_travail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        pdf_url = consultation.arretpdf.pdf.url
    except Exception as e:
        pdf_url = None
    return render(request, 'patient_detail/patient_detail_arret_travail.html',
                    {'pdf_url': pdf_url})
# # work here
def patient_detail_certificat_medical(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        pdf_url = consultation.certificatpdf.pdf.url
    except Exception as e:
        pdf_url = None
    return render(request, 'patient_detail/patient_detail_certificat_medical.html',
                    {'pdf_url': pdf_url})

def patient_detail_lettre_orientation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        pdf_url = consultation.orientationpdf.pdf.url
    except Exception as e:
        pdf_url = None
    return render(request, 'patient_detail/patient_detail_lettre_orientation.html',
                    {'pdf_url': pdf_url})

def patient_detail_facture(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        pdf_url = consultation.facturepdf.pdf.url
    except Exception as e:
        pdf_url = None
    return render(request, 'patient_detail/patient_detail_facture.html',
                    {'pdf_url': pdf_url})
