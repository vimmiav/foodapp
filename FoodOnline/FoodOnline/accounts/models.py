from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("user must have an email address")
        
        if not username:
            raise ValueError("user must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, 'restaurant'),
        (CUSTOMER, 'customer')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()  # Link the custom user manager

    def __str__(self):
        return self.first_name
    
    USERNAME_FIELD = 'email'

    

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='users/profile_picture',blank=True,null=True)
    cover_photo = models.ImageField(upload_to='users/cover_picture',blank=True,null=True)
    address_line_1 = models.CharField(max_length=100,blank=True,null=True)
    address_line_2 = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=30,blank=True,null=True)
    state = models.CharField(max_length=30,blank=True,null=True)
    city = models.CharField(max_length=30,blank=True,null=True)
    pin_code = models.CharField(max_length=10,blank=True,null=True)
    latitude = models.CharField(max_length=10,blank=True,null=True)
    longitude = models.CharField(max_length=10,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email
    


# Way 1
# Receiver function
# def post_user_create_profile_receiver(sender, instance, created, **kwargs):
#     pass

# post_save.connect(post_user_create_profile_receiver, sender=User)

# Way 2
@receiver(post_save, sender=User)
def post_user_create_profile_receiver(sender, instance, created, **kwargs):
    # print(created) # True
    if created:
        UserProfile.objects.create(user=instance)
        # print("user profile created")
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
        #     print("Profile doesnot exist, but we created one!!!")
        print("user is updated")

@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender,instance,**kwargs):
    pass
    # print(instance.first_name,"this user is being saved")





        


























        






