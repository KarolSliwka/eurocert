""" Products models """
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from versatileimagefield.fields import VersatileImageField

class Category(models.Model):
    """ Category model """

    class Meta:
        """ Verbose class override """
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    ACTIVE_STATUS = (
        ("True", "Yes"),
        ("False", "No"),
    )

    visible = models.CharField(
        choices=ACTIVE_STATUS,
        verbose_name="Visible",
        max_length=8,
        default="True",
        null=False,
    )

    category = models.SlugField(verbose_name="Category", editable=False, unique=True)
    name = models.CharField(
        verbose_name="Category Name",
        max_length=128,
        null=False,
        blank=False,
        unique=True,
        help_text="Maximum number of chars: 128",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.category = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    """ Product model """

    class Meta:
        """ Verbose class override """
        verbose_name = "Product"
        verbose_name_plural = "Products"

    ACTIVE_STATUS = (
        ("True", "Yes"),
        ("False", "No"),
    )

    id = models.AutoField(primary_key=True)
    image = VersatileImageField(
        verbose_name="Image",
        default="",
        upload_to="media/images/products/",
        null=False,
        blank=False,
        help_text="Size: 1280px/720px, png or jpeg format",
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=225,
        null=False,
        blank=False,
        help_text="Maximum number of chars: 225",
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=1024,
        null=False,
        blank=False,
        help_text="Maximum number of chars: 1024",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False, help_text="Price"
    )
    quantity = models.IntegerField(null=False, blank=False, help_text="Quantity")
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    date_added = models.DateField(
        default=timezone.now, editable=False, verbose_name="Date added"
    )
    visible = models.CharField(
        choices=ACTIVE_STATUS,
        verbose_name="Visible?",
        max_length=8,
        default="True",
        null=False,
    )
    slug = models.SlugField(default='', editable=False,
                            max_length=200, null=False)

    def get_absolute_url(self):
        kwargs = {"pk": self.id, "slug": self.slug}
        return reverse("product", kwargs=kwargs)

    def remove_on_image_update(self):
        try:
            obj = Product.objects.get(id=self.id)
        except Product.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super(Product, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)
