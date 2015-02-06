import settings, os, datetime, cStringIO

from django.db import models
from django.core.files import File
from django.core.management import call_command

from mixins.models import ModifiedDate


class DbMaintenance(ModifiedDate):

    DB_NAMES={(n, n) for n in settings.DATABASES.keys()}

    exported_file = models.FileField(null=False, blank=True, default='', upload_to='backups/%Y/%m/%d')
    imported_file = models.FileField(null=False, blank=True, default='')
    from_db = models.CharField(max_length=25, null=False, blank=True, choices=DB_NAMES, default='default')
    to_db = models.CharField(max_length=25, null=False, blank=True, choices=DB_NAMES)
    backed_up = models.BooleanField(default=True, verbose_name='Back Up First')
    description = models.TextField(blank=True, null=True, default='')

    def save(self, *args, **kwargs):
        if self.imported_file:
            print '==== imported_file [{0}]'.format(self.imported_file)
        if self.backed_up and not self.exported_file:
            self.backup_db()
        return super(DbMaintenance, self).save(*args, **kwargs)

#     def __unicode__(self):
#         return '{0} [{1}]'.format(self.id, self.exported_file)

    def backup_db(self):
        output = cStringIO.StringIO()
        call_command('dumpdata', format='json', indent=2, stdout=output)
        self.exported_file = File(output)
        self.exported_file.name = 'backup-{0}.json'.format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        output.close()

    def restore_db(self):
        self.exported_file = File(output)
        self.exported_file.name = 'backup-{0}.json'.format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        output.close()
        call_command('loaddata', format='json', indent=2, stdout=output)

