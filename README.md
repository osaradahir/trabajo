# GnosisDj
### Detalles de instalación del sistema.

Los siguientes comandos son para:

1. Eliminar migraciones antiguas de actualizaciones anteriores.
##### Nota: El comando podría o no realizar alguna modificación, sea cual sea el resultado continuar con los siguientes pasos.
```python
python manage.py migrate default zero
```

2. Exportar las migraciones de los modelos presentes en la app default.
```python
python manage.py makemigrations default
```

3. Iniciar las migraciones de los modelos hacia la base de datos.
```python
python manage.py migrate
```

3. Iniciar el servidor con la aplicación ejecutandose.
```python
python manage.py runserver
```