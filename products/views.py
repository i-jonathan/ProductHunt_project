from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import products
from django.utils import timezone
# Create your views here.
def home(request):
    product = products.objects
    return render(request, 'products/home.html', {'products': product})

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon']:
            product = products()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.image = request.FILES['image']
            product.icon = request.FILES['icon']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.pub_date_pretty = product.pub_date.strftime('%b %e %Y')
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All Fields are Required'})
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(products, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(products, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
