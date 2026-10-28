import json
import os
from django.utils import timezone
from django.core.files.storage import default_storage
from sys import exception
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from sqlite3 import Date
from django.contrib import messages  # Correct way to use messages.error
# Remove: from urllib import request (Django provides its own request)
from urllib import request
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Like, Product,ProductImage, Review, Users, Cart, address, Category,Order,OrderItem
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .permissions import staff_required, admin_required
from django.urls import reverse
from decimal import Decimal, InvalidOperation
from django.views.decorators.http import require_POST
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .management.commands.create_admin import generate_password
from django.db.models import Count,Avg
from django.db import transaction
from PIL import Image

@csrf_exempt
def create_cod_order(request):
    if request.method == "POST":
            try:
            # Parse JSON body
                data = json.loads(request.body)
                user_id = data.get("user_id")
                address_id = data.get("address_id")
                cart_items = data.get("cart_items")
                single_product = data.get("product") 
                order_items=[]
                if cart_items:
                    order_items = cart_items
                elif single_product:
                    order_items = [single_product]
                else:
                    return JsonResponse({"status": "error", "message": "No products provided"})
                            # Calculate total amount
                total_amount = 0
                for item in order_items:
                    product = Product.objects.get(pk=item['product_id'])
                    print(product)
                    total_amount += product.price * int(item['quantity'])
                print(total_amount)
                order = Order.objects.create(
                user_id=user_id,
                address_id=address_id,
                total_amount=total_amount,
                payment_method="COD",
                payment_status="Pending"
                    )
                for item in order_items:
                    product = Product.objects.get(pk=item['product_id'])
                    print("hi hello",product)
                    OrderItem.objects.create(
                    order_id=order.pk,        # use integer ID
                    product_id=product.pk,    # use integer ID
                    quantity=int(item['quantity']),
                    price=product.price
                )
                    print(order.id)
                return JsonResponse({"status": "success", "order_id": order.id})
            except Product.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Product not found"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def create_payment(request):
    client = razorpay.Client(auth=("rzp_test_SZnZjwEwJJQcHT", "3TP7OvMwhR5MFZU12kFI9JWF"))

    amount = 50000  # 500.00 rupees (amount in paise)
    print("ok ok ok ")
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "order_id": payment['id'],
        "amount": amount
    })

def orders_history(request):
    user_id = request.session.get("user_id")
    print(user_id)
    orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
    order_details = []
    for order in orders:
        items = OrderItem.objects.filter(order_id=order.id)
        # For each item, fetch product details
        product_items = []
        for item in items:
            product = Product.objects.get(pk=item.product_id)
            main_image = ProductImage.objects.filter(product=product, is_main=True).first()
            product_items.append({
                "title": product.title,
                "price": item.price,
                "quantity": item.quantity,
                "total": item.price * item.quantity,
                "image": main_image.image_path if main_image else None 
            })

        order_details.append({
            "order_id": order.id,
            "total_amount": order.total_amount,
            "payment_method": order.payment_method,
            "payment_status": order.payment_status,
            "created_at": order.created_at,
            "items": product_items
        })
    return render(request,"orders_history.html",{"orders": order_details})

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []

    if query:
        product_results = Product.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:5]
        # products = Product.objects.filter(
        #     name__icontains=query
        # ).values_list('name', flat=True)[:8]
        # Category suggestions
        category_results = Category.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:5]
        suggestions = list(product_results) + list(category_results)
        suggestions = list(dict.fromkeys(suggestions))
        if not suggestions:
            suggestions = ["No matches found"]
    return JsonResponse({'suggestions': suggestions})




def search_products(request):
    query = request.GET.get('q', '').strip()
    print("Query:", query)

    products = []
    categories = []
    user_id = request.session.get("user_id")
    if query:
        # search products
        products = Product.objects.filter(
            title__icontains=query
        ).order_by('-created_at')

        # search categories
        categories = Category.objects.filter(
            name__icontains=query
        )
    liked_ids = []
    cart_ids = []

    if user_id:
        liked_ids = list(
            Like.objects.filter(user_id=user_id)
            .values_list('product_id', flat=True)
        )

        cart_ids = list(
            Cart.objects.filter(user_id=user_id)
            .values_list('product_id', flat=True)
        )
    # attach main image to each product
    for p in products:
        main_img = ProductImage.objects.filter(product=p, is_main=True).first()
        p.image = main_img.image_path if main_img else None

        p.is_liked = p.pk in liked_ids
        p.is_in_cart = p.pk in cart_ids
    context = {
        'products': products,
        'categories': categories,
        'query': query
    }

    return render(request, 'searchbarresults.html', context)

