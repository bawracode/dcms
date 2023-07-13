from eav.models import Value, Entity
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.fields import UUIDField


def get_entity_pk_type(entity_cls) -> str:
    """Returns the entity PK type to use.

    These values map to `models.Value` as potential fields to use to relate
    to the proper entity via the correct PK type.
    """
    if isinstance(entity_cls._meta.pk, UUIDField):
        return 'entity_uuid'
    return 'entity_id'


class ExtendEavValue(Value):
    
    class Meta:
        proxy = True

    language = models.CharField(
        max_length=10,
        default='en',
        blank=True,
        null=True,
        verbose_name=_('Language'),
    )



class ExtendEavEntity(Entity):
    language = settings.LANGUAGE_CODE

    def set_language(self, language):
        self.language = language

    def get_language(self):
        return self.language

    def get_values(self):
        """Get all set :class:`Value` objects for self.instance."""
        entity_filter = {
            'entity_ct': self.ct,
            '{0}'.format(get_entity_pk_type(self.instance)): self.instance.pk,
        }

        try:
            result = ExtendEavValue.objects.filter(**entity_filter, language=self.language).select_related()

            if result.count() == 0:
                result = ExtendEavValue.objects.filter(**entity_filter).select_related()

        except:
            # This is a hack to allow for the fact that the django-eav2
            # Value model does not have a language field, but the
            # django-eav Value model does.
            result = ExtendEavValue.objects.filter(**entity_filter).select_related()

        return result
