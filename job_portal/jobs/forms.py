from django import forms
from .models import JobSeeker, Job, Employer

# JobSeeker Profile Form
class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = [
            'first_name', 'last_name', 'resume', 'profile_picture', 
            'skills', 'experience', 'education', 'phone_number', 
            'location', 'linkedin_url', 'portfolio_url', 'summary', 
            'certifications', 'languages',
        ]
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 2}),
            'certifications': forms.Textarea(attrs={'rows': 2}),
        }

# Job Form
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'location',
            'industry',
            'min_salary',
            'max_salary',
            'min_experience',
            'max_experience',
            'job_type',
            'job_mode',
            'deadline',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
from django import forms
from .models import Employer

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = [
            'name', 
            'dob', 
            'gender', 
            'experience', 
            'skills', 
            'job_title', 
            'department', 
            'phone_number', 
            'email', 
            'profile_picture', 
            'company', 
            'bio',
            'company_logo', 
            
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and (len(phone_number) < 10 or len(phone_number) > 15):
            raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phone_number

    
from django import forms
from .models import Message

from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Type your message...',
                'rows': 4,
            }),
        }
class UsernameVerificationForm(forms.Form):
    username = forms.CharField(max_length=150)

# Form to reset the password
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

from django import forms

# Form to verify username
class UsernameVerificationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))

# Form for resetting the password
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}), required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
