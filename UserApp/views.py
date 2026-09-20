from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from .models import User,User_Details
from django.core.paginator import Paginator
from AdminApp.models import Books,BookRequest
from django.contrib import messages


 
def dashboard(request):
    return render(request,'userdashboard.html')
def books_user(request):
    query = request.GET.get('q', '')
    books_list = Books.objects.filter(Title__icontains=query)
    paginator = Paginator(books_list, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_books.html', {'page_obj': page_obj, 'query': query})
    
def history_user(request):
    return render(request,'history_user.html')
def guide(request):
    return render(request,'guide.html')
def terms(request):
    return render(request,'terms_and_conditions.html')
def smart(request):
    return render(request,'smartai.html')
def profile(request):
    user_id=request.session.get("user_id")
    print(user_id)
    if not user_id:
        return redirect('login')
    try:
        user=User.objects.get(Sno = user_id)
    except User.DoesNotExist:
        return HttpResponse("Invalid Details")
    try:
        user_details=user.details
        profile_exists=True
    except User_Details.DoesNotExist:
        user_details=None
        profile_exists=False
    if request.method == "POST":
        roll_number = request.POST["Roll_number"]
        contact = request.POST["Contact"]
        dob = request.POST["DOB"]
        gender = request.POST["Gender"]
        branch = request.POST["Branch"]
        course = request.POST["Course"]
        year_of_study = request.POST["Year_of_study"]
        graduation_year = request.POST["Graduation_year"]
        address = request.POST["Address"]

        if profile_exists:
            user_details.Roll_number = roll_number
            user_details.Contact = contact
            user_details.DOB = dob
            user_details.Gender = gender
            user_details.Branch = branch
            user_details.Course = course
            user_details.Year_of_Study = year_of_study
            user_details.Graduation_Year = graduation_year
            user_details.Address = address

            user_details.save()
            return redirect('UserApp:profile_update')

        else :
            User_Details.objects.create(
                user = user,
                Roll_number = roll_number,
                Contact = contact,
                DOB = dob,
                Gender = gender,
                Branch = branch,
                Course = course,
                Year_of_Study = year_of_study,
                Graduation_Year = graduation_year,
                Address = address
            )
            return redirect('UserApp:profile_update')

    return render(request,'profile.html',{'user_details' : user_details,'profile_exists':profile_exists})

def change_password(request):
    user_id = request.session.get('user_id')
    print(user_id)

    if not user_id:
        return redirect('login')

    if request.method == "POST":
        current = request.POST["current_password"]
        new = request.POST["new_password"]
        confirm = request.POST["confirm_password"]

        try:
            user = User.objects.get(Sno = user_id)
        except User.DoesNotExist:
            return HttpResponse("No user found")
        
        if not check_password(current , user.Password) :
            return render(request, 'change_password.html' , {'error' : " Error ! Current passwords are not matched"})

        if new != confirm :
            return render(request, 'change_password.html' , {'error' : " Error !  passwords does not matched"})
        
        user.Password = make_password(new)
        user.save()

        return redirect('UserApp:dashboard')

    return render(request,'change_password.html')

    # def signout(request):
    #     logout(request)
    #     return redirect('login')



def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('login')

def profile_update(request):
    return render(request,'profile_update.html')

def request_book(request, book_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, Sno=user_id)
    user_details = get_object_or_404(User_Details, user=user)
    book = get_object_or_404(Books, Book_Id=book_id)

    existing_request = BookRequest.objects.filter(user=user_details, book=book, status='Pending').exists()
    if existing_request:
        messages.warning(request, "You already requested this book.")
        return redirect('UserApp:dashboard')

    BookRequest.objects.create(user=user_details, book=book)
    messages.success(request, "Your book request has been sent to the admin.")
    return redirect('UserApp:dashboard')


