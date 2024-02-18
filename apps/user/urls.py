from django.urls import path
from .views import SendPhoneNumberView, VerifyPhoneNumberView, UserMeApiView, AdminLoginView, LogoutView, AdminView, DeleteAdminView

urlpatterns = [
    path('api/send-phone/', SendPhoneNumberView.as_view()),
    path('api/verify-phone/', VerifyPhoneNumberView.as_view()),
    path('api/me/', UserMeApiView.as_view()),
    path('api/admin-login/', AdminLoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/admin/', AdminView.as_view()),
    path('api/admin-delete/<int:pk>/', DeleteAdminView.as_view()),
]