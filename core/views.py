import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, CustomUser , Budget, Category, Transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from collections import defaultdict
from decimal import Decimal, InvalidOperation
import random
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email_address import validate_email
from django.http import JsonResponse
import re
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum
from datetime import date ,datetime
import calendar
import time
from django.contrib.auth.decorators import login_required
import json
from .models import Transaction, Budget







NAME_REGEX = re.compile(r'^[A-Za-z\s]{7,50}$')
EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # 1. Email format check
        if not EMAIL_REGEX.match(username):
            messages.error(request, "Please enter a valid email address.")
            return redirect("login_page")

        # 2. Email existence check
        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, "This email is not registered with us.")
            return redirect("login_page")

        # 3. Password empty check
        if not password:
            messages.error(request, "Please enter your password.")
            return redirect("login_page")

        # 4. Authenticate credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24 * 7)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Incorrect password.")
            return redirect("login_page")

    return render(request, 'login_page.html')


def logout_user(request):
    logout(request)  
    
    return redirect("login_page")





def signup(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname', '').strip()
        username = request.POST.get('username', '').strip()  # email
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # 1. Full name check
        if not NAME_REGEX.match(fullname):
            messages.error(request, "Full name must be 7–50 letters and contain only alphabets.")
            return redirect('signup')

        # 2. Email format check
        if not EMAIL_REGEX.match(username):
            messages.error(request, "Invalid email format.")
            return redirect('signup')

        # 3. Email already registered
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        # 4. Password strength check
        if not PASSWORD_REGEX.match(password1):
            messages.error(request, "Password must be at least 8 characters, include uppercase, lowercase, digit, and special character.")
            return redirect('signup')

        # 5. Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # 6. Create user
        user = CustomUser.objects.create_user(
            fullname=fullname,
            username=username,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login_page')

    return render(request, 'signup.html')



@login_required(login_url='login_page')
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('date')
    category_totals = defaultdict(Decimal)

    for t in transactions:
        try:
            category_totals[t.category] += Decimal(t.amount)
        except (InvalidOperation, TypeError):
            continue

    donut_labels = list(category_totals.keys())
    donut_data = [float(val) for val in category_totals.values()]

    line_data = defaultdict(lambda: {'Income': Decimal(0), 'Expense': Decimal(0)})
    for t in transactions:
        date_str = t.date.strftime('%Y-%m-%d')
        amt = abs(Decimal(t.amount))
        if t.amount > 0:
            line_data[date_str]['Income'] += amt
        elif t.amount < 0:
            line_data[date_str]['Expense'] += amt

    line_labels = list(line_data.keys())
    line_income = [float(line_data[date]['Income']) for date in line_labels]
    line_expense = [float(line_data[date]['Expense']) for date in line_labels]

    total_income = sum(Decimal(t.amount) for t in transactions if Decimal(t.amount) > 0)
    total_expense = sum(abs(Decimal(t.amount)) for t in transactions if Decimal(t.amount) < 0)
    balance = total_income - total_expense

    total = total_income + total_expense
    income_progress = round((total_income / total) * 100, 2) if total else 0
    expense_progress = round((total_expense / total) * 100, 2) if total else 0

    # ======== Budget Exceed Notifications ========
    exceeded_notifications = []
    budgets = Budget.objects.filter(user=request.user)  # Only current user's budgets

    for budget in budgets:
        total_expenses = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            date__month=budget.month,
            date__year=budget.year,
            amount__lt=0  # Only expenses
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expenses = abs(total_expenses)  # Convert to positive for comparison
        if total_expenses > budget.amount:
            exceeded_notifications.append(
                f"⚠ {budget.category.name} expenses exceeded the budget of ₹{budget.amount:.2f} (Spent: ₹{total_expenses:.2f})"
            )

    context = {
        'donut_labels': json.dumps(donut_labels),
        'donut_data': json.dumps(donut_data),
        'line_labels': json.dumps(line_labels),
        'line_income': json.dumps(line_income),
        'line_expense': json.dumps(line_expense),
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'income_progress': income_progress,
        'expense_progress': expense_progress,
        'table': transactions,
        'exceeded_notifications': exceeded_notifications,  # 🔥 Added for template alerts
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='login_page')
def add_trans(request):
    if request.method == "POST":
        date_val = request.POST.get("date")
        description = request.POST.get("description")
        category_name = request.POST.get("category")  # string
        amount_val = Decimal(request.POST.get("amount"))

        Transaction.objects.create(
            user=request.user,
            description=description,
            category=category_name,
            amount=amount_val,
            date=date_val
        )

        month = int(date_val.split("-")[1])
        year = int(date_val.split("-")[0])

        try:
            category_obj = Category.objects.get(name=category_name)  # user filter hata diya
            budget = Budget.objects.filter(
                user=request.user,
                category=category_obj,
                month=month,
                year=year
            ).first()

            total_expenses = Transaction.objects.filter(
                user=request.user,
                category=category_name,
                date__month=month,
                date__year=year
            ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

            if budget and total_expenses > budget.amount:
                messages.error(request, f"Budget exceeded for {category_name}!")

        except Category.DoesNotExist:
            pass

        return redirect("add_transaction")

    return render(request, "add_transaction.html")



@login_required(login_url='login_page')
def delete_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk)
    txn.delete()
    return redirect('dashboard')


User = get_user_model()

def forget_password(request):
    step = 'email'

    if request.method == 'POST':
        # STEP 1: Send OTP
        if 'email' in request.POST:
            email = request.POST.get('email').strip()
            try:
                user = User.objects.get(username=email)  # assuming username = email
                otp = random.randint(1000, 9999)
                request.session['reset_email'] = email
                request.session['reset_otp'] = str(otp)

                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is {otp}',
                    'your_email@example.com',
                    [email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent to your email.")
                step = 'otp'
            except User.DoesNotExist:
                messages.error(request, "Email not registered.")
                step = 'email'

        # STEP 2: Verify OTP
        elif 'otp1' in request.POST:
            entered_otp = ''.join([
                request.POST.get('otp1', ''),
                request.POST.get('otp2', ''),
                request.POST.get('otp3', ''),
                request.POST.get('otp4', '')
            ])
            if entered_otp == request.session.get('reset_otp'):
                step = 'password'
            else:
                messages.error(request, "Invalid OTP.")
                step = 'otp'

        # STEP 3: Set New Password
        elif 'new_password' in request.POST:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                step = 'password'
            elif not new_password:
                messages.error(request, "Password cannot be empty.")
                step = 'password'
            else:
                try:
                    email = request.session.get('reset_email')
                    user = User.objects.get(username=email)

                    # Important: Only set and save if new_password is provided
                    if new_password:
                        user.set_password(new_password)
                        user.save()

                    # Verify password update
                    test_user = authenticate(
                        username=user.username,
                        password=new_password
                    )

                    if test_user is None:
                        messages.error(request, "Password update failed. Try again.")
                        step = 'password'
                    else:
                        request.session.flush()
                        messages.success(request, "Password reset successful. Please log in.")
                        return redirect('login_page')

                except User.DoesNotExist:
                    messages.error(request, "User not found. Please start again.")
                    step = 'email'

    return render(request, 'forget_password.html', {'step': step})

# Login Validation (works with email or username)
def validate_login(request):
    identifier = request.GET.get('username', '').strip()
    password = request.GET.get('password', '').strip()

    try:
        # Convert email to username if needed
        if User.objects.filter(email=identifier).exists():
            username = User.objects.get(email=identifier).username
        else:
            username = identifier  # Assume it's already username

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"status": "error", "field": "password", "message": "Incorrect password."})

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# Check if email exists
def check_email_exists(request):
    email = request.GET.get('email', '').strip()
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})





