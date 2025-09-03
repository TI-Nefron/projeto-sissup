import uuid
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Patient
from documents.models import Document
from billing.models import Guide

def patient_search_view(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '').strip()
    patients = None

    if query:
        patients = Patient.objects.select_related('clinic').filter(
            Q(full_name__icontains=query) | Q(cpf__exact=query),
            is_active=True
        )

    context = {
        'query': query,
        'patients': patients
    }

    if "HX-Request" in request.headers:
        return render(request, 'dialysis/_patient_search_results.html', context)
    
    return render(request, 'dialysis/patient_search.html', context)

def patient_checklist_view(request: HttpRequest, patient_id: uuid.UUID) -> HttpResponse:
    patient = get_object_or_404(
        Patient.objects.select_related('clinic', 'payer').prefetch_related(
            Prefetch(
                'guides',
                queryset=Guide.objects.prefetch_related('documents')
            )
        ),
        id=patient_id
    )
    
    patient_content_type = ContentType.objects.get_for_model(patient)
    patient_documents = Document.objects.filter(
        content_type=patient_content_type,
        object_id=patient.id
    )

    context = {
        'patient': patient,
        'patient_documents': patient_documents,
    }
    return render(request, 'dialysis/patient_checklist.html', context)