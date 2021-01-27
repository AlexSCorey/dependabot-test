# Generated by Django 2.2.8 on 2020-02-21 16:31

from django.db import migrations, models, connection


def migrate_event_data(apps, schema_editor):
    # see: https://github.com/ansible/awx/issues/9039
    #
    # the goal of this function is to:
    # - [ ] create a parent partition table, main_jobevent_parent
    # - [ ] .. with a single partition
    # - [ ] .. that includes all existing job events
    #
    # the new main_jobevent_parent table should have a new
    # denormalized column, job_created, this is used as a
    # basis for partitioning job event rows
    #
    # The initial partion will be a unique case. After
    # the migration is completed, awx should create
    # new partitions on an hourly basis, as needed.
    # All events for a given job should be placed in
    # a partition based on the job's _created time_.

    # Only partitioning main_jobevent on first pass
    #
    #for tblname in (
    #    'main_jobevent', 'main_inventoryupdateevent',
    #    'main_projectupdateevent', 'main_adhoccommandevent',
    #    'main_systemjobevent'
    #):
    for tblname in ('main_jobevent',):
        with connection.cursor() as cursor:
            # mark existing table as *_old;
            # we will drop this table after its data
            # has been moved over
            cursor.execute(
                f'ALTER TABLE {tblname} RENAME TO {tblname}_old'
            )

            # hacky creation of parent table for partition
            cursor.execute(
                f'CREATE TABLE {tblname} '
                f'(LIKE {tblname}_old, job_created TIMESTAMP WITH TIME ZONE NOT NULL) '
                f'PARTITION BY RANGE(job_created);'
            )

            # .. as well as initial partition containing all existing events
            cursor.execute(
                f'CREATE TABLE {tblname}_part0 '
                f'PARTITION OF {tblname} '
                f'FOR VALUES FROM (\'2000-01-01 00:00:00.000000+00\') to (\'2021-02-01 00:00:00.000000+00\');'
            )

            # copy over all job events into partitioned table
            cursor.execute(
                f'INSERT INTO {tblname} '
                f'SELECT {tblname}_old.*, main_unifiedjob.created '
                f'FROM {tblname}_old '
                f'INNER JOIN main_unifiedjob ON {tblname}_old.job_id = main_unifiedjob.id;'
            )

            # drop old table
            cursor.execute(
                f'DROP TABLE {tblname}_old'
            )
class Migration(migrations.Migration):

    dependencies = [
        ('main', '0123_drop_hg_support'),
    ]

    operations = [
        migrations.RunPython(migrate_event_data),
    ]
