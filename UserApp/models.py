from django.db import models
from django.utils import timezone

class User(models.Model):
    Sno = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100,unique=True)
    Email= models.EmailField(max_length=50,unique=True)
    Password = models.CharField(max_length=255)
    Created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.Name}"
class User_Details(models.Model):
     Sno = models.AutoField(primary_key=True)
     Roll_number = models.CharField(max_length=20,unique=True,null=True,blank=True)
     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='details')
     Contact = models.IntegerField(null=True,blank=True)
     DOB = models.DateField(null=True,blank=True)
     Gender = models.CharField(max_length=10,null=True,blank=True)
     Course = models.CharField(max_length=10,null=True,blank=True)
     Branch = models.CharField(max_length=20,null=True,blank=True)
     Year_of_Study=models.IntegerField(null=True,blank=True)
     Graduation_Year=models.IntegerField(null=True,blank=True)
     Address = models.CharField(max_length=100,null=True,blank=True)
      
     def __str__(self):
        return f"{self.Roll_number or 'Pending'}-{self.user.Name}"

