# Generated by Django 2.2.8 on 2020-01-03 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='First name.', max_length=20)),
                ('middle_name', models.CharField(help_text='Middle name, space-separated if more than one.', max_length=20, null=True)),
                ('last_name', models.CharField(help_text='Last name.', max_length=20)),
                ('birth_place', models.CharField(help_text='Place of birth, generally a city.', max_length=20, null=True)),
                ('birth_date', models.DateField(help_text='Birth date.', null=True)),
                ('birth_date_is_approximative', models.BooleanField(default=False, help_text='Boolean indicating uncertainty around the birth date.')),
                ('death_place', models.CharField(help_text='Place of death, generally a city.', max_length=20, null=True)),
                ('death_date', models.DateField(help_text='Death date.', null=True)),
                ('death_date_is_approximative', models.BooleanField(default=False, help_text='Boolean indicating uncertainty around the death date.')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], help_text="Person's gender.", max_length=1, null=True)),
                ('comments', models.TextField(help_text='Freeform comments.', null=True)),
                ('parent', models.ManyToManyField(help_text='ID of the parent in the Persons table.', related_name='children', to='tree.Person')),
            ],
        ),
    ]
