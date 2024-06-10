from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe, SafeString

from candidates.models import Candidate, Tag


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    fields = ('username', 'candidate_photo', 'photo', 'first_name', 'last_name', 'email', 'gender',
              'about', 'country', 'tags', 'is_active', 'is_staff',)
    readonly_fields = ('is_staff', 'candidate_photo')
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_staff', 'is_fake', 'is_active', 'last_login',)
    list_display_links = ('username',)
    list_editable = ('is_active',)
    ordering = ('-is_active', '-is_staff', 'is_fake', '-pk',)
    actions = ('set_active', 'set_inactive',)
    search_fields = ('username', 'first_name', 'last_name',)
    list_filter = ('is_fake', 'is_active', 'is_staff',)
    filter_horizontal = ('tags',)
    list_per_page = 20
    save_on_top = True

    def has_add_permission(self, request: WSGIRequest) -> None:  # noqa: U100
        return

    @admin.display(description='Candidate photo')
    def candidate_photo(self, candidate_obj: Candidate) -> SafeString | str:
        # mark_safe so that tags are not escaped
        return candidate_obj.photo and mark_safe(f'<img src={candidate_obj.photo.url} width=100>') or 'No photo'

    @admin.action(description='Set as active')
    def set_active(self, request: WSGIRequest, qs: QuerySet) -> None:
        update_dict = {'is_active': True}
        self.change_qs(request, qs, update_dict)

    @admin.action(description='Set as inactive')
    def set_inactive(self, request: WSGIRequest, qs: QuerySet) -> None:
        update_dict = {'is_active': False}
        self.change_qs(request, qs, update_dict)

    def change_qs(self, request: WSGIRequest, qs: QuerySet, update_dict: dict) -> None:
        count = qs.update(**update_dict)
        self.message_user(request, f'Updated {count} records.')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
