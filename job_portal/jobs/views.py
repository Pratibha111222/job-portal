
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import JobSeeker, Employer, Application, Job, Message, Subscription
from .forms import JobSeekerProfileForm, EmployerProfileForm, JobForm, UsernameVerificationForm, PasswordResetForm
import razorpay
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
 
def index(request):
    
    if request.user.is_authenticated:
        
        try:
            job_seeker = request.user.jobseeker
            return redirect('job_seeker_dashboard') 
        except JobSeeker.DoesNotExist:
            
            try:
                employer = request.user.employer
                return redirect('employer_dashboard')  
            except Employer.DoesNotExist:
                pass  
   
    search_query = request.GET.get('search')
    if search_query:
        return redirect('jobseeker_login')  

    
    return render(request, 'index.html', {'search_query': search_query})




def job_seeker_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if password != confirm_password:
            return render(request, 'job_seeker_signup.html', {
                'error_message': "Passwords do not match!",
            })

        
        if User.objects.filter(username=username).exists():
            return render(request, 'job_seeker_signup.html', {
                'error_message': "Username already exists!",
            })

        
        user = User.objects.create_user(username=username, password=password)
        user.save()

        
        JobSeeker.objects.create(user=user)

       
        return redirect('jobseeker_login')  

    return render(request, 'job_seeker_signup.html')

def jobseeker_login(request):
    error_message = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            if hasattr(user, 'jobseeker'): 
                login(request, user)
                return redirect('job_seeker_dashboard')
            else:
                
                error_message = "This login page is for Job Seekers only."
        else:
            error_message = "Invalid credentials, please try again."

    return render(request, 'job_seeker_login.html', {'message': error_message})



def job_seeker_password_reset(request):
    if request.method == 'POST':
        form = UsernameVerificationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            
            if User.objects.filter(username=username).exists():
                
                request.session['username'] = username  
                return redirect('job_seeker_reset_password')
            else:
                messages.error(request, "Username not found.")
                return redirect('job_seeker_password_reset')
    else:
        form = UsernameVerificationForm()

    return render(request, 'job_seeker_password_reset_verify.html', {'form': form})

def job_seeker_reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

           
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('job_seeker_reset_password')

           
            username = request.session.get('username')
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  
            messages.success(request, "Password reset successful.")
            return redirect('jobseeker_login')
    else:
        form = PasswordResetForm()

    return render(request, 'job_seeker_password_reset_form.html', {'form': form})


def employer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if password != confirm_password:
            return render(request, 'employer_signup.html', {
                'error_message': "Passwords do not match!",
            })

        
        if User.objects.filter(username=username).exists():
            return render(request, 'employer_signup.html', {
                'error_message': "Username already exists!",
            })

       
        user = User.objects.create_user(username=username, password=password)
        user.save()

        
        Employer.objects.create(user=user)

        
        login(request, user)

       
        return redirect('employer_login')  
    return render(request, 'employer_signup.html')




def employer_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            if hasattr(user, 'employer'):
                login(request, user)
                return redirect('employer_dashboard')  
            else:
                error_message = "This login page is for Employers only."
        else:
            error_message = "Invalid credentials, please try again."

    return render(request, 'employer_login.html', {'message': error_message})




def employer_password_reset(request):
    if request.method == 'POST':
        form = UsernameVerificationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            
            if User.objects.filter(username=username).exists():
                
                request.session['username'] = username  
                return redirect('employer_reset_password')
            else:
                messages.error(request, "Username not found.")
                return redirect('employer_password_reset')
    else:
        form = UsernameVerificationForm()

    return render(request, 'employer_password_reset_verify.html', {'form': form})


def employer_reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect('employer_reset_password')

            
            username = request.session.get('username')
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)   
            messages.success(request, "Password reset successful.")
            return redirect('employer_login')
    else:
        form = PasswordResetForm()

    return render(request, 'employer_password_reset_form.html', {'form': form})


