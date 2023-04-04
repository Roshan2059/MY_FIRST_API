from django.db import models

class product(models.Model):
    design_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    usage_of_material = models.TextField()
    sewing_wages = models.DecimalField(max_digits=10, decimal_places=2)
    master_charge = models.DecimalField(max_digits=10, decimal_places=2)
    washing_charges = models.DecimalField(max_digits=10, decimal_places=2)
    button_charges = models.DecimalField(max_digits=10, decimal_places=2)
    packing_charges = models.DecimalField(max_digits=10, decimal_places=2)
    zipper_charges = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    thumbnail = models.ImageField(upload_to='product_thumbnails')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name