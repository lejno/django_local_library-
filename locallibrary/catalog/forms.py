import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Book, Author, Language


class BookForm(forms.ModelForm):
    # Allow typing a new author name (simple format: "First Last" or "Last, First")
    author_name = forms.CharField(
        required=False,
        label="Author (type to create)",
        help_text='Type a new author name ("First Last" or "Last, First") if the author is not in the list.'
    )
    # Allow typing a new language name
    language_name = forms.CharField(
        required=False,
        label="Language (type to create)",
        help_text='Type a new language name if the language is not in the list.'
    )

    class Meta:
        model = Book
        # keep author in the form so users can also select existing ones
        fields = ['title', 'author', 'author_name', 'summary', 'isbn', 'genre', 'language', 'language_name']

    def clean(self):
        cleaned = super().clean()
        author = cleaned.get('author')
        name = cleaned.get('author_name')
        language = cleaned.get('language')
        language_name = cleaned.get('language_name')

        # If an existing author wasn't selected but a name was provided, create/get the Author
        if not author and name:
            # Accept either "Last, First" or "First Last" formats
            if ',' in name:
                last, first = [p.strip() for p in name.split(',', 1)]
            else:
                parts = name.split()
                if len(parts) == 1:
                    first = parts[0]
                    last = ''
                else:
                    first = parts[0]
                    last = ' '.join(parts[1:])

            author_obj, created = Author.objects.get_or_create(first_name=first, last_name=last)
            cleaned['author'] = author_obj

        # If an existing language wasn't selected but a name was provided, create/get the Language
        if not language and language_name:
            lang_obj, created = Language.objects.get_or_create(name=language_name.strip())
            cleaned['language'] = lang_obj

        return cleaned


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data