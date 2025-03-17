from django.urls import path
from catalog import views

urlpatterns = [
    # 🔹 Home Page
    path("", views.index, name="index"),  

    # 🔹 Book URLs
    path("books/", views.BookListView.as_view(), name="books"),  
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),  

    # 🔹 Author URLs
    path("authors/", views.AuthorListView.as_view(), name="authors"),  

    # 🔹 Borrowed Books (Only for Logged-in Users)
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),  

    # 🔹 Book Renewal (Only for Librarians/Admins)
    path("book/<int:pk>/renew/", views.renew_book_librarian, name="renew-book"),  

    # 🔹 Author Management URLs (Create, Update, Delete)
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
