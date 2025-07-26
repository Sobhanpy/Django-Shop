from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Cart(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE, related_name="orders"
    )
    is_paid = models.BooleanField(default=False)
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_price = models.PositiveIntegerField()
    total_discount = models.PositiveIntegerField()
    total_payment = models.PositiveIntegerField()
    cart_hash = models.CharField(max_length=255, default="0")
    cart_pan = models.CharField(max_length=200, default="0")
    ref_id = models.CharField(max_length=30, default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile.user.email} - {self.status}"

    class Meta:
        ordering = ['-created_at']

    def get_items(self):
        return self.items.all()


class OrderItems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey('product.Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=100, default="بدون رنگ")
    guarantee = models.CharField(max_length=50, default="بدون گارانتی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
