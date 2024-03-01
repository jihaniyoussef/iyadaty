from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import ServiceConsultationForm
from .models import ServiceConsultation
from first_app.models import Consultation
from first_app.forms import AddConsultationForm
from consultation.models import MotifConsultation, ExamenClinique


@login_required
def consultation_detail(request, id):
    consultation = get_object_or_404(Consultation, id=id)
    return render(request, 'appcon/consultation_detail.html',
            {'consultation': consultation})

@login_required
def edit_consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
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
            return HttpResponse(status=204,
                headers={'HX-Trigger': 'ConsultationDetailChanged'})
    else:
        form = AddConsultationForm(instance=consultation)

    return render(request, 'appcon/edit_consultation_detail.html',
                  {'form': form,})


########################### Frais de la consultation ################
@login_required
def consultation_services(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    service_list = consultation.frais_consultation.all()
    total = 0
    for service in service_list:
        total += service.prix
    return render(request, 'appcon/services.html',
                            {'consultation': consultation,
                            'services': service_list,
                            'total': total,
                            })

@login_required
def delete_consultation_service(request, pk):
    service = get_object_or_404(ServiceConsultation, pk=pk)
    if request.method == 'POST':
        service.delete()
        return HttpResponse(status=204,
            headers={'HX-Trigger': 'serviceListChanged'})
    return render(request, 'appcon/service_delete.html')


@login_required
def add_consultation_service(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = ServiceConsultationForm(request.POST)
        if form.is_valid:
            service = form.save(commit=False)
            service.consultation = consultation
            service.save()
            form = ServiceConsultationForm()
            response = render(request, 'appcon/add_consultation_service.html',
                                {'form': form})
            response['HX-Trigger'] = 'serviceListChanged'
            return response
    else:
        form = ServiceConsultationForm()
    return render(request, 'appcon/add_consultation_service.html',
                        {'form': form, 'pk': pk})