# def search_products(request):
#     print("hi hello")
#     query = request.GET.get('q', '')
#     print(query)
    
#     products = []
#     print(Product.objects.all())
#     if query:
#         products = Product.objects.filter(
#             title=query
#         ).order_by('-created_at')
#         print(products)

#     context = {
#         'products': products,
#         'query': query
#     }

#     return render(request, 'searchbarresults.html', context)


def order_success(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    # Get only the latest order for this user
    latest_order = Order.objects.filter(user_id=user_id).order_by('-created_at').first()
    if not latest_order:
        return redirect("home")  # no order found

    # Get items for this order
    items = OrderItem.objects.filter(order_id=latest_order.id)
    product_items = []

    for item in items:
        product = Product.objects.get(pk=item.product_id)
        main_image = ProductImage.objects.filter(product=product, is_main=True).first()

        product_items.append({
            "title": product.title,
            "category": product.category.name,
            "price": item.price,
            "quantity": item.quantity,
            "total": item.price * item.quantity,
            "image": main_image.image_path if main_image else None
        })

    context = {
        "order": latest_order,
        "items": product_items
    }

    return render(request, "delivery_succes.html", context)





def home(request):
    # Products = Product.objects.all()[]
    Products = Product.objects.all().order_by('-created_at')[:10]
    Categories = Category.objects.all().order_by('-created_at')

    product_data = []
    user_id = request.session.get("user_id")

    liked_ids = []
    cart_ids = []

    if user_id:
        liked_ids = list(
            Like.objects.filter(user_id=user_id)
            .values_list('product_id', flat=True)
        )

        cart_ids = list(
            Cart.objects.filter(user_id=user_id)
            .values_list('product_id', flat=True)
        )

    for product in Products:
        main_image = ProductImage.objects.filter(
            product=product, is_main=True
        ).first()

        product_data.append({
            'id': product.product_id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'old_price': product.old_price,
            'image': main_image.image_path if main_image else None,
            'is_liked': product.product_id in liked_ids,
            'is_in_cart': product.product_id in cart_ids,
        })

    return render(
        request,
        'test1.html',
        {
            'products': product_data,
            'categories': Categories ,
        }
    )




# def product_detail(request, id):
#     product = get_object_or_404(Product, product_id=id)
#     images = ProductImage.objects.filter(product=product)
#     return render(request, 'product_details.html', {
#         'product': product,
#         'images': images,
        
#     })

def product_detail(request, id):
    product = get_object_or_404(Product, product_id=id)
    images = ProductImage.objects.filter(product=product)

    reviews = list(Review.objects.filter(product=product).select_related("user"))
    stats = Review.objects.filter(product=product).aggregate(avg=Avg("rating"), total=Count("review_id"))

    # which reviewers actually bought this product
    order_ids = OrderItem.objects.filter(product_id=product.pk).values_list("order_id", flat=True)
    buyers = set(Order.objects.filter(id__in=order_ids).values_list("user_id", flat=True))
    for r in reviews:
        r.verified = r.user_id in buyers

    user_id = request.session.get("user_id")
    my_review = next((r for r in reviews if r.user_id == user_id), None) if user_id else None

    discount = None
    if product.old_price and product.old_price > product.price:
        discount = int((product.old_price - product.price) * 100 / product.old_price)

    return render(request, 'product_details.html', {
        'product': product, 'images': images,
        'reviews': reviews,
        'avg_rating': round(stats["avg"], 1) if stats["avg"] else None,
        'review_count': stats["total"],
        'my_review': my_review,
        'discount': discount,
    })
    
    
@require_POST
def submit_review(request, product_id):
    user_id = request.session.get("user_id")
    user = Users.objects.filter(pk=user_id, is_active=True).first() if user_id else None
    if not user:
        return redirect("login")

    product = get_object_or_404(Product, pk=product_id)
    back = f"{reverse('product_details', args=[product.pk])}#reviews"

    rating_raw = request.POST.get("rating", "")
    headline = request.POST.get("headline", "").strip()
    comment = request.POST.get("comment", "").strip()

    if not rating_raw.isdigit() or not 1 <= int(rating_raw) <= 5:
        messages.error(request, "Please choose a star rating.")
    elif not headline or len(headline) > 150:
        messages.error(request, "Enter a headline (up to 150 characters).")
    elif not comment or len(comment) > 2000:
        messages.error(request, "Enter your review (up to 2000 characters).")
    else:
        Review.objects.update_or_create(
            user=user, product=product,
            defaults={"rating": int(rating_raw), "headline": headline, "comment": comment},
        )
        messages.success(request, "Thanks! Your review has been saved.")
    return redirect(back)


# def login_view(request):
#     if request.method == "POST":
#         identifier = request.POST['email']
#         password = request.POST['password'] 
#         user = Users.objects.filter(Q(email=identifier) | Q(phone_number=identifier),is_active=1).first()
#         if not user:
#             messages.error(request, "Email/Phone number is incorrect.", extra_tags='login_id')
#             return redirect('login')
#         if check_password(password, user.password):
#             # --- ADD THIS LOGIC HERE ---
#             user.last_login = timezone.now()
#             user.save(update_fields=['last_login']) # Only updates this specific column
#             # Success! Set session and redirect
#             request.session['user_id'] = user.id
#             request.session['user_name'] = user.full_name
#             return redirect('home')
#         else:
#             messages.error(request, "Password is incorrect.", extra_tags='login_pass')
#             return redirect('login')
#     return render(request, 'login_page.html')



def login_view(request):
    if request.method == "POST":
        identifier = request.POST['email'].strip()
        password = request.POST['password']
        user = Users.objects.filter(
            Q(email__iexact=identifier) | Q(phone_number=identifier),
            is_active=True
        ).first()
        if not user:
            messages.error(request, "Email/Phone number is incorrect.", extra_tags='login_id')
            return redirect('login')

        if check_password(password, user.password):
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            request.session.cycle_key()          # new session ID on login
            request.session['user_id'] = user.id
            request.session['user_name'] = user.full_name
            request.session['role'] = user.role   # for showing links only, never for permissions

            if user.must_change_password:
                return redirect('force_password_change')
            if user.role in (Users.ROLE_STAFF, Users.ROLE_ADMIN):
                return redirect('dashboard_upload')   # becomes /dashboard/ in Step 9
            return redirect('home')
        else:
            messages.error(request, "Password is incorrect.", extra_tags='login_pass')
            return redirect('login')
    return render(request, 'login_page.html')







def signup_view(request):
    if request.method == "POST":
        try:
            data=json.loads(request.body)
            full_name = data.get('fullName')
            email = data.get('email')
            phone_number = data.get('phone')
            password = data.get('password')
            print(password)
            hashed_password = make_password(password)
            print(hashed_password)
            date_joined=timezone.now()
            if Users.objects.filter(email=email).exists():
                return JsonResponse({
                    "success": False, 
                    "error": "This email is already registered. Please try logging in."
                }, status=400)
            if Users.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({
                    "success": False, 
                    "error": "This phone number is already linked to another account."
                }, status=400)
            user = Users(full_name=full_name, email=email, phone_number=phone_number, password=hashed_password, date_joined=date_joined)
            user.save()
            return JsonResponse({"success":True,"message": "Account created successfully! Please sign in."}) 
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e),"message": "An error occurred while creating the account."}, status=500)
        

