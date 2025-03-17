from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid
from datetime import date
from django.conf import settings  # Required to assign User as a borrower

class Genre(models.Model):
    """Model representing a book genre (e.g., Science Fiction, Non-Fiction)."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g., Science Fiction, French Poetry, etc.)"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique'
            ),
        ]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])


class Language(models.Model):
    """Model representing a Language (e.g., English, French, Japanese)."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the book's natural language (e.g., English, French, Japanese, etc.)"
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique'
            ),
        ]
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])


class Book(models.Model):
    """Model representing a book (but not a specific copy)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        """Returns the URL to access a particular book record."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Creates a string representation of genres (limited to 3 for admin display)."""
        genres = self.genre.all()
        return ', '.join(genre.name for genre in genres[:3]) + ('...' if genres.count() > 3 else '')

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (for borrowing)."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book instance across the whole library"
    )
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    LOAN_STATUS = [
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    ]
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['due_back']
        permissions = [("can_mark_returned", "Set book as returned")]
        verbose_name = "Book Instance"
        verbose_name_plural = "Book Instances"

    def __str__(self):
        return f'{self.book.title} ({self.id}) - {self.get_status_display()}'

    def get_absolute_url(self):
        """Returns the URL to access a particular book instance."""
        return reverse('bookinstance-detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        """Determines if the book is overdue."""
        return self.due_back and date.today() > self.due_back
