# Generated by Django 4.2.7 on 2023-11-16 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_description', models.TextField(null=True)),
                ('restaurant_address', models.TextField(null=True)),
                ('restaurant_city', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_zip', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_state_code', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_country_code', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_longitude', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_latitude', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_email', models.CharField(blank=True, max_length=255, null=True)),
                ('restaurant_logo', models.CharField(blank=True, max_length=255, null=True)),
                ('min_seat', models.IntegerField(null=True)),
                ('max_seat', models.IntegerField(null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantSeatPM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_slot_pm', models.CharField(max_length=550, null=True)),
                ('date_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.restaurantdate')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.restaurantinformation')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantSeatAM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_slot_am', models.CharField(max_length=550, null=True)),
                ('date_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.restaurantdate')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.restaurantinformation')),
            ],
        ),
        migrations.AddField(
            model_name='restaurantdate',
            name='restaurant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.restaurantinformation'),
        ),
    ]
