# Parcial n.º 3 de Ingeniería de Software

**Estudiante:** José Carlos Barreto  
**Código estudiantil:** 0182410032

## Mis parámetros

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 1 | 0 | 0 | 3 | 2 | 50 kg | 3 kg | 10 kg | 25 % | 50 % | 15 % | $2.000 | 0 |

## Parte 1. Requisitos y criterios de aceptación

### Especificación del cálculo del costo

| ID | Regla (con tus valores) |
| --- | --- |
| R1 | El peso debe cumplir 0 < peso ≤ 50 kg. Si no, se lanza el error “peso inválido”. |
| R2 | Si la zona no es una de las tres válidas, o el día no está entre 1 y 7, se lanza un error. |
| R3 | Tarifa base. Tramo 1 (peso ≤ 3 kg): $6.000. Tramo 2 (hasta 10 kg, inclusive): $9.000. Más de 10 kg: $9.000 + $800 por cada kg sobre 10 kg, de forma proporcional. |
| R4 | Recargo por zona. Rural: +25 %. Nacional: +50 %. Urbana: sin recargo. |
| R5 | Fin de semana (sábado y domingo): +$2.000, después de los descuentos. |
| R6 | Descuento de cliente. Frecuente: 5 %. VIP: 15 %. Cupón ENVIO10: 10 %. Si hay los dos, se aplican ambos: primero el del cliente y luego el cupón. |
| R7 | Un cupón que no existe se ignora. |
| R8 | El costo nunca es menor que $5.000. El resultado se redondea al múltiplo de $100 más cercano; los $50 redondean hacia arriba. |

### Historias de usuario y criterios de aceptación

#### HU-01. Validar los datos de la cotización

Como auxiliar de recepción, quiero validar el peso, la zona y el día del envío para detectar datos incorrectos antes de comunicar un precio.

| DADO | CUANDO | ENTONCES |
| --- | --- | --- |
| Un envío urbano de 50 kg, para un cliente normal, el día 3 y sin cupón. Se considera también cada variante por separado: peso de 0 o 50,01 kg, zona «costera» o día 0. | El auxiliar solicita una cotización para el envío original y para cada variante. | El envío original se acepta y cuesta $41.000. Un peso de 0 o 50,01 kg genera el error «peso inválido» (R1). La zona «costera» y el día 0 generan un error por el dato inválido (R2). |

#### HU-02. Calcular la tarifa por peso y destino

Como asesor de envíos, quiero calcular la tarifa según el tramo de peso y la zona de destino para poder explicar el precio al cliente.

| DADO | CUANDO | ENTONCES |
| --- | --- | --- |
| Tres envíos para clientes normales, el día 4 y sin cupón: urbano de 3 kg, rural de 10 kg y nacional de 10,5 kg. | El asesor cotiza cada envío. | Urbano: 3 kg aún pertenece al primer tramo y cuesta $6.000. Rural: $9.000 más 25 % da $11.250, que se redondea a $11.300. Nacional: $9.400 de base más 50 % da $14.100 (R3, R4, R8). |

#### HU-03. Aplicar descuentos y recargos al total

Como cliente de EnvíaYa, quiero que la cotización aplique mis descuentos y el recargo de fin de semana en el orden correcto para conocer el importe final.

| DADO | CUANDO | ENTONCES |
| --- | --- | --- |
| Tres envíos: rural de 4 kg, VIP, sábado y ENVIO10; rural de 4 kg, frecuente, domingo y cupón desconocido; urbano de 2 kg, VIP, día 3 y ENVIO10. | El cliente confirma los datos y solicita el total de cada envío. | En el primero se descuenta 15 % y luego 10 %. Se suman $2.000 y el total redondeado es $10.600. En el segundo se aplica 5 %, se ignora el cupón y se suman $2.000 al final. El total es $12.700. En el tercero, los descuentos dejan $4.590 y se cobra el mínimo de $5.000 (R5–R8). |

### Matriz de trazabilidad

Los códigos CN identifican los casos de caja negra vinculados con los criterios de aceptación.

