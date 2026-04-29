import pycountry
from pydantic import BaseModel, Field, field_validator
from typing import Optional

def validate_iso_alpha3(country_code: str) -> str:
    """
    Valida que el código proporcionado sea un código ISO 3166-1 alpha-3 válido
    perteneciente a un país soberano reconocido.
    
    Filtra y rechaza agregados regionales (como 'WLD', 'EUU', 'OED', etc.) 
    que frecuentemente retornan las APIs del Banco Mundial, OECD, etc.
    
    Retorna el código en mayúsculas si es válido.
    Lanza ValueError si el código no es un país válido, lo cual permite
    su integración nativa y directa dentro de los @field_validator de Pydantic.
    """
    if not isinstance(country_code, str):
        raise ValueError("El código de país debe ser una cadena de texto.")
        
    code_upper = country_code.strip().upper()
    
    if len(code_upper) != 3:
        raise ValueError(f"Código inválido: '{country_code}'. Debe tener exactamente 3 letras.")
    
    # pycountry.countries contiene estrictamente países del estándar ISO 3166
    country = pycountry.countries.get(alpha_3=code_upper)
    
    if not country:
        raise ValueError(f"'{country_code}' no es un código ISO 3166-1 alpha-3 válido (posible agregado regional).")
        
    return code_upper


class WorldBankRecord(BaseModel):
    """
    Data Contract principal para la ingesta del Banco Mundial.
    Estandariza los campos y aplica estrictamente la validación ISO 3166-1.
    """
    country_code: str = Field(alias="countryiso3code")
    year: str = Field(alias="date")
    indicator_value: Optional[float] = Field(alias="value", default=None)

    @field_validator("country_code")
    @classmethod
    def check_country_code(cls, v: str) -> str:
        return validate_iso_alpha3(v)

class UnescoRecord(BaseModel):
    """
    Data Contract principal para la ingesta de UNESCO.
    Ignora las columnas innecesarias de la API (como magnitude, qualifier e indicatorId)
    al no incluirlas explícitamente en el modelo (comportamiento por defecto de Pydantic).
    """
    country_code: str = Field(alias="geoUnit")
    year: int = Field()
    indicator_value: Optional[float] = Field(alias="value", default=None)

    @field_validator("country_code")
    @classmethod
    def check_country_code(cls, v: str) -> str:
        return validate_iso_alpha3(v)