@login_required(login_url='login_page')
def financial_reports(request):
    user = request.user

    # Get month and year from query params, or default to current month/year
    month = request.GET.get('month')
    year = request.GET.get('year')

    now = datetime.now()
    if year is None or not year.isdigit():
        year = now.year
    else:
        year = int(year)

    if month is None or not month.isdigit():
        month = now.month
    else:
        month = int(month)

    # Filter transactions by user and year
    transactions_year = Transaction.objects.filter(
        user=user,
        date__year=year
    )

    # Monthly transactions (for selected month)
    transactions_month = transactions_year.filter(date__month=month)

    # Calculate sums for month
    total_income_month = transactions_month.filter(amount__gt=0).aggregate(sum=Sum('amount'))['sum'] or Decimal(0)
    total_expense_month = transactions_month.filter(amount__lt=0).aggregate(sum=Sum('amount'))['sum'] or Decimal(0)
    total_expense_month = abs(total_expense_month)
    savings_month = total_income_month - total_expense_month

    # Calculate sums for year
    total_income_year = transactions_year.filter(amount__gt=0).aggregate(sum=Sum('amount'))['sum'] or Decimal(0)
    total_expense_year = transactions_year.filter(amount__lt=0).aggregate(sum=Sum('amount'))['sum'] or Decimal(0)
    total_expense_year = abs(total_expense_year)
    savings_year = total_income_year - total_expense_year

    # Prepare list of years with transactions for dropdown
    years_with_data = Transaction.objects.filter(user=user).dates('date', 'year', order='DESC')
    years_list = [y.year for y in years_with_data]

    # Months for dropdown
    months_list = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    months_dict = dict(months_list)
    month_name = months_dict.get(month, '')
    


    context = {
        'month_name': month_name,
        'months_dict': months_dict,
        'total_income_month': total_income_month,
        'total_expense_month': total_expense_month,
        'savings_month': savings_month,
        'total_income_year': total_income_year,
        'total_expense_year': total_expense_year,
        'savings_year': savings_year,
        'selected_month': month,
        'selected_year': year,
        'months_list': months_list,
        'years_list': years_list,
    }

    return render(request, 'financial_reports.html', context)



