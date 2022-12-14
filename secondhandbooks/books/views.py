from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.db.models.functions import Lower
from comment.forms import CommentForm
from .models import Book, Category, Review
from .forms import BookForm, ReviewForm

# Create your views here.


def all_books(request):
    """ A view to show all books, including sorting and search queries """

    books = Book.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    style = "display: block;"

    if request.GET:
        style = "display: none;"
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                books = books.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            books = books.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            books = books.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('books'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            books = books.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'style': style
    }

    return render(request, 'books/books.html', context)


@login_required
def add_book(request):
    """ Add a book to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('books'))

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Successfully added book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(request,
                           ('Failed to add book. '
                            'Please ensure the form is valid.'))
    else:
        form = BookForm()

    template = 'books/add_book.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_book(request, book_id):
    """ Edit a book in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('books'))

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated book!')
            return redirect(reverse('book_detail', args=[book.id]))
        else:
            messages.error(request,
                           ('Failed to update book. '
                            'Please ensure the form is valid.'))
    else:
        form = BookForm(instance=book)
        messages.info(request, f'You are editing {book.name}')

    template = 'books/edit_book.html'
    context = {
        'form': form,
        'book': book,
    }

    return render(request, template, context)


@login_required
def delete_book(request, book_id):
    """ Delete a book from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('books'))

    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Book deleted!')
    return redirect(reverse('books'))


def book_detail(request, book_id):
    """ A view to show individual book details """

    book = get_object_or_404(Book, pk=book_id)
    comments = book.comments.filter(active=True)
    new_comment = None
    reviews = book.review.filter(reviewed=True).order_by("-created_on")
    total_review = reviews.count()
    avg_review = reviews.aggregate(review=Avg('review'))['review']

    if avg_review is None:
        avg_review = 0

    if request.method == 'POST' and request.user:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()

        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = Review.objects.filter(user=request.user, book=book)[::1]
            if len(review) > 0:
                review_edit = review[0]
                review_edit.review = review_form['review'].value()
                review_edit.save()
            else:
                new_review = review_form.save(commit=False)
                new_review.book = book
                new_review.user = request.user
                new_review.save()
            reviews = book.review.filter(reviewed=True).order_by("-created_on")
            total_review = reviews.count()
            avg_review = reviews.aggregate(review=Avg('review'))['review']
            book.rating = avg_review
            book.save()
    else:
        comment_form = CommentForm()
        review_form = ReviewForm()

    context = {
        'book': book, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'reviews': reviews,
        'total_review': total_review, 'avg_review': avg_review, 'review_form': review_form, 'iterator': range(1, 6)
    }

    return render(request, 'books/book_detail.html', context)


@login_required()
def add_review(request, book_id):
    """ View to add review in book"""
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.review.filter(reviewed=True).order_by("-created_on")

    if request.method == 'POST' and request.user:
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
    else:
        review_form = ReviewForm()

    context = {
        'reviews': reviews, 'book': book, 'review_form': review_form
    }

    return render(request, 'books/review_detail.html', context)
