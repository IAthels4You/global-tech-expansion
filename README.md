# Global Tech Hub Expansion: Opportunity Index Pipeline

This project implements an industrial-grade Analytics Engineering architecture to mitigate financial risk in the opening of new Tech Hubs. The system automates the data flow from official sources (World Bank, UNESCO, OECD) to the consolidation of a single decision-making metric: the **Global Expansion Opportunity Index**.

## Executive Summary
The pipeline resolves international data inconsistency through the application of **Data Contracts** and **Semantic Governance**. It enables executive leadership to compare jurisdictions under homogeneous accounting and talent criteria, using validated indicators such as the Tax Wedge (OECD) and the ISCED 5-8 educational standard (UNESCO).

## Technical Stack
* **Cloud Data Warehouse:** Snowflake (Multi-cluster Architecture and FinOps).
* **Data Transformation:** dbt Core (Medallion Architecture: Raw, Staging, Intermediate, Analytics).
* **Data Ingestion:** Python (Custom connectors for SDMX-JSON APIs).
* **Validation:** Pydantic (Data Contracts) and dbt_expectations (Data Quality).
* **CI/CD:** GitHub Actions for orchestration and continuous deployment.

## Project Structure

```text
global-tech-expansion/
├── .github/
│   └── workflows/          # CI/CD automation for testing and deployment
├── extraction/             # Ingestion Module (Phase I)
│   ├── connectors/         # Modular API logic
│   │   ├── world_bank.py   
│   │   ├── unesco.py       
│   │   └── oecd.py     
│   ├── main.py             # Orchestrator
│   ├── requirements.txt    # Python dependencies
│   └── utils.py            # Data Contracts & Validations (Pydantic)
├── dbt_project/            # Transformation Module (Phases III & IV)
│   ├── models/             # Medallion Architecture implementation
│   │   ├── staging/        # Bronze: Initial cleaning and typing
│   │   ├── intermediate/   # Silver: Joins and business logic
│   │   └── marts/          # Gold: OBT models for BI
│   ├── snapshots/          # History capture (SCD Type 2)
│   ├── tests/              # SQL data quality audits
│   └── dbt_project.yml     # Central dbt configuration
├── docs/                   # Technical Documentation Stack (PDF)
├── .gitignore              # Project exclusion rules
└── README.md               # Technical overview
```

## Technical Documentation Stack

1. **Global_Expansion_Technical_Roadmap_v1**: Master implementation plan. It outlines the project lifecycle across five phases, from API ingestion to predictive AI modeling.
2. **Global_Expansion_Architecture_Justification_v1**: Technical defense of the system design. It justifies the use of Medallion Architecture and Pydantic Data Contracts based on industry standards.
3. **Global_Expansion_Ingestion_Spec_v1**: API technical documentation. It defines endpoints, Gzip/SDMX protocols, and the normalization standards for World Bank, UNESCO, and OECD data.
4. **Global_Expansion_Dependency_Rationale_v1**: Software stack justification. It explains the strategic role of libraries like Snowpark for cloud processing and Prophet for economic forecasting.
5. **Global_Expansion_Indicators_Analysis_v1**: Strategic variable selection. It details the logic behind transforming raw macroeconomic data into normalized decision metrics for the Opportunity Index.
6. **Global_Expansion_Data_Sources_Technical_Sheet_v1**: Data provider inventory. It validates the reliability and global standardization of the World Bank, UNESCO, and OECD as primary sources.
7. **Global_Expansion_Glossary_v1**: Semantic Single Source of Truth (SSOT). It defines the business logic and impact of every indicator used in the final risk triangulation.