@login_required(login_url='login_page')
def budgeting(request):
    user = request.user
    today = date.today()

    selected_month = today.month
    selected_year = today.year

    if request.method == "POST":
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        category_id = request.POST.get('category_id')
        budget_amount = request.POST.get('budget_amount')

        try:
            budget_amount = Decimal(budget_amount)
        except InvalidOperation:
            messages.error(request, "Invalid budget amount.")
            return redirect("budgeting")

        # User filter hata diya kyunki categories global hain
        category_obj = get_object_or_404(Category, id=category_id)

        Budget.objects.update_or_create(
            user=user,
            category=category_obj,
            month=month,
            year=year,
            defaults={"amount": budget_amount}
        )

        selected_month = month
        selected_year = year
        messages.success(request, f"Budget for {category_obj.name} updated successfully!")

    months_list = list(enumerate(calendar.month_name))[1:]
    years_list = range(today.year - 2, today.year + 3)

    # Global categories
    categories = Category.objects.all()

    budgets = Budget.objects.filter(user=user, month=selected_month, year=selected_year)

    budget_dict = {b.category.id: b.amount for b in budgets}
    budget_id_dict = {b.category.id: b.id for b in budgets}

    expenses_dict = {
        cat.id: Transaction.objects.filter(
            user=user,
            category=cat.name,
            date__month=selected_month,
            date__year=selected_year
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        for cat in categories
    }

    exceeded_notifications = [
        f"Budget exceeded for {cat.name}!"
        for cat in categories
        if expenses_dict[cat.id] > budget_dict.get(cat.id, Decimal('0.00'))
    ]

    return render(request, "budgeting.html", {
        "months_list": months_list,
        "years_list": years_list,
        "selected_month": selected_month,
        "selected_year": selected_year,
        "categories": categories,
        "budget_dict": budget_dict,
        "budget_id_dict": budget_id_dict,
        "expenses_dict": expenses_dict,
        "exceeded_notifications": exceeded_notifications,
    })


@login_required(login_url='login_page')
def delete_budget(request, category_id):
    budget = get_object_or_404(
        Budget,
        category_id=category_id,
        user=request.user
    )
    budget.delete()
    messages.success(request, "Budget deleted successfully!")
    return redirect("budgeting")




def resend_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Session expired. Please start again.'})

    otp = random.randint(1000, 9999)
    request.session['reset_otp'] = str(otp)
    request.session['reset_otp_time'] = time.time()

    send_mail(
        'Your new OTP for Password Reset',
        f'Your OTP is {otp}',
        'your_email@example.com',
        [email],
        fail_silently=False,
    )

    return JsonResponse({'status': 'success', 'message': 'OTP resent successfully.'})