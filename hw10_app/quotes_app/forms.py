from django.forms import CharField, TextInput, Textarea, ModelForm, ModelChoiceField, Select

from .models import Author, Quot


class AuthorForm(ModelForm):
    fullname = CharField(
        max_length=200,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}))

    born_date = CharField(
        max_length=120,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}))

    born_location = CharField(
        max_length=120, required=True,
        widget=TextInput(attrs={"class": "form-control"}))

    description = CharField(
        required=True,
        widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuotForm(ModelForm):
    author_choices = Author.objects.all()

    author = ModelChoiceField(
        label="Author",
        queryset=author_choices,
        to_field_name="fullname",
        empty_label="Choose an author below",
        required=True,
        widget=Select(attrs={"class": "form-control"})
    )
    quot = CharField(
        label="Quot",
        required=True,
        widget=Textarea(attrs={"class": "form-control"}))

    tags = CharField(
        label="Tags",
        required=True,
        widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Quot
        fields = ["author", "quot", "tags"]
