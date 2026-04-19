from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import *
from django.contrib import messages
from django.db.models import Avg, Count
import uuid




def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, "Паролҳо мувофиқат намекунанд")
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ин почтаи электронӣ аллакай сабт шудааст!")
            return render(request, 'register.html')
        user = User(email=email, email_token=str(uuid.uuid4()))
        user.set_password(password)
        user.is_verified = False
        user.save()
        link = f'http://127.0.0.1:8000/verify/{user.email_token}/'
        try:
            send_mail(
                'Тасдиқи суроғаи электронӣ',
                f'Барои тасдиқи почтаи электронии худ ба ин пайванд клик кунед: {link}',
                None, [email], fail_silently=False,
            )
            messages.success(request, "Почтаи худро санҷед! Паёми тасдиқ фиристода шуд.")
        except Exception:
            messages.error(request, "Хатогӣ ҳангоми фиристодани почта.")
        return redirect('login')
    return render(request, 'register.html')


def verify_email(request, token):
    user = User.objects.filter(email_token=token).first()
    if user:
        user.is_verified = True
        user.save()
        messages.success(request, "Почтаи электронӣ бо муваффақият тасдиқ шуд!")
        return redirect('login')
    messages.error(request, "Пайванди нодуруст ё кӯҳнашуда!")
    return redirect('login')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            if not getattr(user, 'is_verified', False):
                messages.error(request, "Лутфан, аввал почтаи электронии худро тасдиқ кунед.")
                return redirect('login')
            request.session['user_id'] = user.id
            messages.success(request, "Шумо бо муваффақият вориди сайт шудед!")
            return redirect('home')
        messages.error(request, "Логин ё парол нодуруст аст.")
        return redirect('login')
    return render(request, 'login.html')


def reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.reset_token = str(uuid.uuid4())
            user.save()
            link = f'http://127.0.0.1:8000/reset/{user.reset_token}/'
            send_mail('Барқароркунии парол',
                      f"Барои иваз кардани пароли худ ба ин пайванд гузаред: {link}",
                      None, [email])
        messages.success(request, "Агар ин почта мавҷуд бошад, дастурамал фиристода шуд.")
        return redirect('login')
    return render(request, 'reset_request.html')


def reset_confirm(request, token):
    user = User.objects.filter(reset_token=token).first()
    if not user:
        messages.error(request, "Пайванди барқароркунӣ нодуруст аст!")
        return redirect('login')
    if request.method == "POST":
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.reset_token = None
        user.save()
        messages.success(request, "Пароли шумо бо муваффақият иваз карда шуд!")
        return redirect('login')
    return render(request, 'reset_confirm.html')


def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        old = request.POST.get('current_password')
        new = request.POST.get('new_password')
        if not user.check_password(old):
            messages.error(request, "Пароли ҷорӣ нодуруст аст.")
            return redirect('change_password')
        user.set_password(new)
        user.save()
        messages.success(request, "Парол бо муваффақият нав карда шуд!")
        return redirect('home')
    return render(request, 'change_password.html')


def log_out(request):
    request.session.flush()
    return redirect('login')


def home(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'home.html')




def list_category(request):
    if not request.session.get('user_id'):
        return redirect('login')
    query = request.GET.get('q', '').strip()
    categories = Category.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, 'categories.html', {'categories': categories, 'query': query})


def create_category(request):
    if not request.session.get('user_id'):
        return redirect('login')
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Категория илова карда шуд.")
            return redirect('list_category')
        messages.error(request, "Номи категорияро ворид кунед.")
    return render(request, 'create_category.html')


