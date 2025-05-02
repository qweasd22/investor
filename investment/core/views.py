from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from .models import Client, Security, Investment, Deposit, QuoteHistory
from .forms import ClientForm, SecurityForm, InvestmentForm, DepositForm, QuoteForm
from .filters import InvestmentFilter, SecurityFilter
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView, ListView
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django_filters.views import FilterView

class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clients'
    paginate_by = 20  # Пагинация на 20 элементов

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_form.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def security_list(request):
    securities = Security.objects.all().prefetch_related('quotes')
    return render(request, 'securities.html', {'securities': securities})

def investment_list(request):
    investments = Investment.objects.all().select_related('client', 'security', 'deposit')
    filter = InvestmentFilter(request.GET, queryset=investments)
    return render(request, 'investments.html', {'filter': filter})


# Депозиты
def deposit_list(request):
    deposits = Deposit.objects.all().select_related('client')
    return render(request, 'deposits.html', {'deposits': deposits})

# История котировок

    
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuoteForm
def add_quote(request, pk):
    security = get_object_or_404(Security, pk=pk)
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.security = security
            quote.date = form.cleaned_data.get('date') or timezone.now().date()
            quote.save()
            return redirect('security_detail', pk=pk)
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})

def create_deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deposit_list')
    else:
        form = DepositForm()
    return render(request, 'deposits/form.html', {'form': form})

def create_security(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        Security.objects.create(code=code)
        return redirect('security_list')
    return render(request, 'create_security.html')

def create_investment(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        security_id = request.POST.get('security')
        deposit_id = request.POST.get('deposit')
        Investment.objects.create(client_id=client_id, security_id=security_id, deposit_id=deposit_id)
        return redirect('investment_list')
    clients = Client.objects.all()
    securities = Security.objects.all()
    deposits = Deposit.objects.all()
    return render(request, 'create_investment.html', {'clients': clients, 'securities': securities, 'deposits': deposits})

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('client_list')



def deposit_list(request):
    deposits = Deposit.objects.all().select_related('client')
    return render(request, 'deposits/list.html', {'deposits': deposits})

class DepositDetail(DetailView):
    model = Deposit
    template_name = 'deposits/detail.html'

class DepositUpdate(UpdateView):
    model = Deposit
    form_class = DepositForm
    template_name = 'deposits/form.html'
    success_url = reverse_lazy('deposit_list')

class DepositDelete(DeleteView):
    model = Deposit
    success_url = reverse_lazy('deposit_list')
    template_name = 'deposits/confirm_delete.html'

def deposit_list(request):
    deposits_list = Deposit.objects.all()
    paginator = Paginator(deposits_list, 10)
    page_number = request.GET.get('page')
    deposits = paginator.get_page(page_number)
    return render(request, 'deposits/list.html', {'deposits': deposits})

    


from django.views.generic import CreateView

class InvestmentCreateView(CreateView):
    model = Investment
    form_class = InvestmentForm
    template_name = 'investments/create.html'
    success_url = reverse_lazy('investment_list')

    def form_valid(self, form):
        try:
            form.instance.full_clean()
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class InvestmentListView(ListView):
    model = Investment
    template_name = 'investments/list.html'
    context_object_name = 'investments'
    ordering = ['-purchase_date']

class InvestmentUpdateView(UpdateView):
    model = Investment
    form_class = InvestmentForm
    template_name = 'investments/form.html'
    success_url = reverse_lazy('investment_list')

class InvestmentDeleteView(DeleteView):
    model = Investment
    template_name = 'investments/confirm_delete.html'
    success_url = reverse_lazy('investment_list')

class SecurityListView(ListView):
    model = Security
    template_name = 'securities/list.html'
    context_object_name = 'securities'
    paginate_by = 10

class SecurityCreateView(CreateView):
    model = Security
    form_class = SecurityForm
    template_name = 'securities/form.html'
    success_url = reverse_lazy('security_list')

class SecurityUpdateView(UpdateView):
    model = Security
    form_class = SecurityForm
    template_name = 'securities/form.html'
    success_url = reverse_lazy('security_list')

class SecurityDeleteView(DeleteView):
    model = Security
    template_name = 'securities/confirm_delete.html'
    success_url = reverse_lazy('security_list')

class SecurityDetailView(DetailView):
    model = Security
    template_name = 'securities/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quotes'] = self.object.quotes.all()[:30]
        return context

class QuoteCreateView(CreateView):
    model = QuoteHistory
    form_class = QuoteForm
    template_name = 'securities/quote_form.html'

    def form_valid(self, form):
        form.instance.security = Security.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('security_detail', kwargs={'pk': self.kwargs['pk']})