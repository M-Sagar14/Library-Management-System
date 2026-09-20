from django.db import models
from django.utils import timezone
from UserApp.models import User_Details,User
from datetime import timedelta

class Admin(models.Model):
    Sno=models.AutoField(primary_key=True)
    Admin_Id=models.CharField(max_length=20,unique=True)
    Admin_Name=models.CharField(max_length=50,unique=True)
    Email=models.EmailField()
    Password=models.CharField(max_length=255)
    Contact=models.IntegerField()
    Created_At=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.Admin_Name}"

class Books(models.Model):
    Sno=models.AutoField(primary_key=True)
    Book_Id=models.IntegerField(unique=True)
    Title=models.CharField(max_length=100)
    Author=models.CharField(max_length=50)
    Published_Year=models.IntegerField()
    ISBN = models.CharField(max_length=20)
    Total_Copies=models.IntegerField()
    Available_Copies=models.IntegerField()
    Category=models.CharField(max_length=30,blank=True,null=True)
    Edition=models.CharField(blank=True,null=True)
    Added_Date=models.DateTimeField(default=timezone.now)
    Last_Updated=models.DateTimeField(auto_now=True)
    Image=models.ImageField(upload_to='lms_images/',default='pexels-philippedonn-1133957.jpg', blank=True, null=True)

    def __str__(self):
        return f"{self.Title}"
    

class Ledger(models.Model):
     selected_choices=(
         ("Issued","issued"),
         ("Due","due"),
         ("Returned","returned")
     )
     Sno=models.AutoField(primary_key=True)
     Transaction_Id=models.CharField(max_length=20)
     Roll_Number=models.ForeignKey(User_Details,on_delete=models.CASCADE)
     Book_Id=models.ForeignKey(Books,on_delete=models.CASCADE)
     Issued_Date=models.DateTimeField(default=timezone.now)
     Due_Date=models.DateTimeField(blank=True,null=True)
     Returned_Date=models.DateTimeField(blank=True,null=True)
     Fines=models.IntegerField(default=0)
     Fine_Paid=models.BooleanField(default=False)
     Status=models.CharField(max_length=10,choices=selected_choices)



     def __str__(self):
         return f"{self.Transaction_Id} - {self.Roll_Number}"
class BookRequest(models.Model):
    request_status=[
        ('pending','pending'),
        ('approved','approved'),
        ('rejected','rejected'),
    ]
    sno = models.AutoField(primary_key=True)
    user=models.ForeignKey(User_Details,on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    request_date=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=10,choices=request_status,default='pending')

    def __str__(self):
        return f"{self.user.user.Name} requested {self.book.Title}"

    

def default_due_date():
    return timezone.now() + timedelta(days=14)
    
class BookIssue(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=default_due_date)
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.book.Title} issued to {self.user.Name}"

    @property
    def is_overdue(self):
        return not self.returned and timezone.now() > self.due_date

    def calculate_fine(self):
        """ ₹10 fine per day after due date """
        if self.returned and self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            return days_overdue * 10 
        return 0