def like_product(request, product_id):
        if request.method == "POST":
            user_id = request.session.get("user_id")

            if not user_id:
                return JsonResponse({"success": False})

        # check if already liked
            like = Like.objects.filter(
                user_id=user_id,
                product_id=product_id
            ).first()

            if like:
            # remove like
                like.delete()
                return JsonResponse({"success": True, "status": "removed"})

            else:
            # add like
                Like.objects.create(
                user_id=user_id,
                product_id=product_id,
                liked_at=timezone.now()
                )
                return JsonResponse({"success": True, "status": "added"})



def add_to_cart(request, product_id):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        print(user_id)
        if not user_id:
            return JsonResponse({"success": False, "error": "User not logged in"}, status=401)
        try:
            # product = Product.objects.get(product_id=product_id)
            data=json.loads(request.body)
            action=data.get('action')
            print(action, product_id, user_id,data)
            # Fetch the user and product instances
            user_instance = Users.objects.get(id=user_id)
            product_instance = get_object_or_404(Product, pk=product_id)
            print(product_instance)
            if action == "add":
                obj, created = Cart.objects.update_or_create(
                    user=user_instance,
                    product=product_instance,
                    defaults={'added_at': timezone.now()} # Update timestamp if re-added
                )
                if not created:
                    obj.quantity += 1
                    obj.save()
                    print("Quantity updated:", obj.quantity)
            elif action == "remove":
                Cart.objects.filter(user=user_instance, product=product_instance).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)




def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('home')

def test_view(request):
    return render(request, 'test1.html')

def profile_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = Users.objects.filter(pk=user_id, is_active=True).first()
    if not user:
        request.session.flush()
        return redirect("login")
    user_addresses = address.objects.filter(user_id=user_id).order_by('-is_default')
    return render(request, 'profile.html', {'addresses': user_addresses, "user": user})


