import os
from dataclasses import dataclass, field
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class MemoryRecord:
    """Represents a single memory item in an AI agent's multi-tier memory store."""
    rec_id: int
    topic_vec: np.ndarray          # Normalized semantic embedding
    fact_key: str                  # Entity/attribute key for contradiction checks
    fact_value: int                # Discrete state/value for exact conflict detection
    timestamp: int                 # Creation turn
    tier: str                      # 'working', 'episodic', or 'archival'
    has_provenance: bool = True    # Valid source citation / lineage flag
    superseded: bool = False       # Whether a newer verified record replaced this


class AIMemoryBenchmark:
    """
    Milestone #5: Evaluates Darkness Functional D[Sigma, t] and Persistence S(t)
    across an AI agent's multi-tier memory store under fragmentation, contradiction,
    high-throughput noise, and consolidation/restoration.
    """

    def __init__(
        self,
        embed_dim: int = 16,
        weights: tuple[float, float, float, float] = (1.0, 0.85, 0.9, 1.4),
        seed: int = 7,
    ):
        self.rng = np.random.default_rng(seed)
        self.embed_dim = embed_dim
        self.alpha, self.beta, self.gamma, self.delta = weights
        self.records: list[MemoryRecord] = []
        self.next_id = 0

    def _unit_vec(self, base: np.ndarray | None = None, jitter: float = 0.05) -> np.ndarray:
        if base is None:
            v = self.rng.normal(0.0, 1.0, self.embed_dim)
        else:
            v = base + self.rng.normal(0.0, jitter, self.embed_dim)
        return v / (np.linalg.norm(v) + 1e-12)

    def ingest(
        self,
        topic_vec: np.ndarray,
        fact_key: str,
        fact_value: int,
        turn: int,
        tier: str = "episodic",
        has_provenance: bool = True,
        jitter: float = 0.06,
    ) -> MemoryRecord:
        rec = MemoryRecord(
            rec_id=self.next_id,
            topic_vec=self._unit_vec(topic_vec, jitter=jitter),
            fact_key=fact_key,
            fact_value=fact_value,
            timestamp=turn,
            tier=tier,
            has_provenance=has_provenance,
        )
        self.next_id += 1
        self.records.append(rec)
        return rec

    def retrieve(self, query_vec: np.ndarray, top_k: int = 6, noise_injection: float = 0.0) -> list[MemoryRecord]:
        """Retrieve top-k records by cosine similarity plus optional retrieval noise."""
        if not self.records:
            return []
        scored = []
        for rec in self.records:
            sim = float(np.dot(query_vec, rec.topic_vec))
            noisy_sim = sim + float(self.rng.normal(0.0, noise_injection))
            scored.append((noisy_sim, rec))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [rec for _, rec in scored[:top_k]]

    def consolidate_memory(self, canonical_facts: dict[str, int]) -> int:
        """
        Restoration pass (analogous to k_restore / lenslet projection):
        1. Prunes records lacking provenance.
        2. Marks outdated or contradictory records as superseded against verified truth.
        """
        repaired = 0
        cleaned = []
        for rec in self.records:
            if not rec.has_provenance:
                repaired += 1
                continue
            if rec.fact_key in canonical_facts and rec.fact_value != canonical_facts[rec.fact_key]:
                rec.superseded = True
                repaired += 1
            cleaned.append(rec)
        self.records = cleaned
        return repaired

    def evaluate_turn(
        self,
        query_vec: np.ndarray,
        retrieved: list[MemoryRecord],
        canonical_facts: dict[str, int],
        throughput_phi: float = 1.0,
    ) -> dict[str, float]:
        """Compute r(t), N(t), F_C(t), M_I(t), D[Sigma, t], and S(t) for a retrieval step."""
        if not retrieved:
            return {"r": 0.0, "N": 1.0, "FC": 1.0, "MI": 1.0, "D": 4.0, "S": 0.0}

        # 1. Coherence r(t): semantic alignment penalized by superseded/stale hits
        sims = np.array([max(0.0, float(np.dot(query_vec, r.topic_vec))) for r in retrieved])
        fresh_mask = np.array([0.25 if r.superseded else 1.0 for r in retrieved])
        r_val = float(np.clip(np.mean(sims * fresh_mask), 0.0, 1.0))

        # 2. Noise N(t): irrelevant off-topic fraction + retrieval score dispersion
        off_topic = np.mean(sims < 0.45)
        score_var = float(np.var(sims))
        N_val = float(off_topic + score_var)

        # 3. Constraint Failure F_C(t): missing provenance + chronological inversions
        missing_prov = np.mean([0.0 if r.has_provenance else 1.0 for r in retrieved])
        timestamps = [r.timestamp for r in retrieved]
        # Count chronological inversions when descending recency is expected
        inversions = sum(
            1 for i in range(len(timestamps) - 1) if timestamps[i] < timestamps[i + 1]
        ) / max(1, len(timestamps) - 1)
        FC_val = float(0.65 * missing_prov + 0.35 * inversions)

        # 4. Interface Mismatch M_I(t): pairwise factual contradiction across tiers & records
        contradictions = 0
        pairs = 0
        for i in range(len(retrieved)):
            for j in range(i + 1, len(retrieved)):
                if retrieved[i].fact_key == retrieved[j].fact_key:
                    pairs += 1
                    if retrieved[i].fact_value != retrieved[j].fact_value:
                        contradictions += 1
        # Also check mismatch against canonical ground truth
        truth_errors = np.mean([
            1.0 if (r.fact_key in canonical_facts and r.fact_value != canonical_facts[r.fact_key]) else 0.0
            for r in retrieved
        ])
        pair_conflict_rate = (contradictions / pairs) if pairs > 0 else 0.0
        MI_val = float(0.6 * pair_conflict_rate + 0.4 * truth_errors)

        # Darkness Functional D[Sigma, t]
        D = (
            self.alpha * (1.0 - r_val)
            + self.beta * N_val
            + self.gamma * FC_val
            + self.delta * MI_val
        )

        # Admissible manifold C(Omega, t) and Persistence S(t)
        C_omega = float(np.exp(-0.5 * FC_val))
        S = float(r_val * C_omega * throughput_phi * np.exp(-D))

        return {
            "r": r_val,
            "N": N_val,
            "FC": FC_val,
            "MI": MI_val,
            "D": D,
            "S": S,
            "c_decoherence": self.alpha * (1.0 - r_val),
            "c_noise": self.beta * N_val,
            "c_constraint": self.gamma * FC_val,
            "c_mismatch": self.delta * MI_val,
        }


