# Generated by Django 4.0.4 on 2022-06-03 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_initial'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamwinnermodel',
            name='first',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_first_place', to='authentication.teammodel'),
        ),
        migrations.AddField(
            model_name='teamwinnermodel',
            name='second',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_second_place', to='authentication.teammodel'),
        ),
        migrations.AddField(
            model_name='teamparticipation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_event_participant', to='app.teameventmodel'),
        ),
        migrations.AddField(
            model_name='teamparticipation',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_participant_team', to='authentication.teammodel'),
        ),
        migrations.AddField(
            model_name='teameventrulesmodel',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_event_rules', to='app.teameventmodel'),
        ),
        migrations.AddField(
            model_name='teameventmodel',
            name='organiser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.organisersmodel'),
        ),
        migrations.AddField(
            model_name='solowinnermodel',
            name='event',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.soloeventmodel'),
        ),
        migrations.AddField(
            model_name='solowinnermodel',
            name='first',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solo_first_place', to='authentication.participantsmodel'),
        ),
        migrations.AddField(
            model_name='solowinnermodel',
            name='second',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solo_second_place', to='authentication.participantsmodel'),
        ),
        migrations.AddField(
            model_name='soloparticipation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solo_event_participant', to='app.soloeventmodel'),
        ),
        migrations.AddField(
            model_name='soloparticipation',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_participant', to='authentication.participantsmodel'),
        ),
        migrations.AddField(
            model_name='soloeventrulesmodel',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solo_event_rules', to='app.soloeventmodel'),
        ),
        migrations.AddField(
            model_name='soloeventmodel',
            name='organiser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.organisersmodel'),
        ),
    ]