def cart_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')
    
    cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
    for item in cart_items:
        item.main_image = ProductImage.objects.filter(
            product=item.product,
            is_main=True
        ).first()
    return render(request, 'cart.html', {'cart_items': cart_items})

def like_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
         return redirect('login')
    liked_products = Like.objects.filter(user_id=user_id).select_related('product')
    for it in liked_products:
        it.main_image = ProductImage.objects.filter(
            product=it.product,
            is_main=True
        ).first()
    return render(request, 'liked_products.html', {'liked_products': liked_products})

def remove_from_wishlist(request, product_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"success": False})

    Like.objects.filter(
        user_id=user_id,
        product_id=product_id
    ).delete()
    print("deleted")
    return JsonResponse({"success": True})

def remove_from_cart(request, product_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"success": False})

    Cart.objects.filter(
        user_id=user_id,
        product_id=product_id
    ).delete()
    print("removed")

    return JsonResponse({"success": True})

def update_cart_qty(request, product_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"success": False})

    data = json.loads(request.body)
    qty = data.get("quantity")

    Cart.objects.filter(
        user_id=user_id,
        product_id=product_id
    ).update(quantity=qty)

    return JsonResponse({"success": True})



def order_from_cart(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
    user_addresses = address.objects.filter(user_id=user_id).order_by('-is_default')
    price=0
    total_quantity = 0


    for item in cart_items:
        item.main_image = ProductImage.objects.filter(
            product=item.product,
            is_main=True
        ).first()
    price += item.product.price * item.quantity
    total_quantity += item.quantity

    return render(request, 'order.html', {'cart_items': cart_items,'addresses': user_addresses,"product_price":price,'total_quantity': total_quantity})


def buy_now_order(request, product_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect('login')

    # product = Product.objects.get(pk=product_id)
    product = Product.objects.select_related('category').get(pk=product_id)
    user_addresses = address.objects.filter(user_id=user_id).order_by('-is_default')
    
    main_image = ProductImage.objects.filter(
        product=product,
        is_main=True
    ).first()
    price=product.price
    total_quantity=1
    cart_items = [{
        'product': product,
        'quantity': 1,
        'main_image': main_image,
        'category': product.category

    }]

    return render(request, 'order.html', {'cart_items': cart_items,'addresses': user_addresses,"product_price":price,'total_quantity': total_quantity})




def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if query:
        # 1. Search in Categories (High Priority)
        categories = Category.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:2]

        # 2. Search in Products (Title or Description)
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).values_list('title', flat=True)[:4]

        # Combine results: Categories first, then Products
        suggestions = list(categories) + list(products)

    # If no results found in either table
    if not suggestions:
        suggestions = ["No matches found"]

    return JsonResponse({"suggestions": suggestions})



def search_results(request):
    Products = Product.objects.all().order_by('-created_at')
    product_data = []
    user_id = request.session.get("user_id")

    liked_ids = []
    cart_ids = []

    if user_id:
        liked_ids = list(
            Like.objects.filter(user_id=user_id)
            .values_list('product_id', flat=True)
        )

        cart_ids = list(
            Cart.objects.filter(user_id=user_id)
            .values_list('product_id', flat=True)
        )
    for product in Products:
        main_image = ProductImage.objects.filter(
        product=product, is_main=True
        ).first()

        product_data.append({
            'id': product.product_id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'old_price': product.old_price,
            'image': main_image.image_path if main_image else None,
            'is_liked': product.product_id in liked_ids,
            'is_in_cart': product.product_id in cart_ids,
        })
    return render(request, 'searchresults.html', {"products":product_data})


# def load_more_products(request):
#     offset = int(request.GET.get('offset', 0))
#     limit = int(request.GET.get('limit', 10))

#     products = Product.objects.all().order_by('-created_at')[offset:offset+limit]

#     html = render_to_string("partials/product_cards.html", {
#         "products": products
#     })

#     return JsonResponse({
#         "html": html,
#         "has_more": len(products) == limit
#     })
def load_more_products(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))
    print(offset,limit)
    products = Product.objects.all().order_by('-created_at')[offset:offset+limit]

    # attach main image
    for p in products:
        main = ProductImage.objects.filter(product=p, is_main=True).first()
        p.main_image = main.image_path if main else None

    html = render_to_string("partials/product_cards.html", {
        "products": products
    })

    return JsonResponse({
        "html": html,
        "has_more": len(products) == limit
    })



