from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Mueble  # Importa el modelo de muebles
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm # type: ignore
from django.db.models import Avg, F, ExpressionWrapper, DecimalField

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Vista para el catálogo
def catalogo(request):
    muebles = Mueble.objects.all()  # Trae todos los muebles de la base de datos
    return render(request, 'catalogo.html', {'muebles': muebles})

# Vista para los detalles de un mueble
def detalle_mueble(request, mueble_id):
    mueble = get_object_or_404(Mueble, id=mueble_id)
    if request.method == 'POST':
        # Aquí puedo implementar lógica para aumentar/disminuir cantidad o agregar al carrito aunque no se como hacer eso XD 
        pass
    return render(request, 'detalle_mueble.html', {'mueble': mueble})

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
     # o esta forma REVISAR ()
    #mueble_mejor_oferta = Mueble.objects.filter(descuento__isnull=False).order_by('-descuento').first()

    context = {
        'mejor_calificado': mueble_mejor_rankeado,
        'mas_popular': mueble_mas_popular,
        'mejor_oferta': mueble_mejor_oferta,
    }

    return render(request, 'index.html', context) 