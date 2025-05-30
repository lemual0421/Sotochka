# Generated by Django 5.2 on 2025-05-02 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0004_alter_task_content"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["order"]},
        ),
        migrations.AlterField(
            model_name="task",
            name="order",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name="task",
            unique_together={("subject", "order")},
        ),
    ]
