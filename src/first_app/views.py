from pathlib import Path
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Greatest
from django.db.models import Sum
from django.shortcuts import (render, redirect,
                              get_object_or_404, resolve_url)
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from datetime import datetime, date
import xlwt
from django.contrib.auth import update_session_auth_hash
import plotly.express as px
import plotly.graph_objects as go
from django.core.files.base import ContentFile
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.db.models import Q
import pytz

from .forms import (SearchForm, AddPatientForm, ItemNumForm,
                    ExportExcelFrom, AddAppointementForm,
                    EditAppointementForm, AddConsultationForm,
                    TodayForm, AddAppointementConsultationForm,
                    CustomPasswordChangeForm, MedicamentForm,
                    AddAnalyseForm, ArretTravailFrom)
from .models import (Patient, ItemNum, Appointement, Consultation,
                     Medicament, BilanTest, Analyse, TestName, ArretTravail)
from consultation.models import (PdfArretTravailStore, NomMedicament,
                                 Payment, CertificatMedical,
                                 LettreOrientation, ConsultationDocument,
                                 MotifConsultation, ExamenClinique, InfoDoctor,
                                 Posologie, Quantite)
from appcon.models import (OrdonnacePdf, BilanPdf, FacturePdf, ArretPdf,
                            CertificatPdf, OrientationPdf)

################################################ dashboard views ##################################
@login_required
def dashboard(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                id = int(form.cleaned_data['id'])
                return redirect('patient_detail', pk=id)
            except:
                messages.error(request, 'Veuillez sélectionner un patient dans la liste proposé.')

    td = datetime.now()
    # rendez du jour
    td_app = Appointement.objects.filter(
        date__year=td.year,
        date__month=td.month,
        date__day=td.day,
    )

    return render(request,
                  'first_app/dashboard.html',
                  {
                      'section': 'dashboard',
                      'form': form,
                      'td_app': td_app,
                      'date_form': TodayForm(),
                  })

@login_required
def td_app(request):
    td = datetime.now()
    # rendez du jour
    td_app = Appointement.objects.filter(
        date__year=td.year,
        date__month=td.month,
        date__day=td.day,
    )
    return render(request,
                 'first_app/td_app.html',
                  {'td_app': td_app})

@login_required
def total_com_app(request):
    td = datetime.now()
    # comming appointement
    com_app = []
    td_min = datetime(td.year, td.month, td.day, td.hour)
    for x in Appointement.objects.all():
        if x.date_time >= td_min:
            com_app.append(x)
        else:
            x.delete()
    total_com_app = len(com_app)
    return HttpResponse(f'{total_com_app}')


######################################### Patient views #############################################################
@login_required
def autocomplete_patient(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = Patient.objects.annotate(
            similarity=TrigramSimilarity('first_name', query) +
            TrigramSimilarity('last_name', query),
        ).filter(similarity__gt=0.1).order_by('-similarity')
        patient_list = list()
        for p in qs:
            patient_list.append({'label': p.name, 'value': p.id})
        return JsonResponse(patient_list[:10], safe=False)


@login_required
def patients(request):
    # get patients list
    form = SearchForm()
    patients_list = Patient.objects.all()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            id = int(form.cleaned_data['id'])
            patients_list = [Patient.objects.get(pk=id)]

    try:
        item_num = request.user.itemnums.first()
        items_per_page = item_num.nums
    except:
        items_per_page = 10

    if request.method == 'POST':
        item_form = ItemNumForm(request.POST, instance=ItemNum(nums=items_per_page))
        if item_form.is_valid():
            request.user.itemnums.all().delete()
            item = item_form.save(commit=False)
            item.user = request.user
            item.save()
            items_per_page = item.nums
    else:
        item_form = ItemNumForm(instance=ItemNum(nums=items_per_page))

    paginator = Paginator(patients_list, items_per_page)
    page = request.GET.get('page', 1)
    try:
        patients = paginator.page(page)
    except PageNotAnInteger:
        patients = paginator.page(1)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)
    return render(request,
                  'first_app/patients.html',
                  {
                      'section': 'patients',
                      'patients': patients,
                      'page': page,
                      'form': form,
                      'items_per_page': items_per_page,
                      'item_form': item_form,
                  })

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            # get last patient
            try:
                lp = Patient.objects.first()
                p.num = lp.num + 1
            except Exception as e:
                p.num = 1
            p.save()
            resolved_url = resolve_url('patients')
            # add message
            messages.success(request, f'Le patient {p.name} a été ajouté avec succès')
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})
    else:
        form = AddPatientForm()

    return render(request, 'first_app/patient_form.html',
                  {'form': form})


