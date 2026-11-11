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

Los identificadores J-CN corresponden a los casos de caja negra vinculados con los criterios de aceptación.

| Requisito | Historia | Casos de prueba |
| --- | --- | --- |
| R1 · Peso válido | HU-01 | J-CN-01: 50 kg aceptados. J-CN-02: 0 kg rechazados. J-CN-03: 50,01 kg rechazados. |
| R2 · Zona y día válidos | HU-01 | J-CN-04: zona «costera» rechazada. J-CN-05: día 0 rechazado. |
| R3 · Tarifa por peso | HU-02 | J-CN-06: 3 kg en el primer tramo. J-CN-07: 10 kg en el segundo. J-CN-08: 10,5 kg con cobro proporcional. |
| R4 · Recargo por zona | HU-02 | J-CN-06: urbana sin recargo. J-CN-07: rural +25 %. J-CN-08: nacional +50 %. |
| R5 · Fin de semana | HU-03 | J-CN-09: sábado. J-CN-10: domingo. En ambos se suman $2.000 después de los descuentos. |
| R6 · Descuentos | HU-03 | J-CN-09: VIP y ENVIO10, en ese orden. J-CN-10: cliente frecuente, 5 %. |
| R7 · Cupón desconocido | HU-03 | J-CN-10: se ignora el cupón desconocido y se devuelve $12.700. |
| R8 · Mínimo y redondeo | HU-02, HU-03 | J-CN-07: $11.250 suben a $11.300. J-CN-11: $4.590 se ajustan al mínimo de $5.000. |
