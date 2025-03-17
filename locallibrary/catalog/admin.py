from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

class BooksInline(admin.TabularInline):  
    """Allows books to be added directly inside the Author page."""
    model = Book
    extra = 1  # Shows one empty row for adding a new book
    fields = ('title', 'language')  # Limits fields displayed

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    search_fields = ('last_name', 'first_name')
    ordering = ('last_name',)
    list_filter = ('date_of_birth',)  # Allows filtering by birth year
    inlines = [BooksInline]  # Allows adding books directly inside an author’s profile

class BookInstancesInline(admin.TabularInline):
    """Allows book instances to be added inside the Book page."""
    model = BookInstance
    extra = 1
    fields = ('status', 'due_back', 'borrower')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('author', 'genre', 'language')  # Added language filter
    search_fields = ('title', 'author__last_name')
    inlines = [BookInstancesInline]  # Allows adding book copies inside the Book page

    def display_genre(self, obj):
        """Displays up to 3 genres with '...' if there are more."""
        genres = obj.genre.all()
        return ', '.join(genre.name for genre in genres[:3]) + ('...' if genres.count() > 3 else '')

    display_genre.short_description = 'Genre'

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status_colored', 'due_back', 'borrower')
    list_filter = ('status', 'due_back')
    search_fields = ('book__title', 'borrower__username')
    ordering = ('due_back',)

    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back', 'borrower')}),
    )

    def status_colored(self, obj):
        """Color codes status for better readability."""
        status_colors = {
            'o': '🔴 On Loan',
            'a': '🟢 Available',
            'r': '🟡 Reserved',
            'd': '⚪ Maintenance'
        }
        return status_colors.get(obj.status, obj.status)

    status_colored.admin_order_field = 'status'
    status_colored.short_description = 'Status'

admin.site.register(Genre)
admin.site.register(Language)