@login_required
def add_patient_appointement(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            # get last patient
            try:
                lp = Patient.objects.first()
                p.num = lp.num + 1
            except Exception as e:
                p.num = 1
            p.save()
            resolved_url = resolve_url('add_appointement_new_patient', p.id)
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url,
                                })
    else:
        form = AddPatientForm()

    return render(request, 'first_app/patient_form.html',
                  {'form': form})


@login_required
def add_patient_consultation(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            # get last patient
            try:
                lp = Patient.objects.first()
                p.num = lp.num + 1
            except Exception as e:
                p.num = 1
            p.save()
            resolved_url = resolve_url('add_consultation', pk=p.id)
            # add message
            messages.success(request, f'Le patient {p.name} a été ajouté avec succès')
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})
    else:
        form = AddPatientForm()

    return render(request, 'first_app/patient_form.html',
                  {'form': form})


@login_required
def full_add_patient(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            # get last patient
            try:
                lp = Patient.objects.first()
                p.num = lp.num + 1
            except Exception as e:
                p.num = 1
            p.save()
            messages.success(request, f'Le patient {p.name} a été ajouté avec succès')
            return redirect('patients')
    else:
        form = AddPatientForm()

    return render(request, 'first_app/add_patient.html',
                  {
                      'section': 'add_patient',
                      'form': form
                  })


@login_required
def edit_patient(request, pk, page):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = AddPatientForm(request.POST, instance=patient)
        if form.is_valid():
            p = form.save()
            resolved_url = resolve_url('patients') + f'?page={page}'
            # add message
            messages.success(
                request, f'Le information du patient {p.name} ont été modifié avec succès')
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})
    else:
        form = AddPatientForm(instance=patient)

    return render(request, 'first_app/patient_update_form.html',
                  {'form': form,
                   'patient': patient})


@login_required
def delete_patient(request, pk, page):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.name
        patient.delete()
        resolved_url = resolve_url('patients') + f'?page={page}'
        messages.success(request, f'Le patient {name} a été supprimé avec succès')
        return HttpResponse(status=204,
                            headers={'HX-Redirect': resolved_url})
    return render(request, 'first_app/patient_delete.html',
                           {'patient': patient})

################################## Dossier Medical ####################

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    consultations_list = patient.consultations.all()
    return render(request, 'first_app/patient_detail.html',
                  {'patient': patient,
                   'consultations_list': consultations_list,
                   })

@login_required
def edit_patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = AddPatientForm(request.POST, instance=patient)
        if form.is_valid():
            p = form.save()
            resolved_url = resolve_url('patient_detail', patient.id)
            # add message
            messages.success(
                request, f'Le information du patient {p.name} ont été modifié avec succès')
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})
    else:
        form = AddPatientForm(instance=patient)

    return render(request, 'first_app/patient_update_form.html',
                  {'form': form,
                   'patient': patient})


