import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.models import Book, Author, BookInstance
from catalog.forms import RenewBookForm


# 🔹 Home Page View
def index(request):
    """View function for the home page of the site."""
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status="a").count()
    num_authors = Author.objects.count()

    # Track visits using session
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context)


# 🔹 Book List View (Paginated)
class BookListView(generic.ListView):
    """Displays a paginated list of books."""
    model = Book
    context_object_name = "book_list"
    template_name = "catalog/book_list.html"
    paginate_by = 5

    def get_queryset(self):
        """Optimized query to fetch books along with their authors."""
        return Book.objects.select_related("author")


# 🔹 Author List View (Paginated)
class AuthorListView(generic.ListView):
    """Displays a paginated list of authors."""
    model = Author
    context_object_name = "author_list"
    template_name = "catalog/author_list.html"
    paginate_by = 10

    def get_queryset(self):
        """Optimized query to fetch authors along with their books."""
        return Author.objects.prefetch_related("book_set")


# 🔹 Book Detail View
class BookDetailView(generic.DetailView):
    """Displays details of a specific book."""
    model = Book
    template_name = "catalog/book_detail.html"

    def get_queryset(self):
        """Optimize query to fetch book along with related instances."""
        return Book.objects.select_related("author").prefetch_related("bookinstance_set")


# 🔹 Books Borrowed by Logged-in User
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Lists books currently borrowed by the logged-in user."""
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        """Filter borrowed books for the logged-in user."""
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status="o",
        ).order_by("due_back")


# 🔹 Renew Book View (Function-Based)
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()
            return HttpResponseRedirect(reverse("all-borrowed"))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={"due_back": proposed_renewal_date})

    return render(
        request, "catalog/book_renew_librarian.html", {"form": form, "book_instance": book_instance}
    )


# 🔹 Author Create View
class AuthorCreate(PermissionRequiredMixin, CreateView):
    """Allows users with permission to add a new author."""
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'


# 🔹 Author Update View
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    """Allows users with permission to edit an existing author."""
    model = Author
    fields = '__all__'  # Not recommended in real-world apps for security
    permission_required = 'catalog.change_author'


# 🔹 Author Delete View
class AuthorDelete(PermissionRequiredMixin, DeleteView):
    """Allows users with permission to delete an author."""
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        """Handles deletion errors gracefully."""
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception:
            return HttpResponseRedirect(reverse("author-delete", kwargs={"pk": self.object.pk}))
