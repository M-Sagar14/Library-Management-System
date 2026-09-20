from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from .models import Books,Admin,BookRequest,BookIssue,Ledger
from UserApp.models import User,User_Details
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
import plotly.express as px
import plotly.graph_objects as go

# Create your views here.
def dashboard(request):
    admin_id=request.session.get('admin_id')
    if not admin_id:
        return redirect('login')
    try:
        admin_user=Admin.objects.get(Sno=admin_id)
    except Admin.DoesNotExist:
        return HttpResponse("no Admin found")
    
    users=User.objects.count()
    books=Books.objects.count()
    
    return render(request,'dashboard.html',{'books':books,'users':users})
def analytics(request):
    # ---------------- Books by Category ----------------
    category_summary = Books.objects.values('Category').annotate(total=Count('Sno'))
    categories = [c['Category'] or "Uncategorized" for c in category_summary]
    category_counts = [c['total'] for c in category_summary]

    fig_books_category = px.pie(
        names=categories,
        values=category_counts,
        title="Books by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    books_category_plot = fig_books_category.to_html(full_html=False, include_plotlyjs=False)

    # ---------------- Books by Published Year ----------------
    year_summary = Books.objects.values('Published_Year').annotate(total=Count('Sno')).order_by('Published_Year')
    years = [y['Published_Year'] for y in year_summary]
    year_counts = [y['total'] for y in year_summary]

    fig_books_year = px.bar(
        x=years,
        y=year_counts,
        title="Books by Published Year",
        labels={'x': 'Year', 'y': 'Number of Books'},
        color=year_counts,
        color_continuous_scale='Viridis'
    )
    books_year_plot = fig_books_year.to_html(full_html=False, include_plotlyjs=False)

    # ---------------- Books Availability Status ----------------
    available_count = Books.objects.filter(Available_Copies__gt=0).count()
    unavailable_count = Books.objects.filter(Available_Copies=0).count()

    fig_books_availability = px.pie(
        names=['Available', 'Not Available'],
        values=[available_count, unavailable_count],
        title="Books Availability Status",
        color_discrete_sequence=['#7b4397', '#dc2430']
    )
    books_availability_plot = fig_books_availability.to_html(full_html=False, include_plotlyjs=False)

    # ---------------- Requests by Book (Most Requested Books) ----------------
    book_request_summary = (
        BookRequest.objects.values('book__Title')
        .annotate(total=Count('sno'))
        .order_by('-total')[:10]  # Top 10 most requested books
    )
    books_req_titles = [b['book__Title'] for b in book_request_summary]
    books_req_counts = [b['total'] for b in book_request_summary]

    fig_requests_book = px.bar(
        x=books_req_titles,
        y=books_req_counts,
        title="Top 10 Most Requested Books",
        labels={'x': 'Book Title', 'y': 'Number of Requests'},
        color=books_req_counts,
        color_continuous_scale='Inferno'
    )
    requests_book_plot = fig_requests_book.to_html(full_html=False, include_plotlyjs=False)

    # ---------------- Ledger Status ----------------
    ledger_summary = Ledger.objects.values('Status').annotate(total=Count('Sno'))
    ledger_labels = [l['Status'].capitalize() for l in ledger_summary]
    ledger_data = [l['total'] for l in ledger_summary]

    fig_ledger = px.pie(
        names=ledger_labels,
        values=ledger_data,
        title="Books by Ledger Status",
        color_discrete_sequence=['#7b4397', '#dc2430', '#ff9900']
    )
    ledger_plot = fig_ledger.to_html(full_html=False, include_plotlyjs=False)

    context = {
        'books_category_plot': books_category_plot,
        'books_year_plot': books_year_plot,
        'books_availability_plot': books_availability_plot,
        'requests_book_plot': requests_book_plot,
        'ledger_plot': ledger_plot,
    }

    return render(request, 'analytics.html', context)
def history(request):
    requests = BookRequest.objects.select_related('user', 'book').all().order_by('request_date')
    
    issues = BookIssue.objects.select_related('user', 'book').all()
    
    request_issue_map = {}
    for r in requests:
        issue = issues.filter(user=r.user, book=r.book).first()  # None if not issued
        request_issue_map[r.sno] = issue
    
    return render(request, 'history.html', {
        'requests': requests,
        'request_issue_map': request_issue_map
    })

def ledger(request):
    return render(request,'ledger.html')
def books(request):
    query = request.GET.get('q', '')
    books = Books.objects.all()

    if query:
        books = books.filter(
            Title__icontains=query
        ) | books.filter(
            Author__icontains=query
        ) | books.filter(
            Category__icontains=query
        )

    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books.html', {
        'page_obj': page_obj,
        'query': query,
    })


    return render(request,'Books.html',{'page_obj':page_obj,'query':query})
