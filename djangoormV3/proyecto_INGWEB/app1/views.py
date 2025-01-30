from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Mueble, Critica  # Importa el modelo de muebles
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm # type: ignore
from django.db.models import Avg, F, ExpressionWrapper, DecimalField
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'index.html')


# Vista de Base :3
@csrf_exempt  # Solo si usas métodos POST, aquí no es necesario, pero lo dejo como referencia
def base(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Verifica si es AJAX
        query = request.GET.get('query', '').strip()  # Obtiene el término de búsqueda
        if query:  # Solo buscar si hay algo en la consulta
            resultados = Mueble.objects.filter(nombre__icontains=query)[:10]  # Filtra los resultados
            datos = [{"id": r.id, "nombre": r.nombre} for r in resultados]  # Serializa los resultados
            return JsonResponse(datos, safe=False)
        else:
            return JsonResponse([], safe=False)  # Devuelve una lista vacía si no hay query
    return JsonResponse({"error": "Solicitud no válida"}, status=400)


# Vista para el catálogo
def catalogo(request):
    # Traer todos los muebles
    muebles = Mueble.objects.all()
    # Para obtener el nombre del usuario si está autenticado
    username = request.user.username if request.user.is_authenticated else None
    # Los 5 mas populares, ordenados por la lógica combinada
    populares = sorted(muebles, key=lambda m: m.calificacion_promedio(), reverse=True)[:5]
    # Obtener el rango de precios desde los parámetros GET
    rango_precio = request.GET.get('rango_precio', None)
    # Filtrar por rango de precios si está presente
    if rango_precio:
        rango = [float(p) for p in rango_precio.split('-')]  # Convertir el rango a valores numéricos
        muebles = muebles.filter(precio_original__gte=rango[0], precio_original__lte=rango[1])
    
    return render(request, 'catalogo.html', {'muebles': muebles, 'username': username, 'populares': populares})



# Vista para los detalles de un mueble
def detalle_mueble(request, mueble_id):
    # Obtén el mueble específico por ID
    mueble = get_object_or_404(Mueble, id=mueble_id)
    
    # Obtén las reseñas asociadas al mueble
    criticas = mueble.criticas.all()  # Usamos el related_name='criticas' del modelo Critica

    if request.method == 'POST':
        # Lógica para manejar las críticas
        comentario = request.POST.get('comentario')
        calificacion = request.POST.get('calificacion')
        
        if comentario and calificacion:
            # Crear y guardar la nueva crítica
            Critica.objects.create(
                mueble=mueble,
                usuario=request.user,
                calificacion=int(calificacion),
                comentario=comentario
            )

            # Redirigir a la misma página para ver la crítica recién agregada
            return redirect('detalle_mueble', mueble_id=mueble.id)

        # Aquí puedes implementar lógica adicional (como agregar al carrito)
        accion = request.POST.get('accion')  # Ejemplo: Identificar qué acción se quiere realizar
        if accion == 'agregar_carrito':
            # Lógica para agregar el mueble al carrito (a implementar)
            pass
        elif accion == 'aumentar_cantidad':
            # Lógica para aumentar cantidad (a implementar)
            pass
        elif accion == 'disminuir_cantidad':
            # Lógica para disminuir cantidad (a implementar)
            pass
        
    # Renderiza la plantilla con el mueble, las reseñas y el formulario para la crítica
    return render(request, 'detalle_mueble.html', {
        'mueble': mueble,
        'criticas': criticas,
    })


@csrf_protect  # Protección CSRF
@require_POST  # Solo permitir POST requests
def toggle_like(request, mueble_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir al login si no está autenticado

    mueble = get_object_or_404(Mueble, id=mueble_id)
    usuario = request.user

    if usuario in mueble.likes.all():
        mueble.likes.remove(usuario)
        mueble.popularidad -= 1
    else:
        mueble.likes.add(usuario)
        mueble.popularidad += 1

    mueble.save()

    # Redirigir a la misma página
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#no usada
def darLike(request, mueble_id):
    post= get_object_or_404(post, id=mueble_id)
    post.likes.add(request.user.id)
    return redirect('/mueble/'+ str(mueble_id))


# Vista para redirigir al admin
def redirigir_admin(request):
    return redirect('/admin/')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('catalogo')  # Redirige al catálogo
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

# Vista para el inicio de sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Inicia sesión
            return redirect('catalogo')  # Redirige al catálogo
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')  # Redirige al inicio de sesión

# Vista para los 3 muves mas destacados 
def index(request):
    # Más popular
    mueble_mas_popular = Mueble.objects.order_by('-popularidad').first()

    # Mejor rankeado
    mueble_mejor_rankeado = (
        Mueble.objects.annotate(promedio_calificacion=Avg('criticas__calificacion'))
        .order_by('-promedio_calificacion')
        .first()
    )

    # Mejor oferta
    mueble_mejor_oferta = (
        Mueble.objects.annotate(
            descuento_monetario=ExpressionWrapper(
                F('precio_original') * F('descuento') / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
        .filter(descuento__isnull=False)
        .order_by('-descuento_monetario')
        .first()
    )
    
    context = {
        'mejor_calificado': mueble_mejor_rankeado,
        'mas_popular': mueble_mas_popular,
        'mejor_oferta': mueble_mejor_oferta,
    }

    return render(request, 'index.html', context) 