@login_required(login_url='/login/')
def job_seeker_dashboard(request):
   
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, "Access denied. Only Job Seekers can view this page.")
        return redirect('jobseeker_login')

    job_seeker = request.user.jobseeker

    
    search_query = request.GET.get('search', '')
    industry_filter = request.GET.get('industry', '')
    job_mode_filter = request.GET.get('job_mode', '') 
    min_experience_filter = request.GET.get('min_experience', '')
    max_experience_filter = request.GET.get('max_experience', '')
    min_salary_filter = request.GET.get('min_salary', '')
    max_salary_filter = request.GET.get('max_salary', '') 

   
    filters_applied = any([search_query, industry_filter, job_mode_filter, min_experience_filter, max_experience_filter, min_salary_filter, max_salary_filter])

   
    all_jobs = Job.objects.filter(status='active')

    
    if search_query:
        all_jobs = all_jobs.filter(
            Q(title__icontains=search_query) | Q(location__icontains=search_query)
        )

    
    if industry_filter:
        all_jobs = all_jobs.filter(industry=industry_filter)

    
    if job_mode_filter:
        all_jobs = all_jobs.filter(job_mode=job_mode_filter)

    
    if min_experience_filter.isdigit():
        all_jobs = all_jobs.filter(min_experience__gte=int(min_experience_filter))

    if max_experience_filter.isdigit():
        all_jobs = all_jobs.filter(max_experience__lte=int(max_experience_filter))

    
    if min_salary_filter.isdigit():
        all_jobs = all_jobs.filter(min_salary__gte=int(min_salary_filter))

    if max_salary_filter.isdigit():
        all_jobs = all_jobs.filter(max_salary__lte=int(max_salary_filter))

    
    applied_jobs = Application.objects.filter(job_seeker=job_seeker).values_list('job_id', flat=True)
    available_jobs = all_jobs.exclude(id__in=applied_jobs)


    industry_choices = Job._meta.get_field('industry').choices
    job_mode_choices = Job._meta.get_field('job_mode').choices
    user_applications = Application.objects.filter(job_seeker=job_seeker).select_related('job')
    has_premium_subscription = Subscription.objects.filter(user__username=request.user.username).exists()

   
    return render(request, 'job_seeker_dashboard.html', {
        'job_seeker': job_seeker,
        'jobs': available_jobs,
        'applied_jobs': user_applications,
        'industry_choices': [choice[0] for choice in industry_choices],
        'job_mode_choices': [choice[0] for choice in job_mode_choices],
        'search_query': search_query,
        'industry_filter': industry_filter,
        'job_mode_filter': job_mode_filter,
        'min_experience_filter': min_experience_filter,
        'max_experience_filter': max_experience_filter,
        'salary_filter': min_salary_filter,
        'has_premium_subscription': has_premium_subscription,
        'filters_applied': filters_applied,  
    })


class JobSeekerProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        job_seeker, created = JobSeeker.objects.get_or_create(user=request.user)

       
        if created or not job_seeker.first_name or not job_seeker.skills:
            form = JobSeekerProfileForm(instance=job_seeker)
            return render(request, 'job_seeker_profile_form.html', {'form': form})

        
        return render(request, 'job_seeker_profile_detail.html', {'job_seeker': job_seeker})

    def post(self, request):
        job_seeker, created = JobSeeker.objects.get_or_create(user=request.user)
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker)

        if form.is_valid():
            form.save()
            return redirect('job_seeker_dashboard')  
        return render(request, 'job_seeker_profile_form.html', {'form': form})


class JobSeekerProfileEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        job_seeker = request.user.jobseeker
        form = JobSeekerProfileForm(instance=job_seeker)
        return render(request, 'job_seeker_profile_form.html', {'form': form})

    def post(self, request):
        job_seeker = request.user.jobseeker
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker)
        if form.is_valid():
            form.save()
            return redirect('job_seeker_dashboard') 
        return render(request, 'job_seeker_profile_form.html', {'form': form})

 

def custom_logout(request):
    logout(request)
    return redirect('index')

def company_detail(request, company_id):
   
    company = get_object_or_404(Employer, id=company_id)
   
    jobs = Job.objects.filter(company=company)

    return render(request, 'company_detail.html', {'company': company, 'jobs': jobs})




@login_required(login_url='/login/') 
def employer_dashboard(request):
    try:
        
        employer = request.user.employer

       
        jobs = Job.objects.filter(company=employer, status='active').order_by('-created_at')[:3]

        
        total_jobs = Job.objects.filter(company=employer).count()

       
        pending_applications = Application.objects.filter(job__in=jobs, status='applied').count()

        

    except Employer.DoesNotExist:
        
        jobs = []
        total_jobs = 0
        pending_applications = 0

    return render(request, 'employer_dashboard.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'pending_applications': pending_applications,
    })

 
class EmployerProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        employer, created = Employer.objects.get_or_create(user=request.user)

        
        if created or not all([
            employer.company_name,
            employer.location,
            employer.industry,
            employer.bio,
            employer.contact_email,
            employer.contact_phone,
            employer.company_address  
        ]):
            form = EmployerProfileForm(instance=employer)
            return render(request, 'employer_profile_form.html', {'form': form})

       
        return render(request, 'employer_profile_detail.html', {'employer': employer})

    def post(self, request):
        employer, created = Employer.objects.get_or_create(user=request.user)
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)

        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')  
        return render(request, 'employer_profile_form.html', {'form': form})


class EmployerProfileEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        employer = request.user.employer
        form = EmployerProfileForm(instance=employer)
        return render(request, 'employer_profile_form.html', {'form': form})

    def post(self, request):
        employer = request.user.employer
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)

        if form.is_valid():
            form.save()
            return redirect('employer_profile')  

        return render(request, 'employer_profile_form.html', {'form': form})
 

@login_required
def edit_company_profile(request):
    employer = request.user.employer
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=employer)
    
    return render(request, 'edit_company_profile.html', {'form': form})


@login_required(login_url='/login/')
def applied_jobs_view(request):
    try:
        
        job_seeker = request.user.jobseeker
    except AttributeError:
        
        return render(request, 'error.html', {'message': 'You must be a Job Seeker to view applied jobs.'})

    
    applied_jobs = Application.objects.filter(job_seeker=job_seeker).select_related('job')

    return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})
 

@login_required(login_url='/login/')
def post_job(request):
    
    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        messages.error(request, "Employer profile does not exist. Please complete your profile.")
        return redirect('employer_profile_create')  
    required_fields = [
        employer.company_name,
        employer.location,
        employer.industry,
        employer.contact_email,
    ]
    if not all(required_fields):
        messages.error(request, "Please complete your company profile before posting a job.")
        return redirect('employer_profile_edit')  
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = employer
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('jobs_posted')
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})
 


@login_required(login_url='/login/')
def apply_job(request, job_id):
   
    job = get_object_or_404(Job, id=job_id)

   
    try:
        job_seeker = request.user.jobseeker
    except JobSeeker.DoesNotExist:
        messages.error(request, "You must be a Job Seeker to apply for jobs.")
        return redirect('job_seeker_dashboard')

    
    required_fields = ['first_name', 'last_name', 'resume', 'skills', 'phone_number']
    incomplete_fields = [field for field in required_fields if not getattr(job_seeker, field)]

    if incomplete_fields:
        messages.error(
            request,
            "Your profile is incomplete. Please update your profile to apply for jobs."
        )
        return redirect('job_seeker_profile_edit')
 
   
    if Application.objects.filter(job=job, job_seeker=job_seeker).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_seeker_dashboard')

    
    if request.method == 'POST':
        Application.objects.create(job=job, job_seeker=job_seeker, status='applied')
        messages.success(request, "You have successfully applied for the job.")
        return redirect('job_seeker_dashboard')

    
    return render(request, 'apply_job.html', {'job': job})


@login_required(login_url='/login/')
def jobs_posted(request):
    employer = request.user.employer
    jobs = Job.objects.filter(company=employer)

    return render(request, 'jobs_posted.html', {'jobs': jobs})

 

def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
           
            messages.success(request, 'Job post updated successfully!')
           
            return render(request, 'edit_job.html', {'form': form, 'job': job})

    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})

 
 

def view_applications(request, job_id):
    job = Job.objects.get(id=job_id)
    applications = Application.objects.filter(job=job)
    status_choices = Application._meta.get_field('status').choices

    context = {
        'job': job,
        'applications': applications,
        'status_choices': status_choices,  
    }
    return render(request, 'view_applications.html', context)

def update_application_status(request, application_id):
    if request.method == 'POST':
        application = Application.objects.get(id=application_id)
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):  
            application.status = new_status
            application.save()
        return redirect('view_applications', job_id=application.job.id)


def applied_job_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    job = application.job
    has_premium_subscription = Subscription.objects.filter(user__username=request.user.username).exists()

    context = {
        'job': job,
        'application': application,
        "has_premium_subscription": has_premium_subscription,
    }
    return render(request, 'applied_job_detail.html', context)

class AppliedJobsView(View):
    def get(self, request):
        applied_jobs = Application.objects.filter(job_seeker=request.user.jobseeker)
        return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})


def job_seeker_details(request, job_seeker_id):
    job_seeker = get_object_or_404(JobSeeker, id=job_seeker_id)
    applications = Application.objects.filter(job_seeker=job_seeker)
    
    job_id = applications.first().job.id if applications else None
    return render(request, 'job_seeker_details.html', {
        'job_seeker': job_seeker,
        'job_id': job_id,  
    })

def close_job(request, job_id):
    
    job = get_object_or_404(Job, id=job_id)

   
    if job.company.user == request.user:
        job.status = 'closed'  
        job.save()

   
    return redirect('employer_dashboard')
 
 
