# Changelog

Este registro sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [versionado semántico](https://semver.org/lang/es/).

## [Unreleased]

## [2.0.0] - 2026-11-11

### Added

- Suite automatizada de 41 casos para verificar requisitos y ejecutar la regresión.

### Changed

- Se encapsularon los recargos por zona mediante el patrón Strategy.

### Fixed

- Se alineó el mensaje del peso inválido con el requisito.
- Se validan la zona y el día de envío antes de calcular la tarifa.
- El recargo de fin de semana incluye el sábado y se aplica después de los descuentos.
- El importe se redondea al centenar con aritmética decimal.

### Removed

- Se retiró el argumento `flag` de `calc` y la impresión de diagnóstico asociada.

## [1.0.0] - 2026-11-11

### Added

- Implementación heredada del cálculo de envíos, guardada como línea base.

[Unreleased]: https://github.com/Jce-C/parcial-3-ingenieria-de-software/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Jce-C/parcial-3-ingenieria-de-software/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Jce-C/parcial-3-ingenieria-de-software/tree/v1.0.0
