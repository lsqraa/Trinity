from __future__ import annotations
import re
import unicodedata
from typing import Any

from app.domain.entities import Cliente


def normalize_phone(raw_phone: Any) -> str | None:
    if raw_phone is None:
        return None

    text = str(raw_phone).strip()
    if text.endswith(".0"):
        text = text[:-2]

    digits = re.sub(r"\D", "", text)

    if digits.startswith("593") and len(digits) == 12:
        digits = digits[3:]
    elif digits.startswith("0") and len(digits) == 10:
        digits = digits[1:]

    if len(digits) == 9 and digits.startswith("9"):
        return digits

    return None


def sanitize_text(raw_text: Any) -> str | None:
    if raw_text is None:
        return None

    text = str(raw_text)
    cleaned = "".join(
        ch for ch in text if unicodedata.category(ch) != "Cc" and ch.isprintable()
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    if not cleaned or cleaned.lower() in ("nan", "none", "null"):
        return None

    return cleaned

def validate_record(
    record: dict[str, Any], default_asesor: str = "Asesor Asignado"
) -> Cliente | None:
    raw_telefono = record.get("TELEFONO")
    raw_asesor = record.get("ASESOR")
    raw_nombres = record.get("NOMBRES")

    telefono = normalize_phone(raw_telefono)
    if not telefono:
        return None

    asesor = sanitize_text(raw_asesor) or default_asesor
    nombre = sanitize_text(raw_nombres)

    return Cliente(
        telefono=telefono,
        asesor_nombre=asesor,
        nombre=nombre,
    )


def validate_and_transform_records(
    records: list[dict[str, Any]], default_asesor: str = "Asesor Asignado"
) -> list[Cliente]:
    clientes: list[Cliente] = []
    for record in records:
        cliente = validate_record(record, default_asesor=default_asesor)
        if cliente:
            clientes.append(cliente)
    return clientes


class ContactValidatorService:

    def normalize_phone(self, raw_phone: Any) -> str | None:
        return normalize_phone(raw_phone)

    def sanitize_text(self, raw_text: Any) -> str | None:
        return sanitize_text(raw_text)

    def validate_record(
        self, record: dict[str, Any], default_asesor: str = "Asesor Asignado"
    ) -> Cliente | None:
        return validate_record(record, default_asesor=default_asesor)

    def validate_and_transform_records(
        self, records: list[dict[str, Any]], default_asesor: str = "Asesor Asignado"
    ) -> list[Cliente]:
        return validate_and_transform_records(records, default_asesor=default_asesor)

