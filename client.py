# -*- coding: utf-8 -*-
"""Cross-Dock Pallet Break-Bulk Scheduler for GenPark Agentic Commerce."""
import json
from typing import Dict, Any, List

class CrossDockPalletBreakBulkScheduler:
    @staticmethod
    def schedule_cross_dock_direct_transfer(inbound_pallets: List[Dict[str, Any]], outbound_doors: List[Dict[str, Any]]) -> Dict[str, Any]:
        door_map = {d.get("destination"): d.get("door_id") for d in outbound_doors}
        transfers = []
        staged_for_putaway = []
        
        for p in inbound_pallets:
            dest = p.get("destination")
            if dest in door_map:
                transfers.append({
                    "pallet_id": p.get("pallet_id"),
                    "destination": dest,
                    "target_outbound_door": door_map[dest],
                    "routing": "IMMEDIATE_CROSS_DOCK"
                })
            else:
                staged_for_putaway.append(p.get("pallet_id"))
                
        cross_dock_ratio = round((len(transfers) / max(1, len(inbound_pallets))) * 100.0, 1)
        return {
            "total_pallets_inbound": len(inbound_pallets),
            "direct_cross_dock_transfers": len(transfers),
            "cross_dock_efficiency_pct": cross_dock_ratio,
            "staging_buffer_count": len(staged_for_putaway),
            "transfer_manifest": transfers
        }

    @staticmethod
    def audit_cross_dock_dwell_time_efficiency(pallet_count: int, avg_dwell_minutes: float, standard_putaway_cost_per_pallet_usd: float = 14.5) -> Dict[str, Any]:
        labor_savings_usd = round(pallet_count * standard_putaway_cost_per_pallet_usd * 0.75, 2)
        dwell_tier = "WORLD_CLASS_ZERO_INVENTORY" if avg_dwell_minutes < 45.0 else ("ACCEPTABLE_FLOW" if avg_dwell_minutes < 120.0 else "BOTTLENECK_STAGING")
        
        return {
            "pallet_volume": pallet_count,
            "average_dwell_minutes": avg_dwell_minutes,
            "estimated_handling_cost_savings_usd": labor_savings_usd,
            "cross_dock_benchmark_tier": dwell_tier
        }
