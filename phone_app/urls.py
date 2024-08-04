from django.urls import path

from phone_app.views import PhoneList, CreatePhone, PhoneDetail

urlpatterns = [
    path('', PhoneList.as_view(), name='phone_list'),
    path('create/', CreatePhone.as_view(), name='create_phone'),
    path('<slug:slug>/', PhoneDetail.as_view(), name='phone_detail')
]
