# Generated by Django 4.2.8 on 2023-12-20 13:45

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cli', models.CharField(max_length=200)),
                ('telefono_cli', models.IntegerField(blank=True, null=True)),
                ('direccion_cli', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateField()),
                ('cliente_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Farmacia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_farm', models.CharField(max_length=200)),
                ('direccion_farm', models.CharField(max_length=200)),
                ('telefono_farm', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_prod', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('farmacia_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.farmacia')),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_prov', models.CharField(max_length=200)),
                ('direccion_prov', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.PositiveSmallIntegerField(choices=[(1, 'administrador'), (2, 'cliente'), (3, 'empleado'), (4, 'gerente')], default=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('fecha_votacion', models.DateField(default=django.utils.timezone.now)),
                ('comenta_votacion', models.TextField()),
                ('voto_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.cliente')),
                ('voto_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.producto')),
            ],
        ),
        migrations.CreateModel(
            name='SuministroProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_sum', models.DateField(blank=True, null=True)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('costo_ud', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Subscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_sub', models.CharField(max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cliente_sub', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_promo', models.CharField(max_length=100)),
                ('descripcion_promo', models.TextField()),
                ('valor_promo', models.IntegerField(default=0)),
                ('fecha_fin_promo', models.DateField()),
                ('cliente_promo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='prov_sum_prod',
            field=models.ManyToManyField(through='App_Farmacia.SuministroProducto', to='App_Farmacia.proveedor'),
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(choices=[('CA', 'Caixa'), ('BB', 'BBVA'), ('UN', 'UNICAJA'), ('IN', 'ING Direct')], max_length=2)),
                ('cuenta_bancaria', models.CharField(max_length=20)),
                ('fecha_pago', models.DateTimeField(blank=True, null=True)),
                ('cliente_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.cliente')),
                ('subscripcion_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.subscripcion')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_compras', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Gerente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ger', models.CharField(max_length=200)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('fecha_inicio_gestion', models.DateField(null=True)),
                ('gerente_farm', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.farmacia')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salario', models.FloatField(db_column='salario_empleado', default=1020.4)),
                ('farm_emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.farmacia')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_stock', models.IntegerField(default=0)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_prod_comprado', models.IntegerField(blank=True, null=True)),
                ('precio_ud', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.compra')),
                ('producto_detalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DatosFarmacia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('horario', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateField()),
                ('farmacia_datos', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.farmacia')),
            ],
        ),
        migrations.CreateModel(
            name='CuentaEmpleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('contraseña', models.CharField(max_length=50)),
                ('empleado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.empleado')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='empleado_compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Farmacia.empleado'),
        ),
        migrations.AddField(
            model_name='compra',
            name='producto_compra',
            field=models.ManyToManyField(related_name='producto_compra', through='App_Farmacia.DetalleCompra', to='App_Farmacia.producto'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='productos_favoritos',
            field=models.ManyToManyField(related_name='productos_favoritos', to='App_Farmacia.producto'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cliente',
            name='votacion_prod',
            field=models.ManyToManyField(related_name='votacion_prod', through='App_Farmacia.Votacion', to='App_Farmacia.producto'),
        ),
    ]
