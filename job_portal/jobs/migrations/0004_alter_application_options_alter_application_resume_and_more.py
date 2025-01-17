# Generated by Django 5.1.3 on 2024-11-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_remove_job_benefits_remove_job_employment_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'ordering': ['-applied_date'], 'verbose_name': 'Application', 'verbose_name_plural': 'Applications'},
        ),
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.FileField(blank=True, help_text='Uploaded resume for this specific application. Leave blank to use the default resume.', null=True, upload_to='application_resumes/'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('reviewed', 'Reviewed'), ('interviewed', 'Interviewed'), ('offered', 'Offered'), ('hired', 'Hired'), ('rejected', 'Rejected')], default='applied', help_text='Current status of the application', max_length=20),
        ),
    ]
