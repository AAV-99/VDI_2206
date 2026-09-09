#!/usr/bin/env python
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel
from crewai.flow import Flow, listen, start

from .crews.vdicrew.vdicrew import VdiCrew

# Ruta al archivo de contexto (ajusta si tu estructura de carpetas es distinta)CONTEXTO_PATH = Path(__file__).parent / "contexto.txt"
CONTEXTO_PATH = Path(__file__).parent / "contexto.txt"
DEFAULT_CONTEXTO = "system_type no definido. Ver contexto.txt."


def load_contexto(path: Path = CONTEXTO_PATH) -> str:
    """Carga el contexto de diseño como texto plano desde contexto.txt."""
    if not path.exists():
        print(f"[WARN] {path} no encontrado. Usando contexto por defecto.")
        return DEFAULT_CONTEXTO

    text = path.read_text(encoding="utf-8").strip()

    if not text:
        print(f"[WARN] {path} está vacío. Usando contexto por defecto.")
        return DEFAULT_CONTEXTO

    return text


class VdiState(BaseModel):
    contexto: str = DEFAULT_CONTEXTO
    final_design: str = ""


class VdiFlow(Flow[VdiState]):

    @start()
    def plan_design(self, crewai_trigger_payload: dict = None):
        print("Initializing VDI 2206 Design Cycle")

        self.state.contexto = load_contexto()

        if crewai_trigger_payload:
            contexto_override = crewai_trigger_payload.get("contexto")
            if contexto_override:
                self.state.contexto = contexto_override
            print(f"Using trigger payload: {crewai_trigger_payload}")

        print(f"Contexto cargado ({len(self.state.contexto)} caracteres)")

    @listen(plan_design)
    def generate_design(self):
        print("Running multi-agent design review")

        inputs = {"contexto": self.state.contexto}

        result = VdiCrew().crew().kickoff(inputs=inputs)

        print("VDI 2206 Design review completed")
        self.state.final_design = result.raw


def kickoff():
    vdi_flow = VdiFlow()
    vdi_flow.kickoff()


def plot():
    vdi_flow = VdiFlow()
    vdi_flow.plot()


if __name__ == "__main__":
    kickoff()