from django.db import models
from django.utils.translation import gettext_lazy as _

class PatientDocumentType(models.TextChoices):
    ID = 'ID', _('Documento de Identidade')
    CPF = 'CPF', _('CPF')
    CNS = 'CNS', _('Cartão SUS')
    COMP_RES = 'COMP_RES', _('Comprovante de Residência')
    CONSENT = 'CONSENT', _('Termo de Consentimento Geral')

class GuideDocumentType(models.TextChoices):
    LAUDO = 'LAUDO', _('Laudo Nefrológico')
    EXAME = 'EXAME', _('Exame Laboratorial')
    PRESC = 'PRESC', _('Prescrição')
    SESS = 'SESS', _('Folha de Sessão')
    AUTORIZACAO = 'AUTORIZACAO', _('Autorização Prévia')

AllDocumentTypes = PatientDocumentType.choices + GuideDocumentType.choices