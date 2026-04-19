from django.db import models
from django.contrib.auth.hashers import make_password,check_password
import uuid


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)

    is_active = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False) 

    email_token = models.UUIDField(default=uuid.uuid4, editable=False)
    reset_token = models.UUIDField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    full_name = models.CharField(max_length=50)
    bio = models.TextField()

    def __str__(self):
        return self.full_name
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=15,decimal_places=2)
    cover_image = models.ImageField(upload_to="books/")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author,related_name='books',on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name='books',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='books',on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    book = models.ForeignKey(Book,related_name='reviews',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    
