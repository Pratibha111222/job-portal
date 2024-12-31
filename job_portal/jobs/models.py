from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=100, help_text="City, Country")
    industry = models.CharField(max_length=100, help_text="e.g., Information Technology, Healthcare")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    company_address = models.CharField(max_length=500, blank=True, help_text="Company's physical address")

    def __str__(self):
        return self.company_name
    @property
    def is_employer(self):
        return hasattr(self, 'employer') 


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    resume = models.FileField(upload_to='resumes/')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    skills = models.TextField(help_text="List skills separated by commas.")
    experience = models.CharField(max_length=500, null=True, blank=True)
    education = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, help_text="City, Country")
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, help_text="A brief professional summary or bio.")
    certifications = models.TextField(blank=True, help_text="Certifications separated by commas.")
    languages = models.CharField(max_length=200, blank=True, help_text="Languages spoken, separated by commas.")
    is_premium = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

   


 
from django.db import models
from django.utils.timezone import now

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
    ]

    INDUSTRY_CHOICES = [
        ('Information Technology', 'Information Technology'),
        ('Healthcare', 'Healthcare'),
        ('Finance', 'Finance'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    JOB_MODE_CHOICES = [
        ('Remote', 'Remote'),
        ('Work from Office', 'Work from Office'),
        ('Hybrid', 'Hybrid'),
    ]

    company = models.ForeignKey('Employer', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=30, choices=INDUSTRY_CHOICES, default='Finance')
    
    # Salary range
    min_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, 
        help_text="Minimum salary for this job (optional)."
    )
    max_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, 
        help_text="Maximum salary for this job (optional)."
    )
    
   
    min_experience = models.PositiveIntegerField(
        default=0, 
        help_text="Minimum years of experience required for this job."
    )
    max_experience = models.PositiveIntegerField(
        null=True, blank=True, 
        help_text="Maximum years of experience required for this job (optional)."
    )

    
    vacancies = models.PositiveIntegerField(
        default=1, 
        help_text="Number of openings available for this job."
    )

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full-time')
    job_mode = models.CharField(max_length=20, choices=JOB_MODE_CHOICES, default='Work from Office')
    deadline = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Indicates whether the job is active or closed."
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

    def close_job(self):
        """Mark the job as closed."""
        self.status = 'closed'
        self.save()

    def activate_job(self):
        """Reopen the job if it was previously closed."""
        self.status = 'active'
        self.save()

    @property
    def is_active(self):
        """Check if the job is active."""
        return self.status == 'active'

    def get_salary_range(self):
        """Return the salary range as a string."""
        if self.min_salary and self.max_salary:
            return f"${self.min_salary} - ${self.max_salary}"
        elif self.min_salary:
            return f"Starting at ${self.min_salary}"
        elif self.max_salary:
            return f"Up to ${self.max_salary}"
        else:
            return "Not specified"

    def get_experience_range(self):
        """Return the experience range as a string."""
        if self.min_experience and self.max_experience:
            return f"{self.min_experience} - {self.max_experience} years"
        elif self.min_experience:
            return f"{self.min_experience}+ years"
        else:
            return "No experience required"
    
    def decrease_vacancy(self):
        """Reduce the vacancy count by 1."""
        if self.vacancies > 0:
            self.vacancies -= 1
            self.save()

    def increase_vacancy(self):
        """Increase the vacancy count by 1."""
        self.vacancies += 1
        self.save()





class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview'),
        ('hire', 'Hire'),
        ('reject', 'Reject'),
    ]

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="applications")
    job_seeker = models.ForeignKey('JobSeeker', on_delete=models.CASCADE, related_name="applications")
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='applied',
        help_text="Current status of the application"
    )
    resume = models.FileField(
        upload_to='application_resumes/',
        blank=True,
        null=True,
        help_text="Uploaded resume for this specific application. Leave blank to use the default resume."
    )

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.job.title} - {self.job_seeker.user.username}"

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()
            return True
        return False

    @property
    def display_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='messages')  # This line is key
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"


 

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)  
    subscription_id = models.CharField(max_length=100, null=True, blank=True)  
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.username} - {self.plan}"
