from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post
from registration.models import Profile
import pyrebase
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, View

# Create your views here.
config = {
  "apiKey": "AIzaSyB3li7n11UcoQI1x5oCMFmBmF4A2ivq3IQ",
  "authDomain": "crud-8d8c9.firebaseapp.com",
  "databaseURL": "https://crud-8d8c9-default-rtdb.firebaseio.com",
  "projectId": "crud-8d8c9",
  "storageBucket": "crud-8d8c9.appspot.com",
  "messagingSenderId": "488996369608",
  "appId": "1:488996369608:web:b92bb632cf63385dfa21fd"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()



class Homepage(LoginRequiredMixin, ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    ordering = ("-id")
    


class ProfileDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile_details.html"
    ordering = ("-id")



class Profilepage(LoginRequiredMixin, View):
    def get(self, request):
        post = Post.objects.all().order_by("-id")
        return render(request, 'profile.html', {"posts":post})
    


class Newpost(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'new_post.html')

    def post(self, request):
        try:
            # if request.method == "POST":
            title = request.POST["title"]
            desc = request.POST["desc"]
            img = request.FILES["p_img"]
            
            n_post = Post(title=title,desc=desc,p_img=img)
            n_post.user = request.user
            n_post.save()
            messages.success(request, "Post created successfully !")
            return redirect("home")
            # else:
            #     messages.error(request, "Post not created !")
            #     return redirect("new_post")
        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect("new_post")



# def new_post(request):
#     try:
#         if request.method == "GET":
#             return render(request, 'new_post.html')
#         if request.method == "POST":
#             title = request.POST["title"]
#             desc = request.POST["desc"]
#             img = request.FILES["p_img"]
            
#             n_post = Post(title=title,desc=desc,p_img=img)
#             n_post.user = request.user
#             n_post.save()
#             messages.success(request, "Post created successfully !")
#             return redirect("new_post")
#         else:
#             messages.error(request, "Post not created !")
#             return redirect("new_post")
#     except Exception as e:
#         print(e)
#         messages.error(request, e)
#         return redirect("new_post")

    

    
    
    
  