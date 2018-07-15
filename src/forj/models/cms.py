from extended_choices import Choices

from easy_thumbnails.fields import ThumbnailerImageField

from django.db import models
from django.utils.functional import cached_property

from forj.db.models import base


class ContentNodeManager(base.Manager):
    def type(self, name):
        return self.filter(type=name).order_by("rank").prefetch_related("covers")


class ContentNode(base.Model):
    TYPE_CHOICES = Choices(
        ("COLLECTION_CAROUSEL", "collection.carousel", "Collection : carrousel"),
        ("COLLECTION_SELECTION", "collection.selection", "Collection : selection"),
        ("HOME_CAROUSEL_TOP", "home.carousel.top", "Accueil : carrousel du haut"),
        ("HOME_CAROUSEL_BOTTOM", "home.carousel.bottom", "Accueil : carrousel du bas"),
        ("HOME_PORTRAIT", "home.portrait", "Accueil : portrait"),
    )

    title = models.CharField(
        max_length=250, verbose_name="Title", null=True, blank=True
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    legend = models.CharField(
        max_length=250, verbose_name="Legend", null=True, blank=True
    )
    cover = ThumbnailerImageField(null=True, blank=True, verbose_name="Cover image")
    product_reference = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Product reference"
    )

    rank = models.IntegerField(verbose_name="Rang", default=0)

    objects = ContentNodeManager()

    class Meta:
        abstract = False
        db_table = "forj_contentnode"

    def __str__(self):
        return "{} > {}".format(self.get_type_display(), self.subject)

    @property
    def subject(self):
        return self.title or "{}...".format(self.description[:100])

    @property
    def product_price(self):
        return self.product.get_price(self.product_reference)

    @cached_property
    def product(self):
        from forj.models import Product

        if self.product_reference:
            product = Product.objects.from_reference(self.product_reference)

            return product

        return None


class ContentNodeCover(base.Model):
    content_node = models.ForeignKey(
        ContentNode, related_name="covers", on_delete=models.CASCADE
    )
    image = ThumbnailerImageField(null=True, blank=True, verbose_name="Cover image")
    rank = models.IntegerField(verbose_name="Rang", default=0)

    class Meta:
        abstract = False
        db_table = "forj_contentnodecover"