| Requisito | Historia | Casos de prueba |
| --- | --- | --- |
| R1 · Peso válido | HU-01 | CN-01: 50 kg aceptados. CN-02: 0 kg rechazados. CN-03: 50,01 kg rechazados. |
| R2 · Zona y día válidos | HU-01 | CN-04: zona «costera» rechazada. CN-05: día 0 rechazado. |
| R3 · Tarifa por peso | HU-02 | CN-06: 3 kg en el primer tramo. CN-07: 10 kg en el segundo. CN-08: 10,5 kg con cobro proporcional. |
| R4 · Recargo por zona | HU-02 | CN-06: urbana sin recargo. CN-07: rural +25 %. CN-08: nacional +50 %. |
| R5 · Fin de semana | HU-03 | CN-09: sábado. CN-10: domingo. En ambos se suman $2.000 después de los descuentos. |
| R6 · Descuentos | HU-03 | CN-09: VIP y ENVIO10, en ese orden. CN-10: cliente frecuente, 5 %. |
| R7 · Cupón desconocido | HU-03 | CN-10: se ignora el cupón desconocido y se devuelve $12.700. |
| R8 · Mínimo y redondeo | HU-02, HU-03 | CN-07: $11.250 suben a $11.300. CN-11: $4.590 se ajustan al mínimo de $5.000. |

## Parte 2. Plan de pruebas

### 2.1 Alcance

Verificar el cotizador de EnvíaYa frente a R1–R8: validación del peso, la zona y el día; tarifas por tramo y destino; descuentos, cupón, recargo de fin de semana, mínimo y redondeo. Se evaluará el comportamiento del código heredado `v1.0.0` y se repetirá la suite después de las correcciones.

### 2.2 Niveles de prueba

**Unidad.** Ejecutar `calc` con entradas controladas. Verificar, por ejemplo, que 3 kg permanezcan en el primer tramo y que $11.250 se redondeen a $11.300.

**Integración.** Comprobar la interacción entre tarifa base, recargo rural, descuento VIP, `ENVIO10` y recargo del sábado. Tras la refactorización, verificar que las funciones extraídas mantengan ese orden al trabajar juntas.

**Sistema.** Ejecutar el cotizador completo desde su entrada pública con solicitudes válidas e inválidas. Comprobar el importe final o el error que corresponda a cada solicitud.

**Aceptación.** Ejecutar los criterios de HU-01 a HU-03 y registrar el resultado con su ID de prueba. Incluir un cupón desconocido y verificar que se ignore y se devuelva el total.

### 2.3 Estrategia, ambiente y roles

Diseñar al menos 20 casos de caja negra a partir de particiones, valores límite y una tabla de decisión. Justificar al menos cinco resultados con cálculos manuales. Diseñar los casos de caja blanca a partir del grafo de `calc` y relacionar las pruebas con la matriz de trazabilidad. Automatizar la ejecución, registrar defectos y repetir la suite en la versión corregida.

**Ambiente.** Python 3 en Windows, terminal PowerShell, entorno virtual, pytest, pytest-cov y Git. Registrar la versión de las herramientas y el commit evaluado junto con cada evidencia.

**Roles.** Análisis de pruebas: diseña los casos y calcula los resultados esperados. Ejecución: automatiza, ejecuta y conserva las evidencias. Mantenimiento: corrige los defectos y revisa la regresión.

### 2.4 Riesgos y mitigaciones

Error al clasificar el peso. Probar valores inferiores, iguales y superiores a los límites, con énfasis en 3 kg y 10 kg.

Redondeo anticipado u orden incorrecto de descuentos. Conservar los subtotales del cálculo manual y verificar un empate de $50 y un envío con descuento y recargo de fin de semana.

Pérdida de la evidencia inicial. Ejecutar y guardar los resultados de la versión heredada antes de incorporar las correcciones.

### 2.5 Criterios de entrada y salida

**Entrada.** Especificación R1–R8 y parámetros revisados, versión `v1.0.0` identificada, ambiente listo y casos con entradas y resultados esperados definidos para la ejecución.

**Salida.** Casos ejecutados y trazados, defectos reproducibles documentados, y regresión aprobada en la versión corregida. Guardar capturas y registrar el porcentaje de casos aprobados, los defectos por severidad, su densidad y la cobertura de sentencias y de ramas. Comparar ambas coberturas entre versiones.

## Parte 3. Diseño de casos de caja negra

El diseño usa la especificación R1–R8 y reúne 26 casos. Los resultados de la matriz son los valores esperados que se verificarán al ejecutar las pruebas.

### 3.1 Particiones de equivalencia

Una partición agrupa entradas que reciben el mismo tratamiento. La tabla identifica las clases de cada dato de la cotización.

