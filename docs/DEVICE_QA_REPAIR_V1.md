# Device QA Repair Gate v1

Source evidence: physical Android-device screen recording reviewed on 2026-10-05.

Targeted defects:

1. Android Back exited the app while country details were open.
2. Globe pinch zoom was visibly laggy/jittery.
3. Country selection left the soft keyboard open temporarily.
4. The active metric could remain clipped outside the horizontal selector viewport.
5. The mobile legend occupied excessive map area.
6. Reset-view could collide with overlays when the details sheet was open.
7. Keyboard-to-details transitions produced layout jumps.
8. Portrait flat-map space utilization was weak.
9. Root-level Back had no accidental-exit protection.

Repair policy: preserve data, metric semantics, Grok source provenance, and desktop behavior; modify only native navigation, gesture rendering, and mobile presentation required by device evidence.
