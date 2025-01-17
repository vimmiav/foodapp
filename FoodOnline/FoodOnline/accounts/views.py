from django.shortcuts import render,redirect

# Create your views here.
from .forms import UserForm
from vendor.forms import VendorForm

from .models import User
from django.contrib import messages



def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # # Hash password before saving it into database
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()


            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,"Your account has been registered sucessfully")
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context ={
        'form': form,
    }
    return render(request,'accounts/registerUser.html',context)



def registerVendor(request):
    form = UserForm()
    v_form = VendorForm()

    context={
        'form':form,
        'v_form':v_form

    }

    return render(request,'accounts/registerVendor.html',context)
