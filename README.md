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

1. **Global_Expansion_Technical_Roadmap_v1**: Detailed master implementation plan by phases (Ingestion, Infrastructure, Modeling, and Analytics).
2. **Global_Expansion_Architecture_Justification_v1**: Technical justification of the stack (Snowflake, dbt, Python) and Medallion architecture design.
3. **Global_Expansion_Ingestion_Spec_v1**: Technical specification of endpoints, communication protocols (SDMX-JSON), and API contracts.
4. **Global_Expansion_Dependency_Rationale_v1**: Rationale behind project libraries (Pydantic, Snowpark, Prophet) and their role in the pipeline.
5. **Global_Expansion_Indicators_Analysis_v1**: Strategic justification for the selection of macroeconomic and financial indicators.
6. **Global_Expansion_Data_Sources_Technical_Sheet_v1**: Technical data sheet of origin sources (World Bank, UNESCO, OECD) and their metadata.
7. **Global_Expansion_Glossary_v1**: Semantic definition of indicators to ensure a Single Source of Truth (SSOT).
