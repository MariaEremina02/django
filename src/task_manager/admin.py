from django.contrib import admin
from account.models import CustomUser
from task_manager.models import Tasks, Tags, Projects, ProjectDetails, Comments, Attachment
from django.contrib import messages
from django.utils.safestring import mark_safe
from task_manager.models.task import TaskStatus


admin.site.register(CustomUser)
admin.site.register(Tags)



#инлайн для комментариев
class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1

#инлайн для вложений
class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 1

#инлайн для ProjectDetails
class ProjectDetailsInline(admin.StackedInline):
    model = ProjectDetails
    extra = 0


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    fields = ('name', 'description')
    inlines = [ProjectDetailsInline]

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):

    #список полей
    list_display = (
        'id',
        'name',
        'status',
        'priority',
        'priority_status',
        'assignee',
    )
    exclude = ("is_reopened",)

    list_display_links = ('name', 'status')

    #редактирование
    list_editable = ('priority',)
    list_filter = ('status', 'priority',)

    search_fields = ("name",)
    list_per_page = 20
    ordering = ("-priority", "name")
    save_on_top = True
    actions = ("make_canceled", "decrease_priority")

    readonly_fields = ('created_at', 'comments_count', 'comments_html')

    #layout
    fields = (
        ('name', 'status'),
        'description',
        'priority',
        'assignee',
        'created_at',
        'comments_count',
        'comments_html'
    )

    # inline
    inlines = [CommentInline, AttachmentInline]

    def priority_status(self, obj):
        if obj.priority < 3:
            return "LOW"
        if obj.priority < 5:
            return "MEDIUM"
        return "HIGH"

    priority_status.string = ""
    priority_status.short_description = "Приоритет статуса"

    #кастом поля

    def name_status(self, obj):
        return f"{obj.name} ({obj.status})"
    name_status.short_description = "Name + Status"

    @admin.display(ordering='assignee__email', description='Email исполнителя')
    def assignee_email(self, obj):
        return obj.assignee.email if obj.assignee else "-"

    def comments_count(self, obj):
        return obj.comments.count()

    def comments_html(self, obj):
        comments = obj.comments.all()
        return mark_safe("<br>".join([c.message for c in comments]))

    actions = ['mark_completed', 'mark_canceled', 'reset_reopened', 'add_comment']

    def mark_completed(self, request, queryset):
        queryset.update(status=TaskStatus.COMPLETED)

    def mark_canceled(self, request, queryset):
        queryset.update(status=TaskStatus.CANCELED)

    def reset_reopened(self, request, queryset):
        queryset.update(is_reopened=False)

    def add_comment(self, request, queryset):
        for task in queryset:
            Comments.objects.create(
                task=task,
                message="Processed by admin"
            )
        self.message_user(request, "Комментарии добавлены", messages.SUCCESS)

    #ограничение
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assignee__owner=request.user)


#регистрация коммент
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('message', 'task', 'user')



@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "preview")

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "-"