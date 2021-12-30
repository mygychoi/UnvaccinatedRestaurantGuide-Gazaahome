# Generated by Django 3.2.9 on 2021-12-30 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hitcount.models
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('content', markdownx.models.MarkdownxField()),
                ('head_image', models.ImageField(blank=True, upload_to='corona/post/images/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_anonymous', models.BooleanField(default=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corona_post_author', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'PostCategories',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('address', models.CharField(help_text='<a href="https://map.naver.com/v5/" class="text-decoration-none small" target="_blank">\n        <img src="https://res.cloudinary.com/hyzq6bxmk/image/upload/v1640650504/static/corona/naver_map_yc6xld.png" \n        style="width: 20px; height: 20px">\n        네이버 지도에서 알아보기\n    </a>', max_length=200, null=True)),
                ('region', models.CharField(blank=True, max_length=10, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('verifieded', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='RestaurantCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'RestaurantCategories',
            },
        ),
        migrations.CreateModel(
            name='RestaurantTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnvaccinatedPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantDeleteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='corona/restaurant/comments/%Y/%m/%d/')),
                ('content', models.TextField()),
                ('is_anonymous', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='restaurant_comment_likers', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='category',
            field=models.ForeignKey(help_text='PCR 음성 필요 여부는 <태그>를 통해 작성해주시면 감사하겠습니다.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corona.restaurantcategory'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='restaurant_dislikers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='restaurant_likers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corona.RestaurantTag'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='unvaccinated_pass',
            field=models.ForeignKey(help_text='이용가능 여부가 궁금하시면 <궁금>으로 설정해주세요', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corona.unvaccinatedpass'),
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('is_anonymous', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='post_comment_likers', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='corona.postcategory'),
        ),
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='post_dislikers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FastRestaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('verifieded', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(max_length=20)),
                ('tags', models.CharField(blank=True, max_length=50)),
                ('unvaccinated_pass', models.CharField(max_length=20)),
                ('num_likes', models.IntegerField(default=0)),
                ('num_dislikes', models.IntegerField(default=0)),
                ('num_comments', models.IntegerField(default=0)),
                ('num_hits', models.IntegerField(default=1)),
                ('base', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='corona.restaurant')),
            ],
        ),
    ]
