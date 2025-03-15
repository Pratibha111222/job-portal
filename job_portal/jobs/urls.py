from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Landing page or index
    path('jobseeker-login/', views.jobseeker_login, name='jobseeker_login'),  # Job Seeker login
    path('employer-login/', views.employer_login, name='employer_login'),  # Employer login
    path('jobseeker-signup/', views.job_seeker_signup, name='job_seeker_signup'),  # Job Seeker Sign-Up
    path('employer-signup/', views.employer_signup, name='employer_signup'),  # Employer Sign-Up
    
    # Job Seeker URLs
    path('job-seeker-dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),  # Job Seeker Dashboard
    path('jobseeker-profile/', views.JobSeekerProfileView.as_view(), name='job_seeker_profile'),  # Job Seeker Profile View
    path('jobseeker-profile-edit/', views.JobSeekerProfileEditView.as_view(), name='job_seeker_profile_edit'),  # Job Seeker Profile Edit
    path('job-seeker/password-reset/', views.job_seeker_password_reset, name='job_seeker_password_reset'),
    
    # Step 2: Reset the password
    path('job-seeker/password-reset/confirm/', views.job_seeker_reset_password, name='job_seeker_reset_password'),

    # Password reset for Employers
     path('employer/password_reset/', views.employer_password_reset, name='employer_password_reset'),
    path('employer/password_reset/confirm/', views.employer_reset_password, name='employer_reset_password'),
    # Employer URLs
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),  # Employer Dashboard
path('employer/profile/create/', views.EmployerProfileCreateView.as_view(), name='employer_profile_create'),
    path('employer/profile/update/', views.EmployerProfileUpdateView.as_view(), name='employer_profile_update'),
   path('edit-company-profile/', views.edit_company_profile, name='edit_company_profile'),  # Employer Profile Edit
    path('post-job/', views.post_job, name='post_job'),  # Post a job
    path('jobs-posted/', views.jobs_posted, name='jobs_posted'),
    path('employer-profile/', views.EmployerProfileView.as_view(), name='employer_profile'), 
     
    
    # Logout URL
    path('logout/', views.custom_logout, name='logout'),  # Logout

     path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
     path('applied-jobs/', views.applied_jobs_view, name='applied_jobs'),
     path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('job/edit/<int:job_id>/', views.edit_job, name='edit_job'),
     
     path('job/<int:job_id>/applicant/', views.view_applications, name='view_applications'),
    path('application/update/<int:application_id>/', views.update_application_status, name='update_application_status'),
     path('job/<int:job_id>/', views.job_detail, name='job_detail'),
     path('applied_jobs/', views.AppliedJobsView.as_view(), name='applied_jobs'),
      path('applied_job-detail/<int:application_id>/', views.applied_job_detail, name='applied_job_detail'),
       path('job-seeker/<int:job_seeker_id>/', views.job_seeker_details, name='job_seeker_details'),
       path('close-job/<int:job_id>/', views.close_job, name='close_job'),
        path('job/<int:job_id>/', views.job_detail, name='job_details'),
    path('job/<int:job_id>/send_message/', views.send_message, name='send_message'),
     path('application/<int:application_id>/send-message/', views.send_message, name='send_message'),
    path('application/<int:application_id>/view-messages/', views.view_messages, name='view_messages'),
    path('chat/<int:application_id>/', views.chat_view, name='chat'),
     
    path('subscriptionpage/', views.subscriptionpage, name='subscriptionpage'),
     path('create-payment/',views.create_payment, name='create_payment'),
    path('payment-success/',views.payment_success, name='payment_success'),
     
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


