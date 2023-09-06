from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AuthorForm, QuotForm
from .models import Quot, Author, Tag


def index(request):
    quotes = Quot.objects.filter().all()
    return render(request,
                  "quotes_app/index.html",
                  context={"title": "Quotes app main", "quotes": quotes, "empty_text":"____________________"})


@login_required
def add_author(request):
    if request.method == "POST":

        author_form = AuthorForm(request.POST, instance=Author())

        print(f"USER: {request.user}")
        print(f"author_form.is_valid(): {author_form.is_valid()}")
        print(f"author_form cleaned_data fullname: {author_form.cleaned_data['fullname']}")

        if author_form.is_valid():
            # author_form.save(commit=False)
            authors = Author.objects.filter(fullname=author_form.cleaned_data['fullname']).all()
            if not authors:
                author_form.save()

            return redirect(to="quotes_app:main")

        else:
            print(author_form.errors)

    else:

        author_form = AuthorForm()

        return render(request, "quotes_app/author.html", context={"title": "Author creation", "form": author_form})


@login_required
def add_quot(request):
    if request.method == "POST":

        quot_form = QuotForm(request.POST)

        if quot_form.is_valid():

            quot = quot_form.save(commit=False)
            quot.save()
            tag_names = str(quot_form.cleaned_data["tags"])

            for tag_name in tag_names.split(","):

                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                quot.tags.add(tag)

            return redirect(to="quotes_app:main")

        else:
            print(quot_form.errors)

    else:

        quot_form = QuotForm()

        return render(request, "quotes_app/quot.html", context={"title": "Quot add", "form": quot_form})

# @login_required
# def edit(request, img_id):
#     if request.method == "POST":
#         description = request.POST.get("description")
#         Picture.objects.filter(pk=img_id, user=request.user).update(description=description)
#         return redirect(to="photo_app:pictures")
#
#     pic = Picture.objects.filter(pk=img_id, user=request.user).first()
#     return render(request, "photo_app/change.html", context={"title": "Change description", "pic": pic})
