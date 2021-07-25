from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # all() implied by default
    num_authors = Author.objects.count()
    num_languages = Language.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_languages': num_languages,
    }

    return render(request, 'catalog/index.html', context = context)