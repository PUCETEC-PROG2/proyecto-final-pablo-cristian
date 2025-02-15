from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Client, Purchase, PurchaseDetail, Category

from .forms import ClientForm, PurchaseForm, ProductForm

from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import PurchaseForm
from django.db.models import Sum
from django.utils import timezone


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


def welcome(request):
    return render(request, 'welcome.html', {'message': 'Bienvenidos'})

def home(request):
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'home.html', {'featured_products': featured_products})


def products(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category__name=category)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()
    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })



@login_required
def clients(request):
    clients_list = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients_list})

@login_required
def purchases(request):
    purchases_list = Purchase.objects.all().order_by('-date')
    return render(request, 'purchases.html', {'purchases': purchases_list})

@login_required
def add_purchase(request):
    PurchaseFormSet = inlineformset_factory(
        Purchase,
        PurchaseDetail,
        fields=('product', 'quantity'),
        extra=3,
        can_delete=True
    )

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.date = timezone.now().date()  # Asignar fecha actual
            purchase.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.purchase = purchase
                instance.subtotal = instance.product.price * instance.quantity
                instance.save()
            
            # Actualizar total de la compra
            purchase.total = purchase.purchasedetail_set.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
            purchase.save()
            return redirect('compras')
    else:
        form = PurchaseForm()
        formset = PurchaseFormSet()

    return render(request, 'add_purchase.html', {
        'form': form,
        'formset': formset
    })

@login_required
def purchase_details(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    details = purchase.purchasedetail_set.all()
    return render(request, 'purchase_details.html', {
        'purchase': purchase,
        'details': details
    })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form})

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('clientes')
    return render(request, 'confirm_delete_client.html', {'client': client})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirige si ya está autenticado

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
