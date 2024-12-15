from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Reserva
from .forms import ReservaForm
from .serializers import ReservaSerializer
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def detalle_reserva_html(request, pk=None):
    if pk:
        reserva = get_object_or_404(Reserva, pk=pk)
    else:
        reserva = None

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            if not pk:
                reserva.id = None  # Crear una nueva reserva si no se proporciona un pk
            reserva.save()
            return HttpResponseRedirect(reverse('lista_reservas'))  # Reemplaza con la URL a la que quieres redirigir

    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'detalle_reserva.html', {'form': form, 'reserva': reserva})




@api_view(['GET', 'POST'])
def lista_reservas(request):
    if request.method == 'GET':
        reservas = Reserva.objects.all().order_by('fecha_reserva')
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Función Based View (FBV)
@api_view(['GET', 'PUT', 'DELETE'])
def detalle_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'GET':
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Class-Based Views (CBV)
class ListaReservas(APIView):
    def get(self, request):
        reservas = Reserva.objects.all().order_by('fecha_reserva')
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleReserva(APIView):
    def get_object(self, pk):
        return get_object_or_404(Reserva, pk=pk)

    def get(self, request, pk):
        reserva = self.get_object(pk)
        serializer = ReservaSerializer(reserva)
        return Response(serializer.data)

    def put(self, request, pk):
        reserva = self.get_object(pk)
        serializer = ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reserva = self.get_object(pk)
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

@api_view(['DELETE'])
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.delete()
    return redirect('lista_reservas')