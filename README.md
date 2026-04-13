# Global Tech Hub Expansion: Analytics Engineering Roadmap

Este proyecto resuelve el desafío de expansión estratégica corporativa mediante un pipeline de datos E2E. 
Utiliza **Python**, **Snowflake**, y **dbt** para transformar indicadores macroeconómicos en el 
*Global Expansion Opportunity Index*.

## Stack Técnico
- **Data Warehouse:** Snowflake (FinOps optimized)
- **Transformación:** dbt Core (Medallion Architecture)
- **Orquestación:** GitHub Actions (CI/CD)
- **Lenguajes:** SQL & Python

## Estructura del Proyecto
- `/extraction`: Scripts de ingesta de APIs externas (Banco Mundial).
- `/dbt_project`: Modelado de datos profesional (Staging -> Intermediate -> Marts).