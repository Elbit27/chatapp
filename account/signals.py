from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache

@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def clear_user_cache(sender, **kwargs):
    cache.delete("user_list")
