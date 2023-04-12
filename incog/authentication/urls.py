from django.urls import path
from authentication.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile, Login, account_check

from django.contrib.auth import views as auth_views

'''urlpatterns = [
    ...
    path('user/passwordreset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('user/passwordreset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('user/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('user/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    ...
]'''

urlpatterns = [
	path('account_check/', account_check, name='account_check'),
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	path('login/', Login, name='login'),
   	path('logout/', auth_views.LogoutView.as_view(), {'next_page' : 'login'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),
   	path('passwordreset/done', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
   	path('passwordreset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]