from django.contrib import admin
from .models import Employer, JobSeeker, Job, Application, Message, Subscription


# Employer Admin
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'location', 'contact_email', 'contact_phone')
    search_fields = ('company_name', 'user__username', 'industry', 'location', 'contact_email')
    list_filter = ('industry', 'location')


# JobSeeker Admin
@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'location', 'phone_number', 'is_premium')
    search_fields = ('first_name', 'last_name', 'user__username', 'location', 'skills')
    list_filter = ('location', 'is_premium')
    readonly_fields = ('is_premium',)


# Job Admin
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'company', 'industry', 'location', 'job_type', 'job_mode',
        'min_salary', 'max_salary', 'min_experience', 'max_experience', 
        'vacancies', 'deadline', 'status', 'created_at'
    )
    search_fields = (
        'title', 'company__company_name', 'description', 'location', 'industry'
    )
    list_filter = ('job_type', 'job_mode', 'industry', 'location', 'status')
    ordering = ('-created_at',)
    fields = (
        'title', 'company', 'description', 'location', 'industry',
        'min_salary', 'max_salary', 'min_experience', 'max_experience',
        'vacancies', 'job_type', 'job_mode', 'deadline', 'status'
    )
    readonly_fields = ('created_at', 'updated_at')


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
