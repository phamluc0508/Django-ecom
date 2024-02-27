from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from .models import Cart, CartProduct
from product.models import Product
from decimal import Decimal


def cart_summary(request):
    # Lấy danh sách các sản phẩm trong giỏ hàng
    cart_products = CartProduct.objects.filter(cart__user=request.user)
    
    
    # Tính tổng số tiền của các sản phẩm trong giỏ hàng
    total_price = Decimal(0)
    for product in cart_products:
        price_decimal = Decimal(str(product.product.price))
        total_price += price_decimal * Decimal(product.quantity)
    # total_price = sum(product.product.price * product.quantity for product in cart_products)
    
    context = {
        'cart_products': cart_products,
        'totals': total_price,
    }
    return render(request, 'cart_summary.html', context)

def cart_quantity(request):
    if request.user.is_authenticated:
        # Lấy tổng số lượng sản phẩm trong giỏ hàng của người dùng đăng nhập
        cart_quantity = CartProduct.objects.filter(cart__user=request.user).count()
    else:
        # Nếu người dùng chưa đăng nhập, số lượng sản phẩm trong giỏ hàng là 0
        cart_quantity = 0

    # Trả về số lượng sản phẩm trong giỏ hàng dưới dạng JSON response
    return JsonResponse({'quantity': cart_quantity})

@require_POST
def add_to_cart(request, product_id):
    # Lấy sản phẩm từ ID
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Lấy số lượng từ yêu cầu POST, mặc định là 1 nếu không được chỉ định

    # Kiểm tra xem người dùng đã đăng nhập chưa
    if request.user.is_authenticated:
        user = request.user
        # Kiểm tra xem người dùng đã có giỏ hàng chưa, nếu chưa thì tạo mới
        cart, created = Cart.objects.get_or_create(user=user)
        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa, nếu có thì tăng số lượng, nếu chưa thì tạo mới
        cart_product, product_created = CartProduct.objects.get_or_create(cart=cart, product=product)
        if not product_created:
            # Nếu sản phẩm đã tồn tại trong giỏ hàng, cập nhật số lượng
            cart_product.quantity += quantity
            cart_product.save()
        else:
            # Nếu sản phẩm chưa tồn tại trong giỏ hàng, đặt số lượng mới
            cart_product.quantity = quantity
            cart_product.save()
        return JsonResponse({'success': True})
    else:
        # Nếu người dùng chưa đăng nhập, có thể xử lý theo ý của bạn, ví dụ: trả về một thông báo lỗi
        return JsonResponse({'success': False, 'error': 'User is not authenticated'})


def delete_product(request, product_id):
    # Lấy sản phẩm trong giỏ hàng cần xóa
    cart_product = get_object_or_404(CartProduct, product_id=product_id)
    
    # Xóa sản phẩm khỏi giỏ hàng
    cart_product.delete()

    # Trả về JSON response để cập nhật giao diện người dùng
    return JsonResponse({'success': True})