from django.urls import path, include
from . import api_views, html_views


app_name = 'main_app'

urlpatterns = [
    path('', html_views.start, name='start'),

    #Блок путей для моих любимых апи-вьюшек
    #path('api/pizza/', views_api.PizzaView.as_view(), name='pizza'),

    # Блок путей для вьюшек с дженериками
    # path('api/pizza/', views_api_GenericAPIViewMethod.PizzaListCreateView.as_view(), name='pizza-list-create'),
    # path('api/pizza/<int:pk>/', views_api_GenericAPIViewMethod.PizzaRetrieveUpdateDestroyView.as_view(), name='pizza-retrieve-update-destroy'),
    # path('api/drink/', views_api_GenericAPIViewMethod.DrinkListCreateView.as_view(), name='drink-list-create'),
    # path('api/drink/<int:pk>/', views_api_GenericAPIViewMethod.DrinkRetrieveUpdateDestroyView.as_view(), name='drink-retrieve-update-destroy'),
    # path('api/user/', views_api_GenericAPIViewMethod.UserListCreateView.as_view(), name='user-list-create'),
    # path('api/user/<int:pk>/', views_api_GenericAPIViewMethod.UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    # path('api/basket/', views_api_GenericAPIViewMethod.BasketListCreateView.as_view(), name='basket-list-create'),
    # path('api/basket/<int:pk>/', views_api_GenericAPIViewMethod.BasketRetrieveUpdateDestroyView.as_view(), name='basket-retrieve-update-destroy'),
    # path('api/order/', views_api_GenericAPIViewMethod.OrderListCreateView.as_view(), name='order-list-create'),
    # path('api/order/<int:pk>/', views_api_GenericAPIViewMethod.OrderRetrieveUpdateDestroyView.as_view(), name='order-retrieve-update-destroy'),

    # Блок путей для вьюшек с логическим ветвлением
    # path('api/pizza/', views_api_LogicMethod.PizzaView, name='pizza-list'),
    # path('api/drink/', views_api_LogicMethod.DrinkView, name='drink-list'),
    # path('api/user/', views_api_LogicMethod.UserView, name='user-list'),
    # path('api/basket/', views_api_LogicMethod.BasketView, name='basket-list'),
    # path('api/order/', views_api_LogicMethod.OrderView, name='order-list'),

    # Блок путей для вьюшек с декораторами
    # path('api/pizza/', views_api_DecoratorMethod.PizzaView, name='pizza-list'),
    # path('api/drink/', views_api_DecoratorMethod.DrinkView, name='drink-list'),
    # path('api/user/', views_api_DecoratorMethod.UserView, name='user-list'),
    # path('api/basket/', views_api_DecoratorMethod.BasketView, name='basket-list'),
    # path('api/order/', views_api_DecoratorMethod.OrderView, name='order-list'),

    # Блок путь для вьюшек модел-вью-сет
    # path('api/', include(router.urls)),

]