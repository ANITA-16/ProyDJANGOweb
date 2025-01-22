from django.contrib import admin
from .models import Mueble, Imagen, Categoria, Proveedor, Critica

# Configuración de inlines para las imágenes 
class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1


class CriticaInline(admin.TabularInline):  
    model = Critica
    extra = 1  # Número de críticas vacías disponibles para agregar en el formulario
    fields = ('cliente', 'calificacion', 'comentario', 'fecha')  # Campos que deseas mostrar
    readonly_fields = ('fecha',)  # Marcar ciertos campos como solo lectura


# Configuración del modelo Mueble
@admin.register(Mueble)
class MuebleAdmin(admin.ModelAdmin):
    inlines = [ImagenInline,CriticaInline]
    list_display = ('nombre', 'precio_original','descuento', 'get_precio_actual', 'get_calificacion_promedio', 'popularidad','cantidad','disponible')
    list_filter = ('categoria', 'proveedor')
    
    def get_precio_actual(self, obj):
        return obj.precio_actual

    get_precio_actual.short_description = 'Precio Actual'
    
    def get_calificacion_promedio(self, obj):
        return obj.calificacion_promedio

    get_calificacion_promedio.short_description = 'calificacion promedio'

@admin.register(Critica)
class CriticaAdmin(admin.ModelAdmin):
    list_display = ['mueble', 'cliente', 'calificacion', 'fecha']
    list_filter = ['fecha', 'mueble']


# Registro del modelo Proveedor
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto')  # Muestra estas columnas en la tabla
    search_fields = ('nombre', 'contacto')  # Agrega barra de búsqueda

# Registro del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
