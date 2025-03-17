# Generated by Django 4.2.18 on 2025-03-03 06:54

from django.db import migrations, models
import django.db.models.functions.text
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Author', 'verbose_name_plural': 'Authors'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'author'], 'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': [('can_mark_returned', 'Set book as returned')], 'verbose_name': 'Book Instance', 'verbose_name_plural': 'Book Instances'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Genre', 'verbose_name_plural': 'Genres'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'Language', 'verbose_name_plural': 'Languages'},
        ),
        migrations.RemoveConstraint(
            model_name='genre',
            name='genre_name_case_insensitive_unique',
        ),
        migrations.RemoveConstraint(
            model_name='language',
            name='language_name_case_insensitive_unique',
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='Died'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book instance across the whole library', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Enter a book genre (e.g., Science Fiction, French Poetry, etc.)', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text="Enter the book's natural language (e.g., English, French, Japanese, etc.)", max_length=200, unique=True),
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique'),
        ),
        migrations.AddConstraint(
            model_name='language',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='language_name_case_insensitive_unique'),
        ),
    ]