def members(request):
    users_list = User.objects.all().order_by('Name')
    return render(request, 'members.html', {'members': users_list})

    
def requests(request):
    request_book = BookRequest.objects.filter(status='pending').select_related('user','book') 
    return render(request, 'requests.html' ,{'request_book':request_book})

def Add(request):
    if request.method == "POST":
        
        book_id = request.POST["Book_Id"]
        title=request.POST["Title"]
        author=request.POST["Author"]
        published_year=request.POST["Published_Year"]
        isbn=request.POST["ISBN"]
        total_copies=request.POST["Total_Copies"]
        available_copies=request.POST["Available_Copies"]
        category=request.POST["Category"]
        edition=request.POST["Edition"]
        image=request.FILES.get("Image")

        Books.objects.create(
            Book_Id=book_id,
            Title=title,
            Author=author,
            Published_Year=published_year,
            ISBN=isbn,
            Total_Copies=total_copies,
            Available_Copies=available_copies,
            Category=category,
            Edition=edition,
            Image=image,
        )
        return redirect("AdminApp:books")



    return render(request, "Add.html")
def update(request,id):
    book = get_object_or_404(Books, Book_Id=id)

    if request.method == "POST":
        image=request.FILES.get("Image")
        book.Book_Id = request.POST.get("Book_Id")
        book.Title = request.POST.get("Title")
        book.Author = request.POST.get("Author")
        book.Published_Year = request.POST.get("Published_Year")
        book.ISBN = request.POST.get("ISBN")
        book.Total_Copies = request.POST.get("Total_Copies")
        book.Available_Copies = request.POST.get("Available_Copies")
        book.Category = request.POST.get("Category")
        book.Edition = request.POST.get("Edition") 
        book.save()
        if image:
            book.Image = image
            book.save()

        return redirect("AdminApp:books")

    return render(request, "update.html",{'book': book})


def logout(request):
    try:
        del request.session['admin_id']
    except KeyError:
        pass
    return redirect('login')

def change_password(request):
    admin_id = request.session.get('admin_id')
    print(admin_id)

    if not admin_id:
        return redirect('login')

    if request.method == "POST":
        current = request.POST["current_password"]
        new = request.POST["new_password"]
        confirm = request.POST["confirm_password"]

        try:
            user = User.objects.get(Sno = admin_id)
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


def edit(request):
    return render(request,'edit.html')
def delete_book(request,id):
    book=get_object_or_404(Books,Book_Id=id)
    if request.method=='POST':
        book.delete()
        return redirect('AdminApp:books')
    return render(request,'delete.html ',{'book':book})
def delete_member(request,id):
    try:
        user = User.objects.get(Sno=id)
        if hasattr(user, 'details'):
            user.details.delete()
        user.delete()
    except User.DoesNotExist:
        pass
    return redirect('AdminApp:members') 

def approve_request(request, id):
    req = get_object_or_404(BookRequest, sno=id)
    
    # req.save()

    if req.book.Available_Copies > 0:
        req.status = 'approved'
        req.book.Available_Copies -= 1
        req.book.save()
        req.save()
        print("✅ Approve Request called for:", id)
        BookIssue.objects.create(user=req.user, book=req.book, issued_by=None)  # add admin if logged in
        messages.success(request, f"Book '{req.book.Title}' issued to {req.user.user.Name}.")
    else:
        messages.error(request, "No available copies to issue.")

    return redirect('AdminApp:requests')

def reject_request(request,id):
    req = get_object_or_404(BookRequest, sno=id)
    req.status = 'rejected'
    req.save()
    messages.warning(request, "Book request rejected.")
    return redirect('AdminApp:requests')
