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
from .models import Like, Product,ProductImage, Users, Cart, address, Category,Order,OrderItem
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.views.decorators.csrf import csrf_exempt



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




def product_detail(request, id):
    product = get_object_or_404(Product, product_id=id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'product_details.html', {
        'product': product,
        'images': images
    })


def login_view(request):
    if request.method == "POST":
        identifier = request.POST['email']
        password = request.POST['password'] 
        user = Users.objects.filter(Q(email=identifier) | Q(phone_number=identifier),is_active=1).first()
        if not user:
            messages.error(request, "Email/Phone number is incorrect.", extra_tags='login_id')
            return redirect('login')
        if check_password(password, user.password):
            # --- ADD THIS LOGIC HERE ---
            user.last_login = timezone.now()
            user.save(update_fields=['last_login']) # Only updates this specific column
            # Success! Set session and redirect
            request.session['user_id'] = user.id
            request.session['user_name'] = user.full_name
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
    user_addresses = address.objects.filter(user_id=user_id).order_by('-is_default')
    user = Users.objects.get(pk=user_id)
    return render(request, 'profile.html',{'addresses': user_addresses,"user":user})

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



def dashboard_upload(request):
    categories = Category.objects.all()

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # ---------------------------
        # CATEGORY CREATE
        # ---------------------------
        if form_type == "category":
            name = request.POST.get("category_name")
            image = request.FILES.get("category_image")

            path = None
            if image:
                path = default_storage.save(f"category_images/{image.name}", image)

            Category.objects.create(
                name=name,
                category_image=path,
                created_at=timezone.now()
            )

            return redirect("dashboard_upload")


        # ---------------------------
        # PRODUCT CREATE
        # ---------------------------
        if form_type == "product":

            title = request.POST.get("title")
            description = request.POST.get("description")
            price = request.POST.get("price")
            old_price = request.POST.get("old_price")
            stock = request.POST.get("stock")
            category_id = request.POST.get("category")

            main_image = request.FILES.get("main_image")
            extra_images = request.FILES.getlist("extra_images")

            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                old_price=old_price,
                stock_quantity=stock,
                category_id=category_id
            )

            # main image
            if main_image:
                path = default_storage.save(f"products/{main_image.name}", main_image)
                ProductImage.objects.create(
                    product=product,
                    image_path=path,
                    is_main=True
                )

            # extra images
            for img in extra_images:
                path = default_storage.save(f"products/{img.name}", img)
                ProductImage.objects.create(
                    product=product,
                    image_path=path,
                    is_main=False
                )

            return redirect("dashboard_upload")

    return render(request, "dashboard_upload.html", {"categories": categories})