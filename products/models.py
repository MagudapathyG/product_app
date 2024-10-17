from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

def encrypt_price(plain_price, cipher):
    """Encrypt the price before storing it in the database."""
    encrypted_price = cipher.encrypt(plain_price.encode())
    return encrypted_price.decode()  

def decrypt_price(encrypted_price, cipher):
    """Decrypt the price when retrieving it."""
    decrypted_price = cipher.decrypt(encrypted_price.encode()).decode()
    return decrypted_price

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=255)  # Store encrypted price
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Encrypt the price before saving
        if isinstance(self.price, str):  # Ensure it's a string
            cipher = Fernet(settings.ENCRYPTION_KEY.encode())
            self.price = encrypt_price(self.price, cipher)
        super().save(*args, **kwargs)

    def get_price(self):
        # Decrypt the price when accessed
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        return decrypt_price(self.price, cipher)



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


