# Generated by Django 4.1.2 on 2022-10-16 16:41

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Institute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("scientific_field", models.CharField(max_length=50)),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("courses", models.ManyToManyField(to="usr_cabinet.course")),
            ],
            options={
                "ordering": ["last_name"],
                "abstract": False,
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "institute",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="students",
                        to="usr_cabinet.institute",
                    ),
                ),
            ],
            options={
                "ordering": ["last_name"],
                "abstract": False,
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="related_institute",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="courses",
                to="usr_cabinet.institute",
            ),
        ),
    ]