def run_ai_memory_experiment(turns: int = 40, seed: int = 7) -> dict[str, np.ndarray]:
    """Run a 40-turn lifecycle demonstrating fragmentation, throughput illusion, and consolidation."""
    bench = AIMemoryBenchmark(seed=seed)

    # Establish 4 core semantic topics and canonical truth states
    topics = {f"project_spec_{k}": bench._unit_vec() for k in range(4)}
    canonical_facts = {f"project_spec_{k}": 100 + k for k in range(4)}
    distractor_vec = bench._unit_vec()

    # Seed initial clean memory store
    for k, vec in topics.items():
        bench.ingest(vec, k, canonical_facts[k], turn=0, tier="archival", has_provenance=True)

    history = {k: np.zeros(turns) for k in [
        "t", "r", "D", "D_cum", "S", "c_decoherence", "c_noise", "c_constraint", "c_mismatch"
    ]}
    cum_D = 0.0

    for t in range(turns):
        active_key = f"project_spec_{t % 4}"
        query_vec = topics[active_key]

        # Phase 1 (0-9): Clean operation
        if t < 10:
            bench.ingest(query_vec, active_key, canonical_facts[active_key], turn=t, tier="working")
            retrieved = bench.retrieve(query_vec, top_k=5, noise_injection=0.03)
            phi = 1.0

        # Phase 2 (10-19): Fragmentation, unverified writes, and contradictory updates
        elif t < 20:
            # Inject contradictory fact without provenance
            corrupt_val = canonical_facts[active_key] + 999
            bench.ingest(
                query_vec, active_key, corrupt_val, turn=t, tier="working",
                has_provenance=False, jitter=0.18
            )
            # Inject off-topic distractor
            bench.ingest(distractor_vec, "noise_log", -1, turn=t, tier="episodic", has_provenance=False, jitter=0.4)
            retrieved = bench.retrieve(query_vec, top_k=6, noise_injection=0.18)
            phi = 1.0

        # Phase 3 (20-27): High-throughput illusion (doubling top_k and Phi without cleanup)
        elif t < 28:
            retrieved = bench.retrieve(query_vec, top_k=12, noise_injection=0.25)
            phi = 1.8  # High computational/token throughput masking rising Darkness

        # Phase 4 (28-39): Consolidation / Restoration pass
        else:
            if t == 28:
                bench.consolidate_memory(canonical_facts)
            bench.ingest(query_vec, active_key, canonical_facts[active_key], turn=t, tier="episodic", has_provenance=True)
            retrieved = bench.retrieve(query_vec, top_k=5, noise_injection=0.04)
            phi = 1.1

        metrics = bench.evaluate_turn(query_vec, retrieved, canonical_facts, throughput_phi=phi)
        cum_D += metrics["D"]

        history["t"][t] = t
        history["D_cum"][t] = cum_D
        for k in ["r", "D", "S", "c_decoherence", "c_noise", "c_constraint", "c_mismatch"]:
            history[k][t] = metrics[k]

    return history


def save_ai_memory_figures(history: dict[str, np.ndarray], fig_dir: str = "../figures") -> None:
    os.makedirs(fig_dir, exist_ok=True)
    t = history["t"]

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    # Panel 1: Coherence r(t) vs Persistence S(t)
    axes[0].plot(t, history["r"], "--", color="teal", linewidth=2, label="Retrieval Alignment r(t)")
