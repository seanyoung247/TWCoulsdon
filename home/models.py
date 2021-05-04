from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

class SlugModel(models.Model):
    """ Exposes methods for slug indexed model """
    slug = models.SlugField(max_length=64, editable=False, null=False, blank=False, unique=True)

    def __generate_slug(self, field):
        """ Generates a URL slug from the event title """
        # Based on code from:
        # https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/

        # Generate a candidate for the slug
        #max_length = self._meta.get_field('slug').max_length
        value = self.title
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        # Ensure that the candidate is unique
        for i in itertools.count(1):
            if not Event.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    class Meta:
        abstract = True


class Category(models.Model):
    """ Defines a page category """
    pass