| Entrada | Clases válidas | Clases inválidas o tratamiento especial |
| --- | --- | --- |
| Peso (kg) | 0 < p ≤ 3; 3 < p ≤ 10; 10 < p ≤ 50. | p ≤ 0 y p > 50. Se devuelve «peso inválido». |
| Zona | Urbana, rural y nacional. Cada zona tiene un recargo distinto. | Zona fuera del catálogo. Se devuelve un error de zona. |
| Cliente | Normal, frecuente y VIP. Cada tipo tiene un descuento propio. | Tipo fuera del catálogo. La especificación no define qué respuesta debe producir. |
| Día | Enteros del 1 al 5, sábado (6) y domingo (7). | Entero menor que 1 o mayor que 7. Se devuelve un error de día. Los valores no enteros quedan fuera del dominio descrito. |
| Cupón | Ausente o ENVIO10. | Código desconocido. Se ignora y se calcula como si estuviera ausente. |

### 3.2 Valores límite de peso

Se usa un paso de 0,01 kg para comparar cada límite con sus vecinos. El peso de 3 kg se cobra en el primer tramo. A 10,01 kg la base aumenta \$8, aunque el total urbano siga siendo \$9.000 tras redondear. CN-08 permite observar un incremento proporcional en el resultado final.

| Límite | Por debajo | En el límite | Por encima |
| --- | --- | --- | --- |
| 0 kg | −0,01 kg · CN-12 | 0 kg · CN-02 | 0,01 kg · CN-13 |
| 3 kg (L1) | 2,99 kg · CN-14 | 3 kg · CN-06 | 3,01 kg · CN-15 |
| 10 kg (L2) | 9,99 kg · CN-16 | 10 kg · CN-26 | 10,01 kg · CN-17 |
| 50 kg (PMAX) | 49,99 kg · CN-18 | 50 kg · CN-01 | 50,01 kg · CN-03 |

### 3.3 Tabla de decisión

A representa la tarifa base con el recargo de zona aplicado. Cada fila cubre dos situaciones, día hábil y fin de semana. Las multiplicaciones se aplican de izquierda a derecha. Después del importe indicado se aplica el mínimo de \$5.000 y el redondeo a \$100. Un cupón desconocido se trata como ausente.

| Cliente | Cupón | Días 1–5 | Días 6–7 |
| --- | --- | --- | --- |
| Normal | Ausente | A | A + \$2.000 |
| Normal | ENVIO10 | A × 0,90 | A × 0,90 + \$2.000 |
| Normal | Desconocido | A | A + \$2.000 |
| Frecuente | Ausente | A × 0,95 | A × 0,95 + \$2.000 |
| Frecuente | ENVIO10 | A × 0,95 × 0,90 | A × 0,95 × 0,90 + \$2.000 |
| Frecuente | Desconocido | A × 0,95 | A × 0,95 + \$2.000 |
| VIP | Ausente | A × 0,85 | A × 0,85 + \$2.000 |
| VIP | ENVIO10 | A × 0,85 × 0,90 | A × 0,85 × 0,90 + \$2.000 |
| VIP | Desconocido | A × 0,85 | A × 0,85 + \$2.000 |

### 3.4 Matriz de casos de prueba

Cada fila muestra las entradas en orden de peso, zona, cliente, día y cupón. El resultado esperado se deriva de R1–R8. La columna «Técnica» indica la técnica principal que originó el caso.

