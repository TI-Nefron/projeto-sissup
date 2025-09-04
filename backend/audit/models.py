import hashlib
import json
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class AuditDecision(models.Model):
    """
    Records a decision made by an auditor regarding a specific Guide.

    This model serves as the electronic signature and audit trail for the process,
    creating a non-repudiable record by hashing the guide's state and its
    associated documents at the time of the decision.
    """
    class Decision(models.TextChoices):
        APPROVED = 'APPROVED', _('Aprovado')
        REJECTED = 'REJECTED', _('Recusado com Pendência')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    guide = models.ForeignKey(
        'billing.Guide',  # Using string reference to avoid circular import
        verbose_name=_("Guia Auditada"),
        on_delete=models.CASCADE,
        related_name="audit_decisions"
    )
    decision = models.CharField(
        verbose_name=_("Decisão"),
        max_length=16,
        choices=Decision.choices
    )
    comments = models.TextField(
        verbose_name=_("Comentários/Justificativa"),
        blank=True
    )
    
    # --- Electronic Signature Fields (Step 1) ---
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Auditor"),
        on_delete=models.PROTECT,
        related_name="audits_performed"
    )
    audited_at = models.DateTimeField(
        verbose_name=_("Data da Auditoria"),
        auto_now_add=True,
        editable=False
    )
    payload_hash = models.CharField(
        verbose_name=_("Hash da Carga Probatória (Assinatura)"),
        max_length=64,
        editable=False,
        help_text=_("Hash SHA-256 do estado da guia e seus documentos no momento da auditoria.")
    )

    class Meta:
        verbose_name = _("Decisão de Auditoria")
        verbose_name_plural = _("Decisões de Auditoria")
        ordering = ['-audited_at']

    def __str__(self):
        # The # type: ignore is for Pylance, as Django adds get_..._display dynamically
        return f"{self.get_decision_display()} por {self.auditor.username} em {self.audited_at.strftime('%d/%m/%Y')}" # type: ignore

    def _generate_payload_hash(self):
        """
        Creates a deterministic hash of the guide's data and its documents' hashes.
        This serves as the core of the non-repudiation electronic signature.
        """
        document_hashes = sorted([
            doc.sha256 for doc in self.guide.documents.all()
        ])
        
        payload = {
            "guide_id": str(self.guide.id),
            "guide_status_at_audit": self.guide.status,
            "auditor_id": self.auditor.id,
            "decision": self.decision,
            "timestamp": self.audited_at.isoformat(),
            "document_hashes": document_hashes,
        }
        
        # Use sort_keys and compact separators for a consistent JSON string
        payload_string = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(payload_string.encode('utf-8')).hexdigest()
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate the payload hash on initial creation.
        """
        if not self.pk:
            self.payload_hash = self._generate_payload_hash()
        super().save(*args, **kwargs)