@login_required
def chart_form(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    list_names = []
    for analyse in patient.analyses.all():
        list_names.append(analyse.name)
    test_names = set(list_names)
    return render(request, 'analyse/chart_form.html',
                  {'patient': patient, 'test_names': test_names})


@login_required
def add_chart(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        if request.POST['dropdownanalyse']:
            test_name = request.POST['dropdownanalyse']
            analyses = Analyse.objects.filter(name=test_name)[::-1]
            x = [c.date.strftime("%m/%d/%Y") for c in analyses]
            y = [c.value for c in analyses]

            config = {'displaylogo': False}
            fig = px.line(
                x=x,
                y=y)
            fig.update_traces(mode="markers+lines", marker_size=10)
            fig.update_layout(
                xaxis={
                    'tickangle': 40,
                    'title': 'Date'
                },
                yaxis_title="Valeur",
                title={
                    'text': f"{test_name}",
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font=dict(
                    family="Courier New, monospace",
                    size=20,
                    color="#000"
                )
            )
            chart = fig.to_html(config=config)
            return render(request, 'analyse/add_chart.html',
                          {'chart': chart,
                           'test_name': test_name})
        else:
            return HttpResponse(status=204,)
    return HttpResponse(status=204,)


@login_required
def add_analyse(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    td = datetime.now()
    analyses = patient.analyses.filter(
        created__year=td.year,
        created__month=td.month,
        created__day=td.day,
    )
    test_names = [test.name for test in TestName.objects.all()]
    form = AddAnalyseForm()
    response = render(request, 'analyse/add_analyse.html',
                      {'patient': patient,
                       'analyses': analyses,
                       'date_form': TodayForm(),
                       'test_names': test_names,
                       'form': form})
    response['HX-Trigger'] = 'analyseListChanged'
    return response


@login_required
def analyse_plus(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = AddAnalyseForm(request.POST)
        if form.is_valid and request.POST['dropdowtestname']:
            analyse = form.save(commit=False)
            analyse.patient = patient
            analyse.name = request.POST['dropdowtestname']
            analyse.save()

    td = datetime.now()
    analyses = patient.analyses.filter(
        created__year=td.year,
        created__month=td.month,
        created__day=td.day,
    )
    response = render(request, 'analyse/analyse_plus.html',
                      {'analyses': analyses})
    response['HX-Trigger'] = 'analyseListChanged'
    return response


@login_required
def delete_analyse(request, pk):
    analyse = get_object_or_404(Analyse, pk=pk)
    patient_id = analyse.patient.id
    analyse.delete()
    patient = get_object_or_404(Patient, pk=patient_id)
    td = datetime.now()
    analyses = patient.analyses.filter(
        created__year=td.year,
        created__month=td.month,
        created__day=td.day,
    )
    response = render(request, 'analyse/analyse_plus.html',
                      {'analyses': analyses})
    response['HX-Trigger'] = 'analyseListChanged'
    return response

##################### Appointemnt code ######################


@login_required
def autocomplete_appointement(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = Appointement.objects.annotate(
            similarity=TrigramSimilarity('patient__first_name', query) +
            TrigramSimilarity('patient__last_name', query),
        ).filter(similarity__gt=0.1).order_by('-similarity')
        appointements_list = list()
        for app in qs:
            appointements_list.append({'label': app.patient.name, 'value': app.patient.id})
        return JsonResponse(appointements_list[:10], safe=False)


@login_required
def appointements(request):
    # delete past appoint
    td = datetime.now()
    td_min = datetime(td.year, td.month, td.day, td.hour)
    for x in Appointement.objects.all():
        if x.date_time < td_min:
            x.delete()

    # get patients list
    form = SearchForm()
    appointements_list = Appointement.objects.all()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            id = int(form.cleaned_data['id'])
            patient = Patient.objects.get(pk=id)
            appointements_list = patient.appointements.all()
    try:
        item_num = request.user.itemnums.first()
        items_per_page = item_num.nums
    except:
        items_per_page = 10

    if request.method == 'POST':
        item_form = ItemNumForm(request.POST, instance=ItemNum(nums=items_per_page))
        if item_form.is_valid():
            request.user.itemnums.all().delete()
            item = item_form.save(commit=False)
            item.user = request.user
            item.save()
            items_per_page = item.nums
    else:
        item_form = ItemNumForm(instance=ItemNum(nums=items_per_page))

    paginator = Paginator(appointements_list, items_per_page)
    page = request.GET.get('page', 1)
    try:
        appointements = paginator.page(page)
    except PageNotAnInteger:
        appointements = paginator.page(1)
    except EmptyPage:
        appointements = paginator.page(paginator.num_pages)
    return render(request,
                  'first_app/appointements.html',
                  {
                      'section': 'appointements',
                      'appointements': appointements,
                      'page': page,
                      'form': form,
                      'items_per_page': items_per_page,
                      'item_form': item_form,
                  })

# add apointement
@login_required
def add_appointement(request):
    if request.method == 'POST':
        form = AddAppointementForm(request.POST)
        if form.is_valid():
            appointement = form.save(commit=False)
            try:
                patient_id = int(form.cleaned_data['patient_id'])
                patient = Patient.objects.get(pk=patient_id)
                appointement.patient = patient
                appointement.save()
                messages.success(request, 'Rendez-vous ajouté avec succès')
                return redirect('appointements')
            except:
                messages.error(
                    request, 'Veuillez sélectionner un patient dans la base de données ou en ajouter un nouveau')
        else:
            messages.error(
                request, 'Veuillez sélectionner un patient dans la base de données ou en ajouter un nouveau')
    else:
        form = AddAppointementForm()

    return render(request, 'first_app/add_appointement.html',
                  {
                      'section': 'add_appointement',
                      'form': form
                  })

@login_required
def add_appointement_new_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = AddAppointementForm(request.POST)
        if form.is_valid():
            appointement = form.save(commit=False)
            try:
                patient_id = int(form.cleaned_data['patient_id'])
                patient = Patient.objects.get(pk=patient_id)
                appointement.patient = patient
                appointement.save()
                messages.success(request, 'Rendez-vous ajouté avec succès')
                return redirect('appointements')
            except:
                messages.error(
                    request, 'Veuillez sélectionner un patient dans la base de données ou en ajouter un nouveau')
        else:
            messages.error(
                request, 'Veuillez sélectionner un patient dans la base de données ou en ajouter un nouveau')
    else:
        form = AddAppointementForm(initial={'patient': patient.name, 'patient_id': patient.id})

    return render(request, 'first_app/add_appointement.html',
                  {
                      'section': 'add_appointement',
                      'form': form
                  })


@login_required
def edit_appointement(request, pk, page):
    appointement = get_object_or_404(Appointement, pk=pk)
    if request.method == 'POST':
        form = EditAppointementForm(request.POST, instance=appointement)
        if form.is_valid():
            p = form.save()
            resolved_url = resolve_url('appointements') + f'?page={page}'
            # add message
            messages.success(request, f'Rendez-vous modifié avec succès')
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})
    else:
        form = EditAppointementForm(instance=appointement)

    return render(request, 'first_app/appointement_update_form.html',
                  {'form': form,
                   'appointement': appointement})


@login_required
def delete_appointement(request, pk, page):
    appointement = get_object_or_404(Appointement, pk=pk)
    rdv = appointement.rdv
    if request.method == 'POST':
        appointement.delete()
        resolved_url = resolve_url('appointements') + f'?page={page}'
        messages.success(request, f'Le {rdv} a été supprimé avec succès')
        return HttpResponse(status=204,
                            headers={'HX-Redirect': resolved_url})
    return render(request, 'first_app/appointement_delete.html',
                           {'rdv': rdv})

############################################### Consultation views ############################################
@login_required
def autocomplete_consultation(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = Consultation.objects.annotate(
            similarity=TrigramSimilarity('patient__first_name', query) +
            TrigramSimilarity('patient__last_name', query),
        ).filter(similarity__gt=0.1).order_by('-similarity')
        consultations_list = list()
        for con in qs:
            consultations_list.append({'label': con.patient.name, 'value': con.patient.id})
        return JsonResponse(consultations_list[:10], safe=False)


@login_required
def consultations(request):
    # get patients list
    form = SearchForm()
    consultations_list = Consultation.objects.all()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            id = int(form.cleaned_data['id'])
            patient = Patient.objects.get(pk=id)
            consultations_list = patient.consultations.all()

    try:
        item_num = request.user.itemnums.first()
        items_per_page = item_num.nums
    except:
        items_per_page = 10

    if request.method == 'POST':
        item_form = ItemNumForm(request.POST, instance=ItemNum(nums=items_per_page))
        if item_form.is_valid():
            request.user.itemnums.all().delete()
            item = item_form.save(commit=False)
            item.user = request.user
            item.save()
            items_per_page = item.nums
    else:
        item_form = ItemNumForm(instance=ItemNum(nums=items_per_page))

    paginator = Paginator(consultations_list, items_per_page)
    page = request.GET.get('page', 1)
    try:
        consultations = paginator.page(page)
    except PageNotAnInteger:
        consultations = paginator.page(1)
    except EmptyPage:
        consultations = paginator.page(paginator.num_pages)
    return render(request,
                  'first_app/consultations.html',
                  {
                      'section': 'consultations',
                      'consultations': consultations,
                      'page': page,
                      'form': form,
                      'items_per_page': items_per_page,
                      'item_form': item_form,
                  })


@login_required
def patient_consultation(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                id = int(form.cleaned_data['id'])
                return redirect('add_consultation', pk=id)
            except:
                messages.error(
                    request, 'Veuillez sélectionner un patient dans la base de données ou en ajouter un nouveau')
        else:
            messages.error(
                request, 'Veuillez sélectionner un patient dans la base de données ou en ajouter un nouveau')
    else:
        form = SearchForm()

    return render(request, 'first_app/patient_consultation.html',
                  {
                      'section': 'add_consultation',
                      'form': form
                  })


@login_required
def add_consultation(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    # create consultation
    consultation = Consultation.objects.create(patient=patient)
    form = AddConsultationForm()
    return render(request, 'first_app/add_consultation.html',
                  {
                      'section': 'add_consultation',
                      'form': form,
                      'patient': patient,
                      'consultation': consultation,
                      'date_form': TodayForm(),
                  })

@login_required
def submit_add_consultation(request, pk):
    if request.method == 'POST':
        form = AddConsultationForm(request.POST)
        if form.is_valid:
            # get consultation
            con = get_object_or_404(Consultation, pk=pk)
            patient = con.patient
            # get ordonnance
            medicament_list = [Medicament(name=m.name, posologie=m.posologie,
                                          nbr_unite=m.nbr_unite) for m in con.medicaments.all()]
            # get bilan
            bilan_list = [BilanTest(name=m.name) for m in con.tests.all()]
            # get facture
            payment_list = [Payment(description=p.description, price=p.price)
                            for p in con.payments.all()]

            # get arret de travail
            arret_travail = None
            try:
                arret_travail = ArretTravail(date1=con.arrettravail.date1,
                                             date2=con.arrettravail.date2)
            except:
                pass
            # get certificat medical
            certificat_medical = None
            try:
                certificat_medical = CertificatMedical(text=con.certificatmedical.text)
            except:
                pass
            # get lettre orientation
            lettre_orientation = None
            try:
                lettre_orientation = LettreOrientation(text=con.lettreorientation.text)
            except:
                pass
            con.delete()
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.pk = pk
            consultation.save()
            # get motifs and save new ones
            all_motif = [x.nom.lower() for x in MotifConsultation.objects.all()]
            motif_list = [x.strip().lower() for x in consultation.motif.split(',')]
            for x in motif_list:
                if x not in all_motif and len(x.strip()) != 0:
                    MotifConsultation.objects.create(nom=x.capitalize())
            # get examen and save new ones
            all_examen = [x.nom.lower() for x in ExamenClinique.objects.all()]
            examen_list = [x.strip().lower() for x in consultation.examen.split(',')]
            for x in examen_list:
                if x not in all_examen and len(x.strip()) != 0:
                    ExamenClinique.objects.create(nom=x.capitalize())

            # save ordonnance
            for med in medicament_list:
                med.consultation = consultation
                med.save()
            # create ordonnance pdf
            # get doctor info
            doctor = None
            info_doctor = InfoDoctor.objects.all()
            if info_doctor:
                doctor = info_doctor.first()
            # construct html string
            if len(medicament_list) != 0:
                ordonnance_string = render_to_string('ordonnance/ordonnance_template.html',
                                        {'consultation': consultation,
                                        'ordonnance': medicament_list,
                                        'doctor': doctor})
                ordonnance_result = HTML(string=ordonnance_string, base_url='http://localhost/').write_pdf()
                pdf_ord = ContentFile(ordonnance_result, f'ordonnance_{consultation.id}.pdf')
                OrdonnacePdf.objects.create(consultation=consultation, pdf=pdf_ord)
            # save bilan
            for test in bilan_list:
                test.consultation = consultation
                test.save()
            # save bilan pdf BilanPdf
            if len(bilan_list) != 0:
                bilan_string = render_to_string('bilan/bilan_template.html',
                                        {'consultation': consultation,
                                        'bilan': bilan_list,
                                        'doctor': doctor})
                bilan_result = HTML(string=bilan_string, base_url='http://localhost/').write_pdf()
                pdf_bilan = ContentFile(bilan_result, f'bilan_{consultation.id}.pdf')
                BilanPdf.objects.create(consultation=consultation, pdf=pdf_bilan)
            # save facture
            for payment in payment_list:
                payment.consultation = consultation
                payment.save()
            # save facture pdf
            if len(payment_list) != 0:
                total = 0
                for payment in payment_list:
                    total += payment.subtotal
                facture_string = render_to_string('facture/facture_template.html',
                                        {'consultation': consultation,
                                        'payments': payment_list,
                                        'total': total,
                                        'doctor': doctor})
                facture_result = HTML(string=facture_string, base_url='http://localhost/').write_pdf()
                pdf_facture = ContentFile(facture_result, f'facture_{consultation.id}.pdf')
                FacturePdf.objects.create(consultation=consultation, pdf=pdf_facture)

            # save arret_travail
            if arret_travail:
                arret_travail.consultation = consultation
                arret_travail.save()
                arrettravail__string = render_to_string('arret_travail/arret_travail_template.html',
                                               {'consultation': consultation,
                                                'arrettravail': arret_travail,
                                                'doctor': doctor})
                arrettravail_result = HTML(string=arrettravail__string, base_url='http://localhost/').write_pdf()
                pdf_arrettravail = ContentFile(arrettravail_result, f'arrettravail_{consultation.id}.pdf')
                ArretPdf.objects.create(consultation=consultation, pdf=pdf_arrettravail)

            # save certificat_medical
            if certificat_medical:
                certificat_medical.consultation = consultation
                certificat_medical.save()
                certificat_string = render_to_string('certificat_medical/certificat_medical_template.html',
                                        {'consultation': consultation,
                                        'certificat': certificat_medical,
                                        'doctor': doctor})
                certificat_result = HTML(string=certificat_string, base_url='http://localhost/').write_pdf()
                pdf_certificat = ContentFile(certificat_result, f'certificat_{consultation.id}.pdf')
                CertificatPdf.objects.create(consultation=consultation, pdf=pdf_certificat)

            # save lettre_orientation
            if lettre_orientation:
                lettre_orientation.consultation = consultation
                lettre_orientation.save()
                lettre_string = render_to_string('lettre_orientation/lettre_orientation_template.html',
                                        {'consultation': consultation,
                                        'lettre': lettre_orientation,
                                        'doctor': doctor})
                lettre_result = HTML(string=lettre_string, base_url='http://localhost/').write_pdf()
                pdf_lettre = ContentFile(lettre_result, f'lettre_{consultation.id}.pdf')
                OrientationPdf.objects.create(consultation=consultation, pdf=pdf_lettre)

            resolved_url = resolve_url('consultations')
            # add message
            messages.success(request, f'Consultation pour ajouté avec succès')
            return HttpResponse(status=204,
                                headers={'HX-Redirect': resolved_url})


@login_required
def edit_consultation(request, pk, page):
    # get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # get patient
    patient = consultation.patient
    if request.method == 'POST':
        form = AddConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            consul = form.save()
            # get motifs and save new ones
            all_motif = [x.nom.lower() for x in MotifConsultation.objects.all()]
            motif_list = [x.strip().lower() for x in consul.motif.split(',')]
            for x in motif_list:
                if x not in all_motif and len(x.strip()) != 0:
                    MotifConsultation.objects.create(nom=x.capitalize())
            # get examen and save new ones
            all_examen = [x.nom.lower() for x in ExamenClinique.objects.all()]
            examen_list = [x.strip().lower() for x in consul.examen.split(',')]
            for x in examen_list:
                if x not in all_examen and len(x.strip()) != 0:
                    ExamenClinique.objects.create(nom=x.capitalize())
            messages.success(request, f'Consultation pour {patient.name} modifié avec succès')
            resolved_url = resolve_url('consultations') + f'?page={page}'
            return redirect(resolved_url)
    else:
        form = AddConsultationForm(instance=consultation)

    return render(request, 'first_app/update_consultation.html',
                  {
                      'form': form,
                      'patient': patient,
                      'consultation': consultation,
                      'date_form': TodayForm(),
                  })


@login_required
def delete_consultation(request, pk, page):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST':
        consultation.delete()
        resolved_url = resolve_url('consultations') + f'?page={page}'
        messages.success(request, f'Le consultation a été supprimé avec succès')
        return HttpResponse(status=204,
                            headers={'HX-Redirect': resolved_url})
    return render(request, 'first_app/consultation_delete.html',)


@login_required
def cancel_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    resolved_url = resolve_url('consultations')
    messages.info(request, f'Consultation annuler')
    return HttpResponse(status=204,
                        headers={'HX-Redirect': resolved_url})


@login_required
def add_appointement_consultation(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        app_form = AddAppointementConsultationForm(request.POST)
        if app_form.is_valid():
            appointement = app_form.save(commit=False)
            appointement.patient = patient
            appointement.save()
            return render(request,
                          'consultation/appointement_added.html',
                          {'appointement': appointement, }
                          )
    else:
        app_form = AddAppointementConsultationForm()

    return render(request, 'consultation/appointement_fail.html',
                  {
                      'add': True,
                      'app_form': app_form
                  })


@login_required
def edit_appointement_consultation(request, pk):
    appointement = get_object_or_404(Appointement, pk=pk)
    patient = appointement.patient
    if request.method == 'POST':
        app_form = AddAppointementConsultationForm(request.POST, instance=appointement)
        if app_form.is_valid():
            appointement = app_form.save(commit=False)
            appointement.patient = patient
            appointement.save()
            return render(request,
                          'consultation/appointement_added.html',
                          {'appointement': appointement, }
                          )
    else:
        app_form = AddAppointementConsultationForm(instance=appointement)

    return render(request, 'consultation/appointement_fail.html',
                  {
                      'add': False,
                      'app_form': app_form
                  })

# Ordonnance views
@login_required
def ordonnance(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    medicaments = consultation.medicaments.all()
    form = MedicamentForm()
    response = render(request, 'consultation/ordonnance.html',
                      {'patient': patient,
                       'consultation': consultation,
                       'date_form': TodayForm(),
                       'medicaments': medicaments,
                       'form': form})
    response['HX-Trigger'] = 'ordonnanceChanged'
    return response


@login_required
def cancel_ordonnance(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.medicaments.all().delete()
    return HttpResponse(status=204, headers={'HX-Trigger': 'ordonnanceChanged'})


@login_required
def add_medicament(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = MedicamentForm(request.POST)
        if form.is_valid:
            medicament = form.save(commit=False)
            medicament.consultation = consultation
            medicament.save()

    medicaments = consultation.medicaments.all()
    response = render(request, 'consultation/add_medicament.html',
                      {'medicaments': medicaments})
    response['HX-Trigger'] = 'ordonnanceChanged'
    return response


@login_required
def delete_medicament(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    consultation_id = medicament.consultation.id
    medicament.delete()
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    medicaments = consultation.medicaments.all()
    response = render(request, 'consultation/add_medicament.html',
                      {'medicaments': medicaments})
    response['HX-Trigger'] = 'ordonnanceChanged'
    return response


@login_required
def autocomplete_medicament(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = NomMedicament.objects.annotate(
            similarity=TrigramSimilarity('nom', query)
        ).filter(similarity__gt=0.01).order_by('-similarity')
        medicament_list = list()
        for med in qs:
            medicament_list.append(med.full_name)
        return JsonResponse(medicament_list[:10], safe=False)


@login_required
def autocomplete_posologie(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = Posologie.objects.annotate(
            similarity=TrigramSimilarity('nom', query)
        ).filter(similarity__gt=0.01).order_by('-similarity')
        posologie_list = list()
        for p in qs:
            posologie_list.append(p.nom)
        return JsonResponse(posologie_list[:10], safe=False)

@login_required
def autocomplete_quantite(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = Quantite.objects.annotate(
            similarity=TrigramSimilarity('nom', query)
        ).filter(similarity__gt=0.01).order_by('-similarity')
        quantite_list = list()
        for p in qs:
            quantite_list.append(p.nom)
        return JsonResponse(quantite_list[:10], safe=False)


@login_required
def bilan(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    tests = consultation.tests.all()
    test_names = [test.name for test in TestName.objects.all()]
    return render(request, 'bilan/bilan.html',
                  {'patient': patient,
                   'consultation': consultation,
                   'date_form': TodayForm(),
                   'tests': tests,
                   'test_names': test_names,
                   })


@login_required
def add_test(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        if request.POST['dropdowTestBilanName']:
            test_name = request.POST['dropdowTestBilanName']
            BilanTest.objects.create(consultation=consultation,
                                     name=test_name)

    tests = consultation.tests.all()
    response = render(request, 'bilan/add_test.html',
                      {'tests': tests})
    response['HX-Trigger'] = 'bilanChanged'
    return response


@login_required
def delete_test(request, pk):
    test = get_object_or_404(BilanTest, pk=pk)
    consultation_id = test.consultation.id
    test.delete()
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    tests = consultation.tests.all()
    response = render(request, 'bilan/add_test.html',
                      {'tests': tests})
    response['HX-Trigger'] = 'bilanChanged'
    return response


@login_required
def cancel_bilan(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.tests.all().delete()
    return HttpResponse(status=204, headers={'HX-Trigger': 'bilanChanged'})


@login_required
def autocomplete_test(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = BilanTest.objects.annotate(
            similarity=TrigramSimilarity('name', query)
        ).filter(similarity__gt=0.01).order_by('-similarity')
        test_list = list()
        for test in qs:
            test_list.append(test.name)
        return JsonResponse(test_list[:5], safe=False)


# arret de travail views
@login_required
def arret_travail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    try:
        arret_travail = consultation.arrettravail
        form = ArretTravailFrom({'date1': arret_travail.date1,
                                'date2': arret_travail.date2})
    except Exception as e:
        form = ArretTravailFrom()
    return render(request, 'arret_travail/arret_travail.html',
                  {'patient': patient,
                   'consultation': consultation,
                   'date_form': TodayForm(),
                   'form': form,
                   })

# submit arret de travail
@login_required
def add_arret_travail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    if request.method == 'POST':
        form = ArretTravailFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                arret_travail = consultation.arrettravail
                arret_travail.date1 = cd['date1']
                arret_travail.date2 = cd['date2']
            except:
                arret_travail = ArretTravail.objects.create(
                    consultation=consultation,
                    date1=cd['date1'],
                    date2=cd['date2'],
                )
            response = render(request,
                              'arret_travail/arret_travail_added.html',
                              {'arret_travail': arret_travail,
                               'patient': patient,
                               'consultation': consultation}
                              )
            response['HX-Trigger'] = 'arretTravailChanged'
            return response
        else:
            return render(request, 'arret_travail/arret_travail_fail.html',
                          {
                              'consultation': consultation,
                              'form': form,
                          })


@login_required
def edit_arret_travail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    arret_travail = consultation.arrettravail
    form = ArretTravailFrom({'date1': arret_travail.date1,
                            'date2': arret_travail.date2})
    return render(request, 'arret_travail/arret_travail_fail.html',
                  {
                      'consultation': consultation,
                      'form': form,
                  })


@login_required
def cancel_arret_travail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    try:
        arrettravail = consultation.arrettravail
        arrettravail.delete()
        return HttpResponse(status=204)
    except:
        return HttpResponse(status=204)


@login_required
def arret_travail_overview(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    patient = consultation.patient
    arret_travail = consultation.arrettravails.first()
    return render(request, 'arret_travail/arret_travail_overview.html',
                  {
                      'patient': patient,
                      'arret_travail': arret_travail,
                  })


@login_required
def arret_travail_pdf(request, pk):
    # get doctor info
    doctor = None
    info_doctor = InfoDoctor.objects.all()
    if info_doctor:
        doctor = info_doctor.first()
    # Get consultation
    consultation = get_object_or_404(Consultation, pk=pk)
    # Get lettre if it exist
    try:
        arrettravail = consultation.arrettravail
    except:
        arrettravail = None
    # construct html string
    html_string = render_to_string('arret_travail/arret_travail_template.html',
                                   {'consultation': consultation,
                                    'arrettravail': arrettravail,
                                    'doctor': doctor})
    # pdfkit.from_string(html_string, f'{settings.MEDIA_ROOT}pdfs/arret_travail/arret.pdf')
    result = HTML(string=html_string, base_url='http://localhost/').write_pdf()
    patient_name = consultation.patient.full_name.replace(" ", "_")
    pdf_name = f'arrêt_de_travail_pour_{ patient_name }.pdf'
    pdf_content = ContentFile(result, pdf_name)
    try:
        PdfArretTravailStore.objects.all().delete()
    except:
        pass
    pdf = PdfArretTravailStore.objects.create(file=pdf_content)
    return render(request, 'arret_travail/arret_travail_overview.html',
                  {
                      'pdf_url': pdf.file.url,
                  })


####################################### Parametre section ######################
# Back to it later
@login_required
def export_excel(request):
    # init the excel file
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Patients')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    # write header
    columns = ['Prénom', 'Nom', 'Année de naissance', 'Sexe', 'CNIE', 'Mutuelle',
               'Numéro de téléphone', 'E-mail', 'Adresse']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    if request.method == 'POST':
        form = ExportExcelFrom(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            date_1 = cd['date1']
            date_2 = cd['date2']
            casablanca = pytz.timezone('Africa/Casablanca')
            date1 = datetime(date_1.year, date_1.month, date_1.day, 0, 0, tzinfo=casablanca)
            date2 = datetime(date_2.year, date_2.month, date_2.day, 23, 59, tzinfo=casablanca)
            # define the http response
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename=list_patient_entre_du' + \
                str(date_1) + '_au_' + str(date_2) + '.xls'
            # get rows data
            rows = Patient.objects.filter(
                Q(created__gte=date1), Q(created__lte=date2)
            ).values_list(*['first_name', 'last_name', 'year_of_birth',
                            'sexe', 'cnie', 'mutuelle', 'phone_number', 'email', 'address'])
            font_style = xlwt.XFStyle()
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]).capitalize(), font_style)
            wb.save(response)
            return response
    else:
        form = ExportExcelFrom()
    return render(request, 'first_app/export_excel.html', {
        'section': 'export_data',
        'form': form})

# password change
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'section': 'change_password',
        'form': form,
    })


# autocomplete  for consultation
@login_required
def autocomplete_motif(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = MotifConsultation.objects.annotate(
            similarity=TrigramSimilarity('nom', query),
        ).filter(similarity__gt=0.01).order_by('-similarity')
        motif_list = list()
        for p in qs:
            motif_list.append(p.nom)
        return JsonResponse(motif_list[:10], safe=False)


@login_required
def autocomplete_examen(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        qs = ExamenClinique.objects.annotate(
            similarity=TrigramSimilarity('nom', query),
        ).filter(similarity__gt=0.01).order_by('-similarity')
        examen_list = list()
        for p in qs:
            examen_list.append(p.nom)
        return JsonResponse(examen_list[:10], safe=False)
