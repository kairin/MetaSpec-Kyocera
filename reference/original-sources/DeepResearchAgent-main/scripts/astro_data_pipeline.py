#!/usr/bin/env python3
"""
Astro Data Pipeline - Convert research results to Astro-compatible data
"""
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class AstroDataPipeline:
    def __init__(self,
                 outputs_dir: str = "outputs",
                 astro_dir: str = "astro-docs",
                 data_subdir: str = "src/data"):
        self.outputs_dir = Path(outputs_dir)
        self.astro_dir = Path(astro_dir)
        self.astro_data_dir = self.astro_dir / data_subdir

        # Ensure astro data directory exists
        self.astro_data_dir.mkdir(parents=True, exist_ok=True)

    def extract_research_sessions(self) -> List[Dict[str, Any]]:
        """Extract research sessions from all output directories"""
        sessions = []

        for output_subdir in self.outputs_dir.iterdir():
            if not output_subdir.is_dir():
                continue

            # Look for log files and JSONL files
            log_files = list(output_subdir.glob("*.log"))
            jsonl_files = list(output_subdir.glob("*.jsonl"))

            for log_file in log_files:
                session_data = self._parse_log_file(log_file, output_subdir.name)
                if session_data:
                    sessions.append(session_data)

            for jsonl_file in jsonl_files:
                session_data = self._parse_jsonl_file(jsonl_file, output_subdir.name)
                if session_data:
                    sessions.append(session_data)

        return sessions

    def _parse_log_file(self, log_file: Path, config_type: str) -> Dict[str, Any]:
        """Parse log file to extract session information"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract basic information from log
            lines = content.split('\n')

            # Look for task information
            task = None
            result = None
            start_time = None

            for line in lines:
                if "Executing custom task:" in line:
                    task = line.split("Executing custom task:")[1].strip()
                elif "Result:" in line and "logger:INFO" in line:
                    result = line.split("Result:")[-1].strip()
                elif "Logger initialized" in line:
                    # Extract timestamp
                    if " - " in line:
                        timestamp_part = line.split(" - ")[0]
                        try:
                            # Parse timestamp from log format
                            start_time = timestamp_part.strip()
                        except:
                            pass

            if task:
                return {
                    "id": f"{config_type}_{log_file.stem}",
                    "config_type": config_type,
                    "task": task,
                    "result": result or "No result found",
                    "timestamp": start_time or log_file.stat().st_mtime,
                    "log_file": str(log_file.relative_to(self.outputs_dir)),
                    "status": "completed" if result else "unknown"
                }
        except Exception as e:
            print(f"Error parsing log file {log_file}: {e}")

        return None

    def _parse_jsonl_file(self, jsonl_file: Path, config_type: str) -> Dict[str, Any]:
        """Parse JSONL file to extract session information"""
        try:
            sessions = []
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        sessions.append(data)

            if sessions:
                # Use the latest session data
                latest = sessions[-1]
                return {
                    "id": f"{config_type}_{jsonl_file.stem}",
                    "config_type": config_type,
                    "task": latest.get("task", "Unknown task"),
                    "result": latest.get("result", "No result"),
                    "timestamp": latest.get("timestamp", jsonl_file.stat().st_mtime),
                    "jsonl_file": str(jsonl_file.relative_to(self.outputs_dir)),
                    "status": "completed",
                    "data": latest
                }
        except Exception as e:
            print(f"Error parsing JSONL file {jsonl_file}: {e}")

        return None

    def generate_astro_data(self) -> None:
        """Generate Astro-compatible data files"""
        sessions = self.extract_research_sessions()

        # Sort sessions by timestamp (newest first)
        sessions.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

        # Generate main sessions data
        sessions_file = self.astro_data_dir / "research-sessions.json"
        with open(sessions_file, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_sessions": len(sessions),
                "sessions": sessions
            }, f, indent=2, default=str)

        # Generate summary statistics
        stats = self._generate_stats(sessions)
        stats_file = self.astro_data_dir / "research-stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)

        # Generate config type breakdown
        config_breakdown = {}
        for session in sessions:
            config_type = session.get("config_type", "unknown")
            if config_type not in config_breakdown:
                config_breakdown[config_type] = []
            config_breakdown[config_type].append(session)

        configs_file = self.astro_data_dir / "config-breakdown.json"
        with open(configs_file, 'w', encoding='utf-8') as f:
            json.dump(config_breakdown, f, indent=2, default=str)

        print(f"Generated Astro data files:")
        print(f"  - {sessions_file}")
        print(f"  - {stats_file}")
        print(f"  - {configs_file}")

    def _generate_stats(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate statistics from sessions"""
        if not sessions:
            return {
                "total_sessions": 0,
                "config_types": {},
                "status_breakdown": {},
                "recent_activity": []
            }

        config_types = {}
        status_breakdown = {}

        for session in sessions:
            # Config type stats
            config_type = session.get("config_type", "unknown")
            config_types[config_type] = config_types.get(config_type, 0) + 1

            # Status stats
            status = session.get("status", "unknown")
            status_breakdown[status] = status_breakdown.get(status, 0) + 1

        # Recent activity (last 10 sessions)
        recent_activity = sessions[:10]

        return {
            "total_sessions": len(sessions),
            "config_types": config_types,
            "status_breakdown": status_breakdown,
            "recent_activity": recent_activity,
            "last_updated": datetime.now().isoformat()
        }

    def watch_and_update(self) -> None:
        """Watch for changes and update Astro data (for development)"""
        print("Watching for changes in outputs directory...")
        print("Press Ctrl+C to stop")

        try:
            import time
            last_update = 0

            while True:
                # Check if any files have been modified
                current_time = time.time()
                needs_update = False

                for output_dir in self.outputs_dir.iterdir():
                    if output_dir.is_dir():
                        for file_path in output_dir.glob("*"):
                            if file_path.stat().st_mtime > last_update:
                                needs_update = True
                                break

                if needs_update:
                    print(f"Changes detected, updating Astro data...")
                    self.generate_astro_data()
                    last_update = current_time

                time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            print("\nWatcher stopped.")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Astro Data Pipeline")
    parser.add_argument("--watch", action="store_true",
                       help="Watch for changes and auto-update")
    parser.add_argument("--outputs-dir", default="outputs",
                       help="Outputs directory path")
    parser.add_argument("--astro-dir", default="astro-docs",
                       help="Astro project directory path")

    args = parser.parse_args()

    pipeline = AstroDataPipeline(
        outputs_dir=args.outputs_dir,
        astro_dir=args.astro_dir
    )

    if args.watch:
        pipeline.watch_and_update()
    else:
        pipeline.generate_astro_data()

if __name__ == "__main__":
    main()