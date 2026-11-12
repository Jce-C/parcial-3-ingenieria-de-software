# Notas de versión · v2.0.0

Esta versión corrige la validación de peso, zona y día, así como el orden del recargo y el redondeo final. Los cupones desconocidos se ignoran según el requisito de esta versión.

## Migración de llamadas

Retire `flag` de las llamadas existentes. Para mostrar el costo, use el importe que devuelve `calc`.

```python
# v1.0.0
total = calc(p, z, c, d, cup, flag=True)

# v2.0.0
total = calc(p, z, c, d, cup)
```

## Verificación

La regresión de la Parte 6 registró 41 de 41 pruebas aprobadas y 100 % de cobertura de ramas de envios.py. El detalle de los cambios está en [CHANGELOG.md](CHANGELOG.md).
