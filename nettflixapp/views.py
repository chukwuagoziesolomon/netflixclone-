from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

@login_required
@require_POST
def add_to_list(request):
    """
    Add a movie or show to the user's list.
    Expects a POST request with 'item_id' in the request body.
    """
    try:
        item_id = request.POST.get('item_id')
        if not item_id:
            return JsonResponse({'status': 'error', 'message': 'Item ID is required'}, status=400)
        
        # Here you would add the item to the user's list in your database
        # For example: UserList.objects.create(user=request.user, item_id=item_id)
        
        return JsonResponse({'status': 'success', 'message': 'Item added to your list'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