| ID | Requisito | Entradas | Resultado esperado | Técnica |
| --- | --- | --- | --- | --- |
| CN-01 | R1, R3 | 50 kg · Urbana · Normal · día 3 · sin cupón | \$41.000 | Límite |
| CN-02 | R1 | 0 kg · Urbana · Normal · día 3 · sin cupón | Error «peso inválido» | Límite |
| CN-03 | R1 | 50,01 kg · Urbana · Normal · día 3 · sin cupón | Error «peso inválido» | Límite |
| CN-04 | R2 | 2 kg · «costera» · Normal · día 3 · sin cupón | Error de zona | Partición |
| CN-05 | R2 | 2 kg · Rural · Normal · día 0 · sin cupón | Error de día | Límite |
| CN-06 | R3, R4 | 3 kg · Urbana · Normal · día 4 · sin cupón | \$6.000 | Límite |
| CN-07 | R3, R4, R8 | 10 kg · Rural · Normal · día 4 · sin cupón | \$11.300 | Límite |
| CN-08 | R3, R4 | 10,5 kg · Nacional · Normal · día 4 · sin cupón | \$14.100 | Partición |
| CN-09 | R4–R6, R8 | 4 kg · Rural · VIP · día 6 · ENVIO10 | \$10.600 | Decisión |
| CN-10 | R5–R8 | 4 kg · Rural · Frecuente · día 7 · OTRO | \$12.700 | Decisión |
| CN-11 | R6, R8 | 2 kg · Urbana · VIP · día 3 · ENVIO10 | \$5.000 | Decisión |
| CN-12 | R1 | -0,01 kg · Urbana · Normal · día 3 · sin cupón | Error «peso inválido» | Límite |
| CN-13 | R1, R3 | 0,01 kg · Urbana · Normal · día 3 · sin cupón | \$6.000 | Límite |
| CN-14 | R3 | 2,99 kg · Urbana · Normal · día 4 · sin cupón | \$6.000 | Límite |
| CN-15 | R3 | 3,01 kg · Urbana · Normal · día 4 · sin cupón | \$9.000 | Límite |
| CN-16 | R3 | 9,99 kg · Urbana · Normal · día 4 · sin cupón | \$9.000 | Límite |
| CN-17 | R3, R8 | 10,01 kg · Urbana · Normal · día 4 · sin cupón | \$9.000 | Límite |
| CN-18 | R1, R3, R8 | 49,99 kg · Urbana · Normal · día 3 · sin cupón | \$41.000 | Límite |
| CN-19 | R2, R5 | 4 kg · Urbana · Normal · día 5 · sin cupón | \$9.000 | Límite |
| CN-20 | R2, R5 | 4 kg · Urbana · Normal · día 6 · sin cupón | \$11.000 | Límite |
| CN-21 | R6, R8 | 4 kg · Urbana · VIP · día 4 · sin cupón | \$7.700 | Partición |
| CN-22 | R2 | 4 kg · Urbana · Normal · día 8 · sin cupón | Error de día | Límite |
| CN-23 | R2, R5 | 4 kg · Urbana · Normal · día 1 · sin cupón | \$9.000 | Límite |
| CN-24 | R5–R8 | 4 kg · Rural · Frecuente · día 7 · sin cupón | \$12.700 | Decisión |
| CN-25 | R6 | 4 kg · Urbana · Normal · día 4 · ENVIO10 | \$8.100 | Decisión |
| CN-26 | R3 | 10 kg · Urbana · Normal · día 4 · sin cupón | \$9.000 | Límite |

### 3.5 Cálculo de resultados esperados

**CN-06.** El peso de 3 kg pertenece al primer tramo. La base es \$6.000. Como la zona es urbana, el cliente es normal y el día es hábil, no se aplican ajustes. El mínimo y el redondeo dejan el total en \$6.000.

**CN-07.** 10 kg pertenece al segundo tramo, con base de \$9.000. Zona rural: \$9.000 × 1,25 = \$11.250. Sin otros ajustes, el importe queda justo a mitad entre \$11.200 y \$11.300. Se redondea hacia arriba a \$11.300.

**CN-08.** El exceso es 10,5 − 10 = 0,5 kg. Base: \$9.000 + 0,5 × \$800 = \$9.400. Zona nacional: \$9.400 × 1,50 = \$14.100. El total queda en \$14.100.

**CN-09.** Base de \$9.000. Zona rural: \$9.000 × 1,25 = \$11.250. VIP: \$11.250 × 0,85 = \$9.562,50. ENVIO10: \$9.562,50 × 0,90 = \$8.606,25. Sábado: \$8.606,25 + \$2.000 = \$10.606,25. Total redondeado: \$10.600.

**CN-10.** Base de \$9.000 y recargo rural de 25 %: \$11.250. Cliente frecuente: \$11.250 × 0,95 = \$10.687,50. El cupón OTRO se ignora. Domingo: \$10.687,50 + \$2.000 = \$12.687,50. Total redondeado: \$12.700.

**CN-11.** Base urbana de \$6.000. VIP: \$6.000 × 0,85 = \$5.100. ENVIO10: \$5.100 × 0,90 = \$4.590. Al aplicar el mínimo se obtienen \$5.000, que ya es múltiplo de \$100.