@login_required
def send_message(request, application_id):
    application = get_object_or_404(Application, id=application_id)

   
    if hasattr(request.user, 'employer') and application.job.company.user == request.user:
        receiver = application.job_seeker.user
    elif hasattr(request.user, 'jobseeker') and application.job_seeker.user == request.user:
        receiver = application.job.company.user
    else:
        return redirect('error_page')  
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('view_messages', application_id=application.id)
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'application': application})


@login_required
def chat_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

   
    if request.user != application.job_seeker.user and request.user != application.job.company.user:
        return HttpResponseForbidden("You are not authorized to view this chat.")

   
    messages = application.messages.order_by('timestamp')

    
    if request.method == 'POST':
        content = request.POST.get('content').strip()  
        if content:  
            Message.objects.create(
                sender=request.user,
                recipient=application.job_seeker.user if request.user == application.job.company.user else application.job.company.user,
                application=application,
                content=content,
            )

    context = {
        'application': application,
        'messages': messages,
    }
    return render(request, 'chat.html', context)


@login_required(login_url='/login/')
def employer_inbox(request):
    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        messages.error(request, "You must be an employer to access the inbox.")
        return redirect('index')

    messages_received = Message.objects.filter(receiver=request.user).select_related('sender', 'job')
    return render(request, 'employer_inbox.html', {'messages': messages_received})

@login_required
def view_messages(request, application_id):
    application = get_object_or_404(Application, id=application_id)

   
    if not (
        (hasattr(request.user, 'employer') and application.job.company.user == request.user) or
        (hasattr(request.user, 'jobseeker') and application.job_seeker.user == request.user)
    ):
        return redirect('error_page')

   
    messages = Message.objects.filter(
        sender__in=[application.job.company.user, application.job_seeker.user],
        receiver__in=[application.job.company.user, application.job_seeker.user]
    ).order_by('timestamp')

    form = MessageForm()

    return render(request, 'view_messages.html', {
        'messages': messages,
        'application': application,
        'form': form,
    })



razorpay_client = razorpay.Client(auth=("rzp_test_wH0ggQnd7iT3nB", "eZseshY3oSsz2fcHZkTiSlCm"))
@login_required
def create_payment(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        if plan != 'premium':
            return redirect('subscriptionpage')  
        order_data = {
            'amount': 99900,  
            'currency': 'INR',
            'payment_capture': '1',
        }
        order = razorpay_client.order.create(data=order_data)

       
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        subscription.plan = 'premium'
        subscription.subscription_id = order['id']
        subscription.is_active = False  
        subscription.save()

       
        try:
            job_seeker = request.user.jobseeker  
        except JobSeeker.DoesNotExist:
            job_seeker = None  
       
        context = {
            'order_id': order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': 999,
            'name': request.user.username,
            'email': request.user.email,
            'contact': job_seeker.phone_number if job_seeker else '' 
        }
        return render(request, 'payment_page.html', context)

    return redirect('subscriptionpage') 

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })

           
            subscription = Subscription.objects.get(subscription_id=razorpay_order_id)
            subscription.is_active = True
            subscription.expires_at = now() + timedelta(days=30)
            subscription.save()

            
            if request.user.is_authenticated:
                try:
                    job_seeker = JobSeeker.objects.get(user=request.user)
                    print(f"Updating is_premium for user {job_seeker.user.username}")
                    job_seeker.is_premium = True
                    job_seeker.save()
                    job_seeker.refresh_from_db()  
                    print(f"is_premium updated: {job_seeker.is_premium}")
                except JobSeeker.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'JobSeeker profile does not exist'})
            else:
                return JsonResponse({'status': 'error', 'message': 'User not authenticated'})

            return JsonResponse({'status': 'success'})
        except razorpay.errors.SignatureVerificationError as e:
            print(f"Signature verification error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Signature verification failed'})



def subscriptionpage(request):
    """
    View to render the Buy Subscription page.
    """
    
    has_premium_subscription = Subscription.objects.filter(user__username=request.user.username).exists()

    
    subscription_plans = [
        {
            "name": "Basic",
            "price": "Free",
            "features": ["Basic Job Search", "Apply to 5 jobs per month", "Limited Support"],
            "cta": "Select Free Mode",
        },
        {
            "name": "Premium",
            "price": "₹999/month",
            "features": ["Unlimited Job Applications", "Priority Support", "Access Exclusive Jobs"],
            "cta": "Buy Subscription",
        },
    ]

   
    return render(request, 'subscriptionpage.html', {
        "plans": subscription_plans,
        "has_premium_subscription": has_premium_subscription,
    })
