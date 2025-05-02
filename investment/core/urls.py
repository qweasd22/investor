from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('create/', views.InvestmentCreateView.as_view(), name='investment_create'),
    path('list/', views.InvestmentListView.as_view(), name='investment_list'),
    path('investments/<int:pk>/edit/', views.InvestmentUpdateView.as_view(), name='investment_update'),
    path('investments/<int:pk>/delete/', views.InvestmentDeleteView.as_view(), name='investment_delete'),
    path('create/', views.InvestmentCreateView.as_view(), name='investment_create'),
    path('security/<int:pk>/quotes/', views.QuoteListView.as_view(), name='quote_list'),
    path('security/<int:pk>/quotes/add/', views.QuoteCreateView.as_view(), name='quote_create'),

    path('deposits/', views.deposit_list, name='deposit_list'),
    path('deposits/add/', views.create_deposit, name='add_deposit'),
    path('deposits/<int:pk>/', views.DepositDetail.as_view(), name='deposit_detail'),
    path('deposits/<int:pk>/edit/', views.DepositUpdate.as_view(), name='edit_deposit'),
    path('deposits/<int:pk>/delete/', views.DepositDelete.as_view(), name='delete_deposit'),

    path('securities/', views.SecurityListView.as_view(), name='security_list'),
    path('add/', views.SecurityCreateView.as_view(), name='security_create'),
    path('<int:pk>/', views.SecurityDetailView.as_view(), name='security_detail'),
    path('<int:pk>/edit/', views.SecurityUpdateView.as_view(), name='security_update'),
    path('<int:pk>/delete/', views.SecurityDeleteView.as_view(), name='security_delete'),
    path('<int:pk>/add-quote/', views.QuoteCreateView.as_view(), name='quote_create'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Добавьте аналогичные пути для других моделей
]