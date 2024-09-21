
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .tasks import *
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.shortcuts import render
from .forms import *

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract the file
            csv_file = request.FILES['file']
            if csv_file.size > 1024 * 1024 * 1024:
                messages.error(request, 'File too large. Max size is 1GB.')
                return render(request, 'upload.html', {'form': form})

            # Save file and process asynchronously
            tmp_path = default_storage.save(f'tmp/{csv_file.name}', csv_file)

            process_csv.delay(tmp_path)

            messages.success(request, 'File is being processed asynchronously. You will be notified when it’s done.')
            return render(request, 'upload.html', {'form': form, 'message': 'File is being processed.'})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


@login_required
def query_builder(request):
    # Get filter parameters from the request
    keyword = request.GET.get('keyword', '')
    industry = request.GET.get('industry', '')
    founded_year = request.GET.get('founded_year', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    country = request.GET.get('country', '')
    current_employee_estimate = request.GET.get('current_employee_estimate', 0)
    total_employee_estimate = request.GET.get('total_employee_estimate', 0)

    queryset = Company.objects.all()
    if keyword:
        queryset = queryset.filter(name__icontains=keyword)
    if industry:
        queryset = queryset.filter(industry__icontains=industry)
    if founded_year:
        queryset = queryset.filter(founded_year=founded_year)
    if city:
        queryset = queryset.filter(locality__icontains=city)  
    if state:
        queryset = queryset.filter(locality__icontains=state)  
    if country:
        queryset = queryset.filter(country__icontains=country)
    if current_employee_estimate:
        queryset = queryset.filter(current_employee_estimate__gte=current_employee_estimate)
    if total_employee_estimate:
        queryset = queryset.filter(total_employee_estimate__lte=total_employee_estimate)

    total_records = queryset.count()
    industries = Company.objects.values_list('industry', flat=True).distinct()  
    queryset = queryset.order_by('name')  

    # Paginate the queryset
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'company_list': queryset,
        'companylist': page_obj, 
        'total_records': total_records,  # Total number of records found
        'industries': industries, 
    }
    return render(request, 'query.html', context)




@login_required
def manage_users(request):
    users = User.objects.all() 
    return render(request, 'user_management.html', {'users': users})

# Add a new user
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        

         # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'new_user.html')

        try:
            # Create the new user
            User.objects.create(username=username, email=email)
            messages.success(request, "New user added")
            return redirect('manage-users')
        except IntegrityError:
            messages.error(request, "There was an error adding the user.")
            return render(request, 'new_user.html')

    return render(request, 'new_user.html')

# Delete a user
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully")
        return redirect('manage-users')
    return redirect('manage-users')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('manage-users')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to homepage after successful registration
    else:
        form = SignUpForm()
    return render(request, 'new_user.html', {'form': form})

# User logout view
def logout_view(request):
    logout(request)
    return redirect('login')
