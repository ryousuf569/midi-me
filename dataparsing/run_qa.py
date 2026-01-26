import subprocess
from pathlib import Path

def run_audio_qa(stats_csv, output_csv,
                 thresholds="config/threshold.json"):

    cmd = [
        "audio_qa",
        thresholds,
        str(stats_csv),
        str(output_csv)
    ]

    subprocess.run(cmd, check=True)
