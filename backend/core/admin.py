from django.contrib import admin
from .models import (
    Company,
    Project,
    Document,
    DocumentVersion,
    AuditLog,
)


# =========================
# INLINE: DOCUMENT VERSIONS
# =========================
class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 0
    readonly_fields = (
        "version_number",
        "uploaded_by",
        "uploaded_at",
    )
    ordering = ("-version_number",)

    def has_add_permission(self, request, obj=None):
        return False  # versions should be added via workflow, not admin


# =========================
# COMPANY
# =========================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


# =========================
# PROJECT
# =========================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "company",
        "status",
        "start_date",
        "end_date",
    )
    list_filter = ("company", "status")
    search_fields = ("code", "name")
    ordering = ("company__name", "code")
    autocomplete_fields = ("company",)


# =========================
# DOCUMENT
# =========================
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "document_number",
        "title",
        "project",
        "discipline",
        "doc_type",
        "status",
        "created_by",
        "created_at",
    )
    list_filter = (
        "project__company",
        "project",
        "discipline",
        "doc_type",
        "status",
    )
    search_fields = (
        "document_number",
        "title",
    )
    readonly_fields = ("created_by", "created_at")
    ordering = ("document_number",)
    autocomplete_fields = ("project",)
    inlines = [DocumentVersionInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# =========================
# DOCUMENT VERSION
# =========================
@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "version_number",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("document__project",)
    search_fields = ("document__document_number",)
    readonly_fields = (
        "version_number",
        "uploaded_by",
        "uploaded_at",
    )
    ordering = ("-uploaded_at",)

    def has_add_permission(self, request):
        return False  # enforced via API/workflow

    def has_change_permission(self, request, obj=None):
        return False  # versions are immutable


# =========================
# AUDIT LOG (READ-ONLY)
# =========================
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "entity_type",
        "entity_id",
        "action",
        "performed_by",
        "performed_at",
    )
    list_filter = ("entity_type", "action")
    search_fields = ("entity_id",)
    readonly_fields = (
        "entity_type",
        "entity_id",
        "action",
        "old_value",
        "new_value",
        "performed_by",
        "performed_at",
    )
    ordering = ("-performed_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
