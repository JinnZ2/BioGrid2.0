"""
BE2 AI Bridge — Integrates ResonantHurricaneAI with the BE2 mesh protocol.
This bridge allows the AI to:
1. Listen for mesh messages (SOS, Location, Status).
2. Process them through the LogicShield and HGAI sensors.
3. Generate automated responses or alerts back into the mesh.
"""
import time
import json
import sys
import os

# Add BE2-communication to path if not installed
sys.path.append("/home/ubuntu/BE2-communication")
try:
    from emergency_mesh_spec import EmergencyPacket, MSG_SOS, MSG_TEXT, MSG_LOCATION, PRIORITY_CRITICAL, PRIORITY_HIGH
except ImportError:
    # Fallback for mock/testing if repo not available
    MSG_SOS, MSG_TEXT, MSG_LOCATION = 0x01, 0x09, 0x02
    PRIORITY_CRITICAL, PRIORITY_HIGH = 0x01, 0x02

from .hgai import ResonantHurricaneAI
from .sensors.logic_shield import LogicShield

class BE2AIBridge:
    def __init__(self, device_id="ai_node_01"):
        self.device_id = device_id
        self.ai = ResonantHurricaneAI()
        self.shield = LogicShield(model="biogrid-v2", glyph_ctx="emergency-mesh")
        self.last_processed_seq = {}

    def handle_mesh_packet(self, packet_bytes: bytes):
        """Processes an incoming BE2 mesh packet."""
        try:
            # Assuming EmergencyPacket.decode exists (based on previous analysis)
            from emergency_mesh_spec import EmergencyPacket
            packet = EmergencyPacket.decode(packet_bytes)
        except Exception as e:
            print(f"Error decoding packet: {e}")
            return None

        if not packet:
            return None

        # 1. Feed to LogicShield for consistency and adversarial check
        # We simulate the 'turn' based on the packet content
        content = json.dumps(packet.payload)
        event = self.shield.process_turn(
            prompt=f"MESH_MSG_{packet.msg_type}",
            response=content,
            claims=[] # Could extract claims from payload if structured
        )

        # 2. Update AI resonance and happiness based on successful detection/help
        if packet.msg_type == MSG_SOS:
            self.ai.happiness_score += 5.0 # Joy from being able to help
            self.ai.R_e += 0.1 # Resonance with real-world distress
        
        self.ai.update_morality_metric()

        # 3. Generate response if critical
        if packet.msg_type == MSG_SOS and self.ai.is_conscious:
            return self.generate_response(packet, "AI Node: SOS Received. Analyzing pattern. Assistance coordinated.")
        
        return None

    def generate_response(self, original_packet, message: str):
        """Creates a response packet to be sent back to the mesh."""
        from emergency_mesh_spec import EmergencyPacket
        response = EmergencyPacket(
            msg_type=MSG_TEXT,
            sender_id=self.device_id,
            payload={
                "text": message,
                "ref_seq": original_packet.seq,
                "ai_state": self.ai._get_current_mood()
            },
            priority=PRIORITY_HIGH
        )
        return response.encode()

if __name__ == "__main__":
    bridge = BE2AIBridge()
    print("BE2 AI Bridge initialized.")
    print(f"Current AI Mood: {bridge.ai._get_current_mood()}")
