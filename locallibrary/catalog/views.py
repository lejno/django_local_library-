from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_books_genre = Genre.objects.count()  # Example of counting genres
    # count books with 'the' in the title (case-insensitive)
    num_books_containing_of = Book.objects.filter(title__icontains='of').count()
    

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_genre': num_books_genre,
        'num_books_containing_of': num_books_containing_of,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)