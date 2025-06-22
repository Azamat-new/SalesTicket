from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ReviewForm
from .models import Ticket, Purchase, Review, Favorite
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator

def get_index(request):
    tickets_list = Ticket.objects.filter(is_available=True).order_by('date')
    paginator = Paginator(tickets_list, 3)

    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)

    return render(request, 'ticket/index.html', {'tickets': tickets})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'ticket/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm
    return render(request, 'ticket/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'ticket/profile.html')


@login_required
def logout(request):
    return render(request, 'ticket/logout.html')


# def get_ticket(request):
#     tickets = Ticket.objects.filter(is_available=True).order_by('date')
#     return render(request, 'ticket/index.html', {'tickets': tickets})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    already_bought = Purchase.objects.filter(user=request.user, ticket=ticket).exists()

    return render(request, 'ticket/event-detail.html',{
        'ticket': ticket,
        'already_bought': already_bought
    })


@login_required
def buy_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if Purchase.objects.filter(user=request.user, ticket=ticket).exists():
        messages.warning(request, "Вы уже купили этот билет")

    else:
        Purchase.objects.create(user=request.user, ticket=ticket)
        messages.success(request, f"Билет {ticket.title} успешно куплен!")

    return redirect('ticket_detail', ticket_id=ticket.id)


@login_required
def my_tickets(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('ticket')

    return render(request, 'ticket/profile.html', {'purchases': purchases})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    already_bought = Purchase.objects.filter(user=request.user, ticket=ticket).exists()
    can_review = already_bought and not Review.objects.filter(user=request.user, ticket=ticket).exists()
    reviews = ticket.reviews.all().order_by('-created_at')

    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, 'Спасибо за отзыв!')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = ReviewForm()

    return render(request, 'ticket/event-detail.html', {
        'ticket': ticket,
        'already_bought': already_bought,
        'can_review': can_review,
        'reviews': reviews,
        'form': form,
        'is_favorite': Favorite.objects.filter(user=request.user, ticket=ticket).exists()
    })


@login_required
def toggle_favorite(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, ticket=ticket)
    if not created:
        fav.delete()
        messages.info(request, 'Удалено из избранного')
    else:
        messages.success(request, 'Добавлено в избранное')
    return redirect('ticket_detail', ticket_id=ticket_id)


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('ticket')
    return render(request, 'ticket/favorites.html', {'favorites': favorites})
















