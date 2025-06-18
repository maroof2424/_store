from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('contact/', views.contact, name='contact'),  # Contact URL
    
    # Authentication URLs
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Feedback URLs
    path('product/<int:pk>/feedback/', views.add_feedback, name='add_feedback'),
    path('product/<int:pk>/all-feedbacks/', views.all_feedbacks, name='all_feedbacks'),

    #Run Command
    path('run-migrations/', views.run_migrations, name='run_migrations'),
]