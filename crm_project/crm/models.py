from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


LEAD_CHOICES = (
    # Choosing to which segment the lead belongs to.
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Customer Support', 'Customer Support'),
        ('Else', 'Else'),
    )

SOURCE_CHOICES = (
    ('Newsletter', 'Newsletter'),
    ('YouTube', 'YouTube'),
    ('Research/Google', 'Research/Google'),
    ('Cold Call/Email', 'Cold Call/Email'),
    ('Else', 'Else'),
)


class User(AbstractUser):
    """Nothing needs to be changed, we are keeping all the fields from the AbstractUser."""
    pass


class Company(models.Model):
    """Company profile."""
    company = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField()
    lead = models.CharField(choices=LEAD_CHOICES, default='Else', max_length=20)
    phone_number = PhoneNumberField(blank=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company


class Agent(models.Model):
    """Users/Workers profiles."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"


class Client(models.Model):
    """Client profile."""
    first_name = models.CharField(max_length=100, verbose_name='First Name')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Last Name')
    email = models.EmailField(verbose_name='Email')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='City')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Country')
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name='Phone Number')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Company')
    date_created = models.DateField(auto_now_add=True, verbose_name='Date Created')
    lead = models.CharField(choices=LEAD_CHOICES, default='Else', max_length=20, verbose_name='Lead')
    title = models.CharField(max_length=50, verbose_name='Title')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    source = models.CharField(choices=SOURCE_CHOICES, max_length=100, default='Else', verbose_name='Source')
    lead_owner = models.ForeignKey(Agent, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Lead Agent')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


