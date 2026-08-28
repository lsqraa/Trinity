from __future__ import annotations
import sqlite3
from pathlib import Path

from app.domain.entities import Cliente, Envio, EstadoEnvio
from app.domain.ports import IEnvioRepository


class SQLiteAdapter(IEnvioRepository):

    def __init__(self, db_path: str = "data/trinity.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telefono TEXT UNIQUE NOT NULL,
                    asesor_nombre TEXT NOT NULL,
                    nombre TEXT,
                    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS envios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'PENDIENTE',
                    ultimo_error TEXT,
                    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_envios_estado ON envios(estado);
                CREATE INDEX IF NOT EXISTS idx_envios_actualizado ON envios(actualizado_en);
                """
            )

    def save_clientes(self, clientes: list[Cliente]) -> int:
        nuevos_insertados = 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for cliente in clientes:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO clientes (telefono, asesor_nombre, nombre)
                    VALUES (?, ?, ?)
                    """,
                    (cliente.telefono, cliente.asesor_nombre, cliente.nombre),
                )

                if cursor.rowcount > 0:
                    cliente.id = cursor.lastrowid
                    nuevos_insertados += 1
                else:
                    cursor.execute(
                        "SELECT id FROM clientes WHERE telefono = ?",
                        (cliente.telefono,),
                    )
                    row = cursor.fetchone()
                    if row:
                        cliente.id = row["id"]

                cursor.execute(
                    """
                    SELECT id FROM envios WHERE cliente_id = ? AND estado = ?
                    """,
                    (cliente.id, EstadoEnvio.PENDIENTE.value),
                )

                if not cursor.fetchone():
                    cursor.execute(
                        """
                        INSERT INTO envios (cliente_id, estado)
                        VALUES (?, ?)
                        """,
                        (cliente.id, EstadoEnvio.PENDIENTE.value),
                    )
        return nuevos_insertados

    def get_next_pendientes(self, limit: int = 45) -> list[Envio]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    e.id AS envio_id,
                    e.estado,
                    e.ultimo_error,
                    c.id AS cliente_id,
                    c.telefono,
                    c.asesor_nombre,
                    c.nombre
                FROM envios e
                JOIN clientes c ON e.cliente_id = c.id
                WHERE e.estado = ?
                ORDER BY e.id ASC
                LIMIT ?
                """,
                (EstadoEnvio.PENDIENTE.value, limit),
            )
            rows = cursor.fetchall()

        envios: list[Envio] = []
        for row in rows:
            cliente = Cliente(
                id=row["cliente_id"],
                telefono=row["telefono"],
                asesor_nombre=row["asesor_nombre"],
                nombre=row["nombre"],
            )
            envio = Envio(
                id=row["envio_id"],
                cliente=cliente,
                estado=EstadoEnvio(row["estado"]),
                ultimo_error=row["ultimo_error"],
            )
            envios.append(envio)
        return envios

    def actualizar_envio(
        self,
        envio_id: int,
        estado: EstadoEnvio,
        ultimo_error: str | None = None,
    ) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE envios 
                SET estado = ?, ultimo_error = ?, actualizado_en = CURRENT_TIMESTAMP 
                WHERE id = ?
                """,
                (estado.value, ultimo_error, envio_id),
            )

    def get_envios_hoy_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM envios 
                WHERE DATE(actualizado_en, 'localtime') = DATE('now', 'localtime') 
                  AND estado = ?
                """,
                (EstadoEnvio.ENVIADO.value,),
            )
            row = cursor.fetchone()
            return int(row["total"]) if row else 0

    def get_stats(self) -> dict[str, int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    COUNT(*) AS total,
                    COALESCE(SUM(CASE WHEN estado = 'PENDIENTE' THEN 1 ELSE 0 END), 0) AS pendientes,
                    COALESCE(SUM(CASE WHEN estado = 'ENVIADO' THEN 1 ELSE 0 END), 0) AS enviados,
                    COALESCE(SUM(CASE WHEN estado = 'FALLIDO' THEN 1 ELSE 0 END), 0) AS fallidos
                FROM envios
                """
            )
            row = cursor.fetchone()
            if not row:
                return {"total": 0, "pendientes": 0, "enviados": 0, "fallidos": 0}
            return {
                "total": int(row["total"]),
                "pendientes": int(row["pendientes"]),
                "enviados": int(row["enviados"]),
                "fallidos": int(row["fallidos"]),
            }