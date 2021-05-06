from django.db import models
from tinymce.models import HTMLField
from core.models import SlugModel


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
            self._generate_slug(Category, self.display_name)

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