def category_products(request, category_id):
    products = Product.objects.filter(category_id=category_id).order_by('-created_at')
    category = Category.objects.get(pk=category_id)
    user_id = request.session.get("user_id")
    product_data = []
    
    liked_ids = []
    cart_ids = []

    if user_id:
        liked_ids = list(
        Like.objects.filter(user_id=user_id)
        .values_list('product_id', flat=True)
    )

    cart_ids = list(
        Cart.objects.filter(user_id=user_id)
        .values_list('product_id', flat=True)
    )

    for product in products:

        main_image = ProductImage.objects.filter(product=product, is_main=True).first()

        product_data.append({
        'id': product.product_id,
        'title': product.title,
        'description': product.description,
        'price': product.price,
        'old_price': product.old_price,
        'image': main_image.image_path if main_image else None,
        'is_liked': product.product_id in liked_ids,
        'is_in_cart': product.product_id in cart_ids,
    })

    return render(request, "cate_sec_products.html", {
        "products": product_data,"category": category
    })



def save_address(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = request.session.get("user_id")
        print(data)
        address.objects.create(
            user_id=user_id,
            title=data.get("title"),
            address=data.get("address"),
            phone_number=data.get("phone_number"),
            is_default=False
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


# def dashboard_upload(request):
#     categories = Category.objects.all()

#     if request.method == "POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         price = request.POST.get("price")
#         old_price = request.POST.get("old_price")
#         stock = request.POST.get("stock")
#         category_id = request.POST.get("category")

#         main_image = request.FILES.get("main_image")
#         extra_images = request.FILES.getlist("extra_images")

#         product = Product.objects.create(
#             title=title,
#             description=description,
#             price=price,
#             old_price=old_price,
#             stock_quantity=stock,
#             category_id=category_id
#         )

#         # save main image
#         if main_image:
#             path = default_storage.save(f"products/{main_image.name}", main_image)
#             ProductImage.objects.create(
#                 product=product,
#                 image_path=path,
#                 is_main=True
#             )

#         # save extra images
#         for img in extra_images:
#             path = default_storage.save(f"products/{img.name}", img)
#             ProductImage.objects.create(
#                 product=product,
#                 image_path=path,
#                 is_main=False
#             )

#         return redirect("dashboard_upload")

#     return render(request, "dashboard_upload.html", {"categories": categories})



MAX_IMAGE_MB = 5


def _image_error(f):
    """Return an error string if f is not a real image under the size limit, else None."""
    if f.size > MAX_IMAGE_MB * 1024 * 1024:
        return f"'{f.name}' is larger than {MAX_IMAGE_MB} MB."
    try:
        Image.open(f).verify()
    except Exception:
        return f"'{f.name}' is not a valid image."
    finally:
        f.seek(0)
    return None


@staff_required
def dashboard_upload(request):
    categories = Category.objects.all().order_by("name")
    form = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ---------- CATEGORY ----------
        if form_type == "category":
            name = request.POST.get("category_name", "").strip()
            image = request.FILES.get("category_image")

            if not name or len(name) > 100:
                messages.error(request, "Enter a category name (up to 100 characters).")
            elif Category.objects.filter(name__iexact=name).exists():
                messages.error(request, "A category with that name already exists.")
            elif image and _image_error(image):
                messages.error(request, _image_error(image))
            else:
                path = default_storage.save(f"category_images/{image.name}", image) if image else None
                Category.objects.create(name=name, category_image=path, created_at=timezone.now())
                messages.success(request, f"Category '{name}' added.")
                return redirect("dashboard_categories")

        # ---------- PRODUCT ----------
        elif form_type == "product":
            form = request.POST
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            main_image = request.FILES.get("main_image")
            extra_images = request.FILES.getlist("extra_images")
            cat_id = request.POST.get("category", "")
            category = Category.objects.filter(pk=cat_id).first() if cat_id.isdigit() else None
            error = None

            try:
                price = Decimal(request.POST.get("price", ""))
                old_raw = request.POST.get("old_price", "").strip()
                old_price = Decimal(old_raw) if old_raw else None
                stock = int(request.POST.get("stock", ""))
            except (InvalidOperation, ValueError):
                error = "Price, old price and stock must be valid numbers."
            else:
                if not title or len(title) > 255:
                    error = "Enter a title (up to 255 characters)."
                elif not price.is_finite() or price <= 0 or price >= 10**8:
                    error = "Price must be greater than 0."
                elif old_price is not None and (not old_price.is_finite() or old_price <= 0 or old_price >= 10**8):
                    error = "Old price must be greater than 0, or left empty."
                elif stock < 0:
                    error = "Stock can't be negative."
                elif category is None:
                    error = "Choose a category."
                elif main_image is None:
                    error = "A main image is required."
                else:
                    for f in [main_image] + extra_images:
                        error = _image_error(f)
                        if error:
                            break

            if error:
                messages.error(request, error)
            else:
                with transaction.atomic():
                    product = Product.objects.create(
                        title=title, description=description, price=price,
                        old_price=old_price, stock_quantity=stock, category=category,
                    )
                    _save_product_image(product, main_image, True)
                    for f in extra_images:
                        _save_product_image(product, f, False)
                messages.success(request, f"Product '{title}' added.")
                return redirect("dashboard_home")

    return render(request, "dashboard_upload.html", {"categories": categories, "form": form})




def _attach_main_image(products):
    for p in products:
        m = ProductImage.objects.filter(product=p, is_main=True).first()
        p.main_image = m.image_path if m else None
    return products


def _save_product_image(product, f, is_main):
    path = default_storage.save(f"products/{f.name}", f)
    ProductImage.objects.create(product=product, image_path=path, is_main=is_main)


@staff_required
def dashboard_home(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.select_related("category").order_by("-created_at")
    if q:
        qs = qs.filter(title__icontains=q)
    products = _attach_main_image(list(qs))
    return render(request, "dashboard_home.html", {"products": products, "q": q})

@staff_required
def dashboard_product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all().order_by("name")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        try:
            price = Decimal(request.POST.get("price", ""))
            old_raw = request.POST.get("old_price", "").strip()
            old_price = Decimal(old_raw) if old_raw else None
            stock = int(request.POST.get("stock", ""))
        except (InvalidOperation, ValueError):
            messages.error(request, "Price, old price and stock must be valid numbers.")
            return redirect("dashboard_product_edit", product_id=product.pk)

        cat_id = request.POST.get("category", "")
        category = Category.objects.filter(pk=cat_id).first() if cat_id.isdigit() else None
        main_file = request.FILES.get("main_image")
        extra_files = request.FILES.getlist("extra_images")

        if (not title or len(title) > 255 or not price.is_finite() or price <= 0
                or price >= 10**8 or stock < 0 or category is None):
            messages.error(request, "Title, a positive price, stock (0 or more) and a category are required.")
            return redirect("dashboard_product_edit", product_id=product.pk)

        if old_price is not None and (not old_price.is_finite() or old_price <= 0 or old_price >= 10**8):
            messages.error(request, "Old price must be greater than 0, or left empty.")
            return redirect("dashboard_product_edit", product_id=product.pk)

        for f in ([main_file] if main_file else []) + extra_files:
            err = _image_error(f)
            if err:
                messages.error(request, err)
                return redirect("dashboard_product_edit", product_id=product.pk)

        product.title = title
        product.description = description
        product.price = price
        product.old_price = old_price
        product.stock_quantity = stock
        product.category = category
        product.save()

        # replace main image
        if main_file:
            for old in ProductImage.objects.filter(product=product, is_main=True):
                default_storage.delete(old.image_path)
                old.delete()
            _save_product_image(product, main_file, True)

        # remove ticked extra images (never the main one)
        ids = [i for i in request.POST.getlist("delete_images") if i.isdigit()]
        for img in ProductImage.objects.filter(product=product, is_main=False, pk__in=ids):
            default_storage.delete(img.image_path)
            img.delete()

        # add new extra images
        for f in extra_files:
            _save_product_image(product, f, False)

        messages.success(request, "Product updated.")
        return redirect("dashboard_home")

    images = ProductImage.objects.filter(product=product).order_by("-is_main", "id")
    return render(request, "dashboard_product_edit.html",
                  {"product": product, "categories": categories, "images": images})





@staff_required
@require_POST
def dashboard_product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Orders store plain integer IDs and order history loads each product,
    # so deleting an ordered product would break customers' order pages.
    if OrderItem.objects.filter(product_id=product.pk).exists():
        messages.error(request, "This product is in past orders, so it can't be deleted. "
                                "Set its stock to 0 instead.")
        return redirect("dashboard_home")

    for img in ProductImage.objects.filter(product=product):
        default_storage.delete(img.image_path)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect("dashboard_home")



def force_password_change(request):
    user_id = request.session.get("user_id")
    user = Users.objects.filter(pk=user_id, is_active=True).first() if user_id else None
    if not user:
        return redirect('login')
    if not user.must_change_password:
        return redirect('home')

    error = None
    if request.method == "POST":
        new_pw = request.POST.get("new_password", "")
        confirm = request.POST.get("confirm_password", "")
        import re
        if new_pw != confirm:
            error = "Passwords do not match."
        elif check_password(new_pw, user.password):
            error = "New password must be different from the temporary one."
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', new_pw):
            error = "At least 8 characters with a letter, a number and one of @$!%*#?&."
        else:
            user.password = make_password(new_pw)
            user.must_change_password = False
            user.save(update_fields=['password', 'must_change_password'])
            request.session.cycle_key()
            if user.role in (Users.ROLE_STAFF, Users.ROLE_ADMIN):
                return redirect('dashboard_home')
            return redirect('home')
    return render(request, 'force_password_change.html', {'error': error})




@admin_required
def dashboard_staff(request):
    new_credentials = None

    if request.method == "POST":
        name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()

        try:
            validate_email(email)
            email_ok = True
        except ValidationError:
            email_ok = False

        if not name or not email_ok:
            messages.error(request, "Enter a name and a valid email.")
        elif not re.match(r"^[6-9]\d{9}$", phone):
            messages.error(request, "Enter a valid 10-digit phone number.")
        elif Users.objects.filter(email__iexact=email).exists():
            messages.error(request, "That email is already registered.")
        elif Users.objects.filter(phone_number=phone).exists():
            messages.error(request, "That phone number is already registered.")
        else:
            password = generate_password()
            Users.objects.create(
                full_name=name, email=email, phone_number=phone,
                password=make_password(password),
                date_joined=timezone.now(),
                is_active=True,
                role=Users.ROLE_STAFF,          # always staff, never taken from the form
                must_change_password=True,
            )
            # Rendered directly (not via messages) so the password never goes into a cookie.
            new_credentials = {"name": name, "email": email, "password": password}

    team = Users.objects.filter(role__in=[Users.ROLE_STAFF, Users.ROLE_ADMIN]).order_by("role", "full_name")
    return render(request, "dashboard_staff.html", {"team": team, "new_credentials": new_credentials})


@admin_required
@require_POST
def dashboard_staff_toggle(request, user_id):
    target = get_object_or_404(Users, pk=user_id, role__in=[Users.ROLE_STAFF, Users.ROLE_ADMIN])

    if target.pk == request.current_user.pk:
        messages.error(request, "You can't deactivate your own account.")
        return redirect("dashboard_staff")

    if target.role == Users.ROLE_ADMIN and target.is_active:
        if Users.objects.filter(role=Users.ROLE_ADMIN, is_active=True).count() <= 1:
            messages.error(request, "You can't deactivate the last active admin.")
            return redirect("dashboard_staff")

    target.is_active = not target.is_active
    target.save(update_fields=["is_active"])
    messages.success(request, f"{target.full_name} is now {'active' if target.is_active else 'deactivated'}.")
    return redirect("dashboard_staff")


@admin_required
@require_POST
def dashboard_staff_reset(request, user_id):
    target = get_object_or_404(Users, pk=user_id, role=Users.ROLE_STAFF)
    password = generate_password()
    target.password = make_password(password)
    target.must_change_password = True
    target.save(update_fields=["password", "must_change_password"])

    team = Users.objects.filter(role__in=[Users.ROLE_STAFF, Users.ROLE_ADMIN]).order_by("role", "full_name")
    return render(request, "dashboard_staff.html", {
        "team": team,
        "new_credentials": {"name": target.full_name, "email": target.email, "password": password},
    })
    
    
    
@staff_required
def dashboard_categories(request):
    categories = Category.objects.annotate(product_count=Count("product")).order_by("name")
    return render(request, "dashboard_categories.html", {"categories": categories})

@staff_required
def dashboard_category_edit(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        image = request.FILES.get("category_image")

        if not name or len(name) > 100:
            messages.error(request, "Enter a category name (up to 100 characters).")
            return redirect("dashboard_category_edit", category_id=category.pk)
        if Category.objects.filter(name__iexact=name).exclude(pk=category.pk).exists():
            messages.error(request, "Another category already uses that name.")
            return redirect("dashboard_category_edit", category_id=category.pk)
        if image and _image_error(image):
            messages.error(request, _image_error(image))
            return redirect("dashboard_category_edit", category_id=category.pk)

        category.name = name
        if image:
            old = category.category_image.name if category.category_image else None
            category.category_image = default_storage.save(f"category_images/{image.name}", image)
            if old:
                default_storage.delete(old)
        category.save()

        messages.success(request, "Category updated.")
        return redirect("dashboard_categories")

    return render(request, "dashboard_category_edit.html", {"category": category})

@staff_required
@require_POST
def dashboard_category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    count = Product.objects.filter(category=category).count()
    if count:
        messages.error(request, f"'{category.name}' still has {count} product(s). "
                                "Move or delete them first, then delete the category.")
        return redirect("dashboard_categories")

    if category.category_image:
        default_storage.delete(category.category_image.name)
    category.delete()
    messages.success(request, "Category deleted.")
    return redirect("dashboard_categories")



@staff_required
def dashboard_account(request):
    user = request.current_user

    if request.method == "POST":
        action = request.POST.get("action")

        # ---------- PROFILE ----------
        if action == "profile":
            name = request.POST.get("full_name", "").strip()
            phone = request.POST.get("phone", "").strip()

            if not name or len(name) > 100:
                messages.error(request, "Enter a name (up to 100 characters).")
            elif not re.match(r"^[6-9]\d{9}$", phone):
                messages.error(request, "Enter a valid 10-digit phone number.")
            elif Users.objects.filter(phone_number=phone).exclude(pk=user.pk).exists():
                messages.error(request, "That phone number is already used by another account.")
            else:
                user.full_name = name
                user.phone_number = phone
                user.save(update_fields=["full_name", "phone_number"])
                request.session["user_name"] = name
                messages.success(request, "Profile updated.")
                return redirect("dashboard_account")

        # ---------- PASSWORD ----------
        elif action == "password":
            old_pw = request.POST.get("old_password", "")
            new_pw = request.POST.get("new_password", "")
            confirm = request.POST.get("confirm_password", "")

            if not check_password(old_pw, user.password):
                messages.error(request, "Your current password is incorrect.")
            elif new_pw != confirm:
                messages.error(request, "New passwords do not match.")
            elif check_password(new_pw, user.password):
                messages.error(request, "New password must be different from the current one.")
            elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', new_pw):
                messages.error(request, "At least 8 characters with a letter, a number and one of @$!%*#?&.")
            else:
                user.password = make_password(new_pw)
                user.must_change_password = False
                user.save(update_fields=["password", "must_change_password"])
                request.session.cycle_key()
                messages.success(request, "Password changed.")
                return redirect("dashboard_account")

    return render(request, "dashboard_account.html", {"account": user})



@require_POST
def update_profile(request):
    user_id = request.session.get("user_id")
    user = Users.objects.filter(pk=user_id, is_active=True).first() if user_id else None
    if not user:
        return redirect("login")

    name = request.POST.get("full_name", "").strip()
    old_pw = request.POST.get("old_password", "")
    new_pw = request.POST.get("new_password", "")
    confirm = request.POST.get("confirm_password", "")
    changing_pw = bool(old_pw or new_pw or confirm)

    error = None
    if not name or len(name) > 100:
        error = "Enter your name (up to 100 characters)."
    elif changing_pw:
        if not check_password(old_pw, user.password):
            error = "Your current password is incorrect."
        elif new_pw != confirm:
            error = "New passwords do not match."
        elif check_password(new_pw, user.password):
            error = "New password must be different from the current one."
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', new_pw):
            error = "Password needs 8+ characters with a letter, a number and one of @$!%*#?&."

    if error:
        messages.error(request, error)
        return redirect("profile")

    user.full_name = name
    fields = ["full_name"]
    if changing_pw:
        user.password = make_password(new_pw)
        user.must_change_password = False
        fields += ["password", "must_change_password"]
    user.save(update_fields=fields)

    request.session["user_name"] = name
    if changing_pw:
        request.session.cycle_key()
    messages.success(request, "Profile updated.")
    return redirect("profile")




@staff_required
def dashboard_product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related("category"), pk=product_id)
    images = ProductImage.objects.filter(product=product).order_by("-is_main", "id")

    reviews = list(Review.objects.filter(product=product).select_related("user").order_by("-created_at"))
    stats = Review.objects.filter(product=product).aggregate(avg=Avg("rating"), total=Count("review_id"))

    # star breakdown: 5 down to 1
    counts = {i: 0 for i in range(1, 6)}
    for r in reviews:
        counts[r.rating] += 1
    breakdown = [{"star": s, "count": counts[s],
                  "pct": int(counts[s] * 100 / len(reviews)) if reviews else 0}
                 for s in range(5, 0, -1)]

    # mark reviewers who actually bought this product
    order_ids = OrderItem.objects.filter(product_id=product.pk).values_list("order_id", flat=True)
    buyers = set(Order.objects.filter(id__in=order_ids).values_list("user_id", flat=True))
    for r in reviews:
        r.verified = r.user_id in buyers

    return render(request, "dashboard_product_detail.html", {
        "product": product,
        "images": images,
        "reviews": reviews,
        "avg_rating": round(stats["avg"], 1) if stats["avg"] else None,
        "review_count": stats["total"],
        "breakdown": breakdown,
    })


@staff_required
@require_POST
def dashboard_review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    product_id = review.product_id
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect("dashboard_product_detail", product_id=product_id)