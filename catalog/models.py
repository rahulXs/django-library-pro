from django.db import models
from django.urls import reverse

import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length = 20, help_text = 'Enter book genre (ex. Fiction)')

    def __str__(self):
        return self.name 

class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)
    summary = models.TextField(max_length = 1000, help_text = "Enter description of book")
    # International Standard Book Number. This 10 or 13-digit number.
    isbn = models.CharField('ISBN', max_length = 13, unique = True, help_text = '10 or 13 digit Number')

    genre = models.ManyToManyField(Genre, help_text = 'Select genre of book')
    language = models.ForeignKey('Language', on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"

class BookInstance(models.Model):
    #Universally unique identifiers are a good alternative to AutoField for primary_key. The database will not generate the UUID for you,
    #so it is recommended to use default"
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text = "Unique ID of this particular book across library")

    due_back = models.DateField(null = True, blank = True)
    book = models.ForeignKey('Book', on_delete = models.RESTRICT, null = True)
    imprint = models.CharField(max_length = 20)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length = 1, choices = LOAN_STATUS, blank = True, default = 'm', help_text = "Book availability status")

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField(null = True, blank = True)
    #books = models.ForeignKey(Book, on_delete = models.SET_NULL)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

class Language(models.Model):
    name = models.CharField(max_length = 20, help_text = "Enter language of book")

    def __str__(self):
        return self.name

