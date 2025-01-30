from django.db import models
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User

def catalogo(request):
    muebles = Mueble.objects.prefetch_related('imagen_set').all()
    return render(request, 'catalogo.html', {'muebles': muebles})

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'Categoria'

    def __str__(self):
       return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=50) #se puede separar y poner telefono y correo, se entiende que solo se va a poner uno de los dos aqui

    class Meta:
        db_table = 'Proveedor'

    def __str__(self):
        return self.nombre


# modelo de RESEÑAS 
class Critica (models.Model):
    mueble = models.ForeignKey('Mueble', on_delete=models.CASCADE, related_name='criticas')  # Relación con el modelo Mueble
     # Relación con el usuario que realiza la reseña
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    #cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)  # Relación con el cliente que realiza la reseña
    calificacion = models.PositiveIntegerField()  # Calificación del cliente (e.g., de 1 a 5)
    comentario = models.TextField(null=True, blank=True)  # Comentario del cliente
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha en la que se crea la reseña

    class Meta:
        db_table = 'Critica'
        ordering = ['-fecha']  # Las reseñas más recientes primero

    
    def __str__(self):
        return f'Crítica de {self.usuario.username} para {self.mueble.nombre}'

# Modelo de MUEBLES
class Mueble(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_original = models.DecimalField(max_digits=10, decimal_places=2)  # Precio sin descuento
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Descuento explícito (en %)
    disponible = models.BooleanField(default=True)
    cantidad = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    popularidad = models.PositiveIntegerField(default=0)  # Número de "me gusta"
    likes = models.ManyToManyField(User, related_name='mueble_likes', blank=True)  # Relación de "Me gusta"
    class Meta:
        db_table = 'Mueble'

    def __str__(self):
        return self.nombre

    @property
    def precio_actual(self):
        """
        Calcular el precio actual basado en el precio original y el descuento.
        """
        if self.descuento:
            return round(self.precio_original * (1 - (self.descuento / 100)), 2)
        return self.precio_original

    def valor_descuento(self):
        """
        Calcular el descuento en dinero.
        """
        return self.precio_original - self.precio_actual

    def calificacion_promedio(self):
        """
        Calcula el promedio de calificaciones de las críticas asociadas.
        """
        criticas = self.criticas.all()
        if criticas.exists():
            return round(sum(critica.calificacion for critica in criticas) / criticas.count(), 2)
        return 0.0


# Modelo Imagen
class Imagen(models.Model):
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    imagenURL = models.URLField()

    class Meta:
        db_table = 'Imagen'

    def __str__(self):
        return f"Imagen para {self.mueble.nombre}"


# Modelo Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombre


# Modelo Venta
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Venta'

    def __str__(self):
        return f"Venta {self.id}"


# Modelo DetalleVenta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'DetalleVenta'

    def __str__(self):
        return f"Detalle de Venta {self.id}"