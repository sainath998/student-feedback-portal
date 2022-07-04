from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(roles=[]) :
    def decorator(view) :
        def wrapper(request, *args, **kwargs) :
            print(f"roles={roles}")
            user_group = None

            if request.user.groups.exists() :
                user_group = request.user.groups.all()[0]
            else :
                return redirect('feedback-error')
                # return HttpResponse("You are not allowed to view this page")

            print(f"user_group={user_group}")

            if user_group.name in roles :
                print("decorator success")
                return view(request, *args, **kwargs)
            else :
                print("decorator fail")
                return redirect('feedback-error')
                # return HttpResponse("You are not allowed to view this page")

        return wrapper
    return decorator
    pass
