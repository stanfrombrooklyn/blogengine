from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True) # Auto generate slug, allow Cyrillic
    return new_slug + '-' + str(int(time())) # to make slug unique add seconds

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    #blank=True because we autogenerate slugs
    slug = models.SlugField(max_length=150, blank=True, unique=True) #human readable url
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): #redefining this to generate slug only once, while creating Post
        # id attr only appears in an instance of Post when it's saved in db
        # при update поста, если оставить поле slug пустым, в бд заносится запись
        # с пустым полем slug, и метод get_absolute_url не может найти пост,
        # ибо они ищутся по slug, а он пустой. корень проблемы в методе save
        # в модели post. метод gen_slug срабатывает только тогда, когда записи
        # post в бд нет, (if not self.id). Т.е. это будет работать только
        # при действии create, а при update в бд уже есть запись и id существует,
        # именно поэтому и не генерируется slug. Эта проверка (if not self.id)
        # не только лишняя (поле slug у нас unique, при попытке создать
        # одинаковый slug нам и так выкинет ошибку), она просто мешает

        #if not self.id:
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})