def detail_category(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    category = get_object_or_404(Category, id=id)
    return render(request, 'detail_category.html', {'category': category})


def update_category(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            category.name = name
            category.save()
            messages.success(request, "Категория нав карда шуд.")
            return redirect('list_category')
        messages.error(request, "Номи категорияро ворид кунед.")
    return render(request, 'update_category.html', {'category': category})


def delete_category(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Категория нест карда шуд.")
        return redirect('list_category')
    return render(request, 'delete_category.html', {'category': category})



def list_author(request):
    if not request.session.get('user_id'):
        return redirect('login')
    query = request.GET.get('q', '').strip()
    authors = Author.objects.all()
    if query:
        authors = authors.filter(full_name__icontains=query)
    return render(request, 'authors.html', {'authors': authors, 'query': query})


def create_author(request):
    if not request.session.get('user_id'):
        return redirect('login')
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        bio = request.POST.get('bio', '').strip()
        if full_name and bio:
            Author.objects.create(full_name=full_name, bio=bio)
            messages.success(request, "Муаллиф илова карда шуд.")
            return redirect('list_author')
        messages.error(request, "Ҳамаи майдонҳоро пур кунед.")
    return render(request, 'create_author.html')


def detail_author(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    author = get_object_or_404(Author, id=id)
    return render(request, 'detail_author.html', {'author': author})


def update_author(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    author = get_object_or_404(Author, id=id)
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        bio = request.POST.get('bio', '').strip()
        if full_name and bio:
            author.full_name = full_name
            author.bio = bio
            author.save()
            messages.success(request, "Маълумоти муаллиф нав карда шуд.")
            return redirect('list_author')
        messages.error(request, "Ҳамаи майдонҳоро пур кунед.")
    return render(request, 'update_author.html', {'author': author})


def delete_author(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    author = get_object_or_404(Author, id=id)
    if request.method == "POST":
        author.delete()
        messages.success(request, "Муаллиф нест карда шуд.")
        return redirect('list_author')
    return render(request, 'delete_author.html', {'author': author})



def list_book(request):
    if not request.session.get('user_id'):
        return redirect('login')
    books = Book.objects.select_related('author', 'category').all()
    search    = request.GET.get('search', '').strip()
    category  = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    if search:
        books = books.filter(title__icontains=search)
    if category:
        books = books.filter(category_id=category)
    if price_min:
        books = books.filter(price__gte=price_min)
    if price_max:
        books = books.filter(price__lte=price_max)
    categories = Category.objects.all()
    return render(request, 'books.html', {'books': books, 'categories': categories})


def create_book(request):
    if not request.session.get('user_id'):
        return redirect('login')
    if request.method == "POST":
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price')
        cover_image = request.FILES.get('cover_image')
        author_id   = request.POST.get('author')
        category_id = request.POST.get('category')
        if not all([title, description, price, author_id, category_id]):
            messages.error(request, "Ҳамаи майдонҳоро пур кунед.")
        else:
            author   = get_object_or_404(Author, id=author_id)
            category = get_object_or_404(Category, id=category_id)
            created_by = get_object_or_404(User, id=request.session['user_id'])
            Book.objects.create(
                title=title, description=description, price=price,
                cover_image=cover_image, author=author,
                category=category, created_by=created_by
            )
            messages.success(request, "Китоб илова карда шуд.")
            return redirect('list_book')
    authors    = Author.objects.all()
    categories = Category.objects.all()
    return render(request, 'create_book.html', {'authors': authors, 'categories': categories})


def detail_book(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    book    = get_object_or_404(Book, id=id)
    reviews = book.reviews.select_related('user').all()
    return render(request, 'detail_book.html', {'book': book, 'reviews': reviews})


def update_book(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price')
        cover_image = request.FILES.get('cover_image')
        author_id   = request.POST.get('author')
        category_id = request.POST.get('category')
        if not all([title, description, price, author_id, category_id]):
            messages.error(request, "Ҳамаи майдонҳоро пур кунед.")
        else:
            book.title       = title
            book.description = description
            book.price       = price
            if cover_image:
                book.cover_image = cover_image
            book.author   = get_object_or_404(Author, id=author_id)
            book.category = get_object_or_404(Category, id=category_id)
            book.save()
            messages.success(request, "Маълумоти китоб нав карда шуд.")
            return redirect('list_book')
    authors    = Author.objects.all()
    categories = Category.objects.all()
    return render(request, 'update_book.html', {'book': book, 'authors': authors, 'categories': categories})


def delete_book(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Китоб нест карда шуд.")
        return redirect('list_book')
    return render(request, 'delete_book.html', {'book': book})



def list_review(request, book_id):
    if not request.session.get('user_id'):
        return redirect('login')
    book    = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.select_related('user').all()
    return render(request, 'reviews.html', {'reviews': reviews, 'book': book})


def create_review(request, book_id):
    if not request.session.get('user_id'):
        return redirect('login')
    book = get_object_or_404(Book, id=book_id)
    user = get_object_or_404(User, id=request.session['user_id'])
    if request.method == "POST":
        text   = request.POST.get('text', '').strip()
        rating = request.POST.get('rating')
        if text and rating:
            Review.objects.create(book=book, user=user, text=text, rating=rating)
            messages.success(request, "Шарҳи шумо илова карда шуд.")
            return redirect('detail_book', id=book_id)
        messages.error(request, "Ҳамаи майдонҳоро пур кунед.")
    return render(request, 'create_review.html', {'book': book})


def detail_review(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    review = get_object_or_404(Review, id=id)
    return render(request, 'detail_review.html', {'review': review})


def update_review(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    review       = get_object_or_404(Review, id=id)
    current_user = get_object_or_404(User, id=request.session['user_id'])
    if review.user.id != current_user.id and not current_user.is_staff:
        messages.error(request, "Шумо ҳуқуқи тағир додани ин баррасиро надоред.")
        return redirect('detail_book', id=review.book.id)
    if request.method == "POST":
        text   = request.POST.get('text', '').strip()
        rating = request.POST.get('rating')
        if text and rating:
            review.text   = text
            review.rating = rating
            review.save()
            messages.success(request, "Шарҳи шумо бо муваффақият нав карда шуд.")
            return redirect('detail_book', id=review.book.id)
        messages.error(request, "Ҳамаи майдонҳоро пур кунед.")
    return render(request, 'update_review.html', {'review': review})


def delete_review(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    review       = get_object_or_404(Review, id=id)
    current_user = get_object_or_404(User, id=request.session['user_id'])
    book_id      = review.book.id
    if review.user.id != current_user.id and not current_user.is_staff:
        messages.error(request, "Шумо ҳуқуқи нест кардани ин баррасиро надоред.")
        return redirect('detail_book', id=book_id)
    if request.method == "POST":
        review.delete()
        messages.success(request, "Баррасӣ нест карда шуд.")
        return redirect('detail_book', id=book_id)
    return render(request, 'delete_review.html', {'review': review})





def statistics(request):
    if not request.session.get('user_id'):
        return redirect('login')
    total_books = Book.objects.count()
    avg_price   = Book.objects.aggregate(Avg('price'))['price__avg'] or 0
    top_authors = Author.objects.annotate(count=Count('books')).order_by('-count')[:5]

    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'total_books': total_books,
        'avg_price':   round(avg_price, 2),
        'top_authors': top_authors,
        'avg_rating':  round(avg_rating, 1),
    }
    return render(request, 'statistics.html', context)
