# Generated by Django 5.1.3 on 2024-11-15 08:58

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_jobseeker_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='benefits',
        ),
        migrations.RemoveField(
            model_name='job',
            name='employment_type',
        ),
        migrations.RemoveField(
            model_name='job',
            name='experience_required',
        ),
        migrations.RemoveField(
            model_name='job',
            name='posted_date',
        ),
        migrations.RemoveField(
            model_name='job',
            name='qualifications',
        ),
        migrations.RemoveField(
            model_name='job',
            name='responsibilities',
        ),
        migrations.RemoveField(
            model_name='job',
            name='skills_required',
        ),
        migrations.AddField(
            model_name='employer',
            name='company_address',
            field=models.CharField(blank=True, help_text="Company's physical address", max_length=500),
        ),
        migrations.AddField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='job',
            name='experience_level',
            field=models.CharField(choices=[('Junior', 'Junior'), ('Mid', 'Mid-level'), ('Senior', 'Senior')], default='Junior', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='industry',
            field=models.CharField(choices=[('Information Technology', 'Information Technology'), ('Healthcare', 'Healthcare'), ('Finance', 'Finance')], default='Finance', max_length=100),
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract')], default='Fresher', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.employer'),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
