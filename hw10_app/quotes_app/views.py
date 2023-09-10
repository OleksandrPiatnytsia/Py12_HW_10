from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import AuthorForm, QuotForm
from .models import Quot, Author, Tag
from .scraping import make_scraping


def scrap_data(request):
    if request.method == "GET":

        result_dict = make_scraping()

        saved_authors = {}

        for author_dict in result_dict["authors"]:

            author = Author.objects.filter(fullname=author_dict["fullname"]).first()

            if not author:
                author = Author()
                author.fullname = author_dict["fullname"]
                author.born_date = author_dict["born_date"]
                author.born_location = author_dict["born_location"]
                author.description = author_dict["description"]
                author.save()

            saved_authors.update({author.fullname: author})

        for quot_dict in result_dict["quotes"]:

            # db_author = Author.objects.filter(fullname=quot_dict["author"]).first()

            db_author = saved_authors.get(quot_dict["author"])

            print(f"fullname: {quot_dict['author']} class: {db_author}")

            if db_author:

                new_quot = Quot()
                new_quot.author = db_author
                new_quot.quot = quot_dict["quot"]
                new_quot.save()

                for tag_name in quot_dict["tags"]:

                    tag_db = Tag.objects.filter(name=tag_name).first()
                    if not tag_db:
                        new_tag = Tag()
                        new_tag.name = tag_name
                        new_tag.save()
                        tag_db = new_tag

                    new_quot.tags.add(tag_db)

                new_quot.save()

            else:
                print(f"problem author {quot_dict['author']}")

    return redirect(to="quotes_app:main")


def get_most_used_tags():

    sql_query = """CREATE TEMPORARY TABLE temp_table AS
                SELECT 
                  COUNT(1) AS tag_sum, 
                  quot_tags.tag_id as tag_id
                FROM 
                  quotes_app_quot_tags AS quot_tags
                GROUP BY 
                  quot_tags.tag_id
                ORDER BY 
                  tag_sum DESC 
                LIMIT 10;
                
                SELECT temp_table.tag_id AS tag_id,
                    quotes_app_tag.name AS tag_name, 
                    temp_table.tag_sum AS tag_sum
                FROM temp_table
                left join quotes_app_tag on
                temp_table.tag_id = quotes_app_tag.id
                ORDER BY 
                  tag_sum desc,
                  quotes_app_tag.name"""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)

        results = cursor.fetchall()

        column_names = ["tag_id", "tag_name", "tag_sum"]

        list_of_dicts = [dict(zip(column_names, row)) for row in results]

        for dict_ in list_of_dicts:
            dict_["font_size"] = dict_["tag_sum"]*0.16

        return list_of_dicts


def index(request):
    quotes = Quot.objects.all().order_by('creation_date', 'id')
    tag_list = get_most_used_tags()
    return render(request,
                  "quotes_app/index.html",
                  context={"title": "Quotes app main",
                           "quotes": quotes,
                           "quotes_view": False,
                           "tag_list": tag_list})


def author_page(request):
    author_id = request.GET.get('author_id')

    author = Author.objects.filter(id=author_id).first()

    return render(request, "quotes_app/author_page.html", context={"title": "Author page", "author": author})
    # return HttpResponse("Author Page for " + author.fullname)


def tags_search(request):
    tag_id = request.GET.get('tag_id')

    tag = Tag.objects.filter(id=tag_id).first()
    quotes = Quot.objects.filter(tags=tag).all()
    tag_list = get_most_used_tags()

    return render(request,
                  "quotes_app/index.html",
                  context={"title": "Tag search",
                           "quotes": quotes,
                           "quotes_view": True,
                           "tag": tag,
                           "tag_list": tag_list})

    # print(quotes)

    # return render(request, "quotes_app/author_page.html", context={"title": "Author page", "author": author})
    # return HttpResponse(f"tag id {tag} find some qotes {quotes}")


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

        return render(
            request,
            "quotes_app/quot.html",
            context={
                "title": "Quot add",
                "form": quot_form}
        )

# @login_required
# def edit(request, img_id):
#     if request.method == "POST":
#         description = request.POST.get("description")
#         Picture.objects.filter(pk=img_id, user=request.user).update(description=description)
#         return redirect(to="photo_app:pictures")
#
#     pic = Picture.objects.filter(pk=img_id, user=request.user).first()
#     return render(request, "photo_app/change.html", context={"title": "Change description", "pic": pic})
