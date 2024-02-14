from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserForm, ShartnomaForm, CustomUserFormUpdateProfile
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser, Fanlar, Shartnoma, Teachers

# Create your views here.

def about(request):
    return render(request, "education/about.html")


def admission(request):
    return render(request, "education/admission.html")

class RegistrationStudents(View):
    def get(self, request):
        form = CustomUserForm()
        context = {
            "form": form
        }

        return render(request , "education/registration.html", context)
    
    def post(self, request):
        form = CustomUserForm(data=request.POST, files=request.FILES)
        context = {
            "form": form
        }
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request , "education/registration.html", context)

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "education/login.html", {"form": form})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if user.IDNumber:
                return redirect("home")
            else:
                return redirect("profile_update")
        else:
            return render(request, "education/login.html", {"form": form})

class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect("home")
    
class ShartnomaView(LoginRequiredMixin, View):
    def get(self, request):
        form = ShartnomaForm()
        return render(request, "education/shartnoma.html", {"form": form})


from django.db.models import Q

def get_unselected_subjects(student):
    # Talabaning tanlagan fanlarni oldindan olish
    selected_subjects = Shartnoma.objects.filter(talaba=student).values_list('fan', flat=True)

    # Tanlanmagan fanlarni olish
    unselected_subjects = Fanlar.objects.exclude(id__in=selected_subjects)

    return unselected_subjects



class ProfilePageView(LoginRequiredMixin,View):
    def get(self, request):
        student = CustomUser.objects.get(id=request.user.id)
        lessons_list = get_unselected_subjects(student)
        applied_lessons = Shartnoma.objects.all().filter(talaba=request.user)
        applied_lessons_count = applied_lessons.count()
        pending_contracts = Shartnoma.pendings.all()
        verified_contracts = Shartnoma.verified_contracts.all()
        context = {
            "student": request.user,
            "applied_lessons": applied_lessons,
            "lessons_list": lessons_list,
            "pendings": pending_contracts,
            "applied_lessons_count": applied_lessons_count,
            "verified_contracts": verified_contracts
        }

        return render(request, "students/profile.html", context)
    
    def post(self, request):
        course_id = request.POST['course_id']
        course = Fanlar.objects.get(id=course_id)
        contract = Shartnoma.objects.create(
            talaba=request.user,
            fan=course,
            is_active=True
        )

        contract = contract.save()
        return redirect("profile")
    
class UpdateProfilePageView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user_update_form = CustomUserFormUpdateProfile(instance=user)
        return render(request, "students/profile_update.html", {"form": user_update_form})
    
    def post(self, request):
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user_update_form = CustomUserFormUpdateProfile(instance=user, data=request.POST, files=request.FILES)
        if user_update_form.is_valid():
            user_update_form.save()
            return redirect("profile")
        else:
            return render(request, "students/profile_update.html", {"form": user_update_form})

class VerifyContract(LoginRequiredMixin, View):
    def get(self, request, uuid):
        shartnoma_id = uuid
        shartnoma = Shartnoma.objects.get(shartnoma_id=shartnoma_id)
        update_form = ShartnomaForm(instance=shartnoma)
        return render(request, "students/verify_course.html", {"form": update_form, "contract": shartnoma})
    
    def post(self, request, uuid):
        shartnoma_id = uuid
        shartnoma = Shartnoma.objects.get(shartnoma_id=shartnoma_id)
        update_form = ShartnomaForm(instance=shartnoma , data=request.POST, files=request.FILES)
        if update_form.is_valid():
            update_form.save()
            return redirect("profile")
        return render(request, "students/verify_course.html", {"form": update_form, "contract": shartnoma})
    
class ContractDetailPageView(LoginRequiredMixin, View):
    def get(self, request, uuid):
        shartnoma_id = uuid
        shartnoma = Shartnoma.objects.get(shartnoma_id=shartnoma_id)
        return render(request, "students/contract_detail.html", {"contract": shartnoma})
    
class StudentsListView(LoginRequiredMixin, View):
    def get(self, request):
        students = CustomUser.objects.all().filter(is_superuser=False).order_by("-date_joined")
        return render(request, "students/students_list.html", {"students": students})