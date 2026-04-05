import time
from datetime import datetime
from typing import List, Dict, Final, Optional, Mapping
from enum import Enum, auto
from dataclasses import dataclass

# Configuration globale immuable
MIN_LEVEL: Final = 0.0
MAX_LEVEL: Final = 1.0
LOG_FORMAT: Final = "%Y-%m-%d %H:%M:%S"

class StateType(Enum):
    ANXIETY = auto()
    DEPRESSION = auto()
    STRESS = auto()
    STABILITY = auto()
    PEAK_PERFORMANCE = auto()

@dataclass(frozen=True, slots=True)
class Event:
    """Snapshot immuable haute performance d'un état mental."""
    timestamp: str
    state: StateType
    intensity: int
    protocol_triggered: str
    stability_index: float

class BioFeedbackLoop:
    """Moteur de simulation biochimique avec protection contre la dérive."""
    __slots__ = ("_chemistry",)

    def __init__(self):
        self._chemistry: Dict[str, float] = {
            "serotonine": 0.5,
            "dopamine": 0.5,
            "cortisol": 0.2,
            "gaba": 0.6
        }

    def update(self, chemical: str, delta: float) -> None:
        """Ajuste les niveaux avec validation de domaine stricte."""
        if chemical not in self._chemistry:
            raise ValueError(f"Composant '{chemical}' non géré par le noyau.")
        
        current = self._chemistry[chemical]
        # Clamping : On garantit que les valeurs restent entre 0 et 1
        self._chemistry[chemical] = round(max(MIN_LEVEL, min(MAX_LEVEL, current + delta)), 3)

    @property
    def snapshot(self) -> Mapping[str, float]:
        return self._chemistry.copy()

class CognitiveShield:
    """Protocoles de restructuration basés sur les neurosciences et la TCC."""
    PROTOCOLS: Final = {
        StateType.ANXIETY: "🛡️ 4-7-8 + Défusion Cognitive (Observer la pensée sans s'y identifier).",
        StateType.DEPRESSION: "⚡ Activation comportementale immédiate (Règle des 120 secondes).",
        StateType.STRESS: "📉 Scan corporel + Élimination radicale des micro-décisions.",
        StateType.STABILITY: "🧘 Gratitude active (Journaling de 3 victoires).",
        StateType.PEAK_PERFORMANCE: "🚀 Deep Work - Suppression totale de l'environnement de distraction."
    }

    @classmethod
    def resolve(cls, state: StateType) -> str:
        return cls.PROTOCOLS.get(state, "Standard mindfulness protocol activated.")

class SentinelOS:
    """Noyau de gestion du bien-être optimisé pour l'utilisateur."""
    def __init__(self, user_id: str):
        self.user: Final = user_id.upper()
        self.bio = BioFeedbackLoop()
        self.history: List[Event] = []

    def process_state(self, state: StateType, intensity: int) -> str:
        """Analyse l'entrée, déclenche les boucles de rétroaction et archive."""
        # Validation de l'intensité (1-10)
        safe_intensity = max(1, min(10, intensity))
        impact = safe_intensity / 10.0
        protocol = CognitiveShield.resolve(state)

        # Matrice d'impact chimique (Logique atomique)
        impacts = {
            StateType.ANXIETY: {"cortisol": 0.25 * impact, "gaba": -0.2 * impact},
            StateType.STRESS: {"cortisol": 0.3 * impact, "gaba": -0.15 * impact},
            StateType.DEPRESSION: {"dopamine": -0.4 * impact, "serotonine": -0.2 * impact},
            StateType.PEAK_PERFORMANCE: {"dopamine": 0.2, "serotonine": 0.1, "cortisol": -0.1}
        }

        # Application des modifications chimiques
        for chem, delta in impacts.get(state, {}).items():
            self.bio.update(chem, delta)

        # Calcul de l'indice de résilience
        stability = self.get_stability_index()

        # Log de l'événement
        self.history.append(Event(
            timestamp=datetime.now().strftime(LOG_FORMAT),
            state=state,
            intensity=safe_intensity,
            protocol_triggered=protocol,
            stability_index=stability
        ))
        
        return protocol

    def get_stability_index(self) -> float:
        """Calcul pondéré de l'homéostasie émotionnelle."""
        chem = self.bio.snapshot
        # Formule : (Humeur + Calme - Stress) normalisé
        score = (chem['serotonine'] + chem['gaba'] - chem['cortisol'])
        return round(max(0.0, min(1.0, score)), 2)

    def display_report(self):
        """Rendu visuel haute fidélité du statut système."""
        idx = self.get_stability_index()
        status = "🟢 OPTIMAL" if idx > 0.75 else "🟡 VIGILANCE" if idx > 0.45 else "🔴 CRITIQUE"
        
        print(f"\n{'#'*64}")
        print(f" SENTINEL-ALPHA v2.1 | USER: {self.user} | STATUS: {status}")
        print(f"{'#'*64}")
        print(f" BIOMÉTRIE : {self.bio.snapshot}")
        print(f" RÉSILIENCE : {idx * 100}%")
        
        if self.history:
            last = self.history[-1]
            print(f" DERNIER ÉVÉNEMENT : {last.state.name} (Lvl {last.intensity})")
            print(f" ACTION : {last.protocol_triggered}")
        print(f"{'#'*64}\n")

# --- EXECUTION ---
if __name__ == "__main__":
    # Initialisation pour KILIANDIAMA
    system = SentinelOS("KILIANDIAMA")

    # Simulation d'un état de Peak Performance
    system.process_state(StateType.PEAK_PERFORMANCE, 10)
    system.display_report()

    # Redémarrage / Reboot simulé
    print("[SYSTEM] Rebooting for next iteration...\n")
