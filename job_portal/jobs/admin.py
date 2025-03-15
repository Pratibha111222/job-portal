from django.contrib import admin
from .models import Employer, JobSeeker, Job, Application, Message, Subscription


# Employer Admin
from django.contrib import admin
from .models import Employer
from django.contrib import admin
from .models import Employer

# Optional: Customize the Admin Interface
class EmployerAdmin(admin.ModelAdmin):
    # Define the fields you want to display in the list view of the admin page
    list_display = ('user', 'name', 'job_title', 'department', 'company', 'experience')
    
    # Add filters for easier navigation
    list_filter = ('gender', 'department', 'company')
    
    # Add search functionality
    search_fields = ('name', 'user__username', 'job_title', 'company')
    
    # Group fields in the detail view for better organization
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'dob', 'gender', 'phone_number', 'email')
        }),
        ('Professional Details', {
            'fields': ('job_title', 'department', 'skills', 'experience', 'bio')
        }),
        ('Company Information', {
            'fields': ('company', 'company_logo')
        }),
        ('Media', {
            'fields': ('profile_picture',)
        }),
    )

# Register the Employer model with the custom admin class
admin.site.register(Employer, EmployerAdmin)


# JobSeeker Admin
@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'location', 'phone_number', 'is_premium')
    search_fields = ('first_name', 'last_name', 'user__username', 'location', 'skills')
    list_filter = ('location', 'is_premium')
    readonly_fields = ('is_premium',)


# Job Admin
from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'job_mode', 'location', 'industry', 'status', 'vacancies', 'deadline')
    list_filter = ('industry', 'job_type', 'job_mode', 'status')
    search_fields = ('title', 'company__company_name', 'location')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Job Details", {
            'fields': ('title', 'company', 'description', 'industry', 'location', 'job_type', 'job_mode', 'deadline', 'status')
        }),
        ("Salary & Experience", {
            'fields': ('min_salary', 'max_salary', 'min_experience', 'max_experience')
        }),
        ("Vacancies", {
            'fields': ('vacancies',)
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    actions = ['mark_as_closed', 'mark_as_active']

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, "Selected jobs have been marked as closed.")
    mark_as_closed.short_description = "Mark selected jobs as Closed"

    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, "Selected jobs have been marked as active.")
    mark_as_active.short_description = "Mark selected jobs as Active"



# Application Admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'status', 'applied_date', 'resume')
    search_fields = ('job__title', 'job_seeker__user__username', 'status')
    list_filter = ('status', 'applied_date', 'job__industry')
    ordering = ('-applied_date',)
    fields = ('job', 'job_seeker', 'status', 'applied_date', 'resume')


# Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'application', 'content', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'content', 'application__job__title')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)


# Subscription Admin
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active', 'created_at', 'expires_at')
    search_fields = ('user__username', 'plan')
    list_filter = ('is_active', 'plan', 'created_at')
    ordering = ('-created_at',)
    fields = ('user', 'plan', 'subscription_id', 'is_active', 'created_at', 'expires_at')
    readonly_fields = ('created_at',)

 
 
