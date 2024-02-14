from django.urls import path
from .views import (about, 
                    admission, 
                    RegistrationStudents, 
                    LogoutView, 
                    LoginView,
                    ShartnomaView, 
                    ProfilePageView,
                    UpdateProfilePageView,
                    VerifyContract,
                    ContractDetailPageView,
                    StudentsListView
)

urlpatterns = [
    path("admission/", admission, name="admission"),
    path("about/", about, name="about"),
    path("students/registration/", RegistrationStudents.as_view(), name="register"),
    path("students/logout/", LogoutView.as_view(), name="logout"),
    path("students/login/", LoginView.as_view(), name="login"),
    path("students/contract/", ShartnomaView.as_view(), name="contract"),
    path("students/profile/", ProfilePageView.as_view(), name="profile"),
    path("students/profile-update/", UpdateProfilePageView.as_view(), name="profile_update"),
    path("students/profile/contracts/<uuid>", VerifyContract.as_view(), name="verify_contract"),
    path("students/profile/contracts/detail/<uuid>", ContractDetailPageView.as_view(), name="contract_detail"),
    path("students/", StudentsListView.as_view(), name="students_list"),
]
