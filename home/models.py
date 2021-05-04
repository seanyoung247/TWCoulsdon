import itertools
from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField


class SlugModel(models.Model):
    """ Exposes methods for slug indexing models """
    class Meta:
        abstract = True

    slug = models.SlugField(max_length=64, editable=False, null=False, blank=False, unique=True)

    def _generate_slug(self, model, field):
        """ Generates a URL slug from the event title """
        # Based on code from:
        # https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/

        # Generate a candidate for the slug
        #max_length = self._meta.get_field('slug').max_length
        value = field
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        # Ensure that the candidate is unique
        for i in itertools.count(1):
            if not model.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate


class Category(SlugModel):
    """ Defines a page category """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    title_page = models.ForeignKey('Page', related_name='+',
        null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def get_display_name(self):
        """ Returns the Category's display name """
        return self.display_name

    def save(self, *args, **kwargs):
        # Do we need to generate a slug?
        if not self.pk:
            self._generate_slug(Category, self.name)

        super().save(*args, **kwargs)


class Page(SlugModel):
    """ Defines a page of content """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    content = HTMLField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Do we need to generate a slug?
        if not self.pk:
            self._generate_slug(Page, self.title)

        super().save(*args, **kwargs)

