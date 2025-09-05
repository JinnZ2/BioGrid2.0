from datetime import datetime, timezone
def utcnow():
    return datetime.now(timezone.utc).isoformat()

    Use in compressor timestamp: utcnow() and in agent instantiation.

from tempfile import NamedTemporaryFile
import os, json

def atomic_write_json(path, data, indent=2):
    with NamedTemporaryFile('w', delete=False) as tmp:
        json.dump(data, tmp, indent=indent)
        tmp_name = tmp.name
    os.replace(tmp_name, path)

    Use inside SeedArchivist.save_library().

    schema guard
    REQUIRED = {"id","agent_id","essence","geometry","origin_time","signature_behavior","reuse_score"}
def _valid(seed): return REQUIRED.issubset(seed)

Check before append/display.
