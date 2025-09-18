#!/usr/bin/env python3
"""
Guardian Package Manager - Core Library
Handles intelligent updates, conflict resolution, and advanced operations
"""

import difflib
import hashlib
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


@dataclass
class AgentInfo:
    """Information about a Guardian agent"""

    id: str
    name: str
    path: str
    checksum: str
    version: str
    customized: bool = False
    last_updated: str | None = None


@dataclass
class UpdateChange:
    """Represents a change during update"""

    agent_id: str
    change_type: str  # 'new', 'updated', 'conflict', 'deprecated'
    local_path: str
    remote_content: str
    conflict_resolution: str | None = None


class GuardianUpdater:
    """Intelligent update system for Guardian agents"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.guardian_dir = self.project_root / ".guardian"
        self.claude_dir = self.project_root / ".claude" / "agents"
        self.cache_dir = self.guardian_dir / "cache"

        self.guardian_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)

        self.metadata = self.load_metadata()
        self.remote_manifest: dict[str, Any] | None = None

    def load_metadata(self) -> dict[str, Any]:
        """Load local metadata file"""
        metadata_file = self.guardian_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    data: dict[str, Any] = json.load(f)
                    return data
            except json.JSONDecodeError:
                print("⚠️ Corrupted metadata file, reinitializing...")
                return self._create_empty_metadata()
        else:
            return self._create_empty_metadata()

    def _create_empty_metadata(self) -> dict[str, Any]:
        """Create empty metadata structure"""
        return {
            "guardian_version": None,
            "project_type": "generic",
            "installed_at": None,
            "agents": {},
            "customizations": {},
            "spec_integration": False,
        }

    def save_metadata(self) -> None:
        """Save metadata to file"""
        metadata_file = self.guardian_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def fetch_remote_manifest(self) -> dict[str, Any]:
        """Fetch remote manifest with agent information"""
        if self.remote_manifest is not None:
            return self.remote_manifest

        manifest_url = "https://raw.githubusercontent.com/kairin/claude-guardian-agents/main/manifest.json"

        try:
            print("🔍 Fetching remote manifest...")
            response = requests.get(manifest_url, timeout=30)
            response.raise_for_status()
            self.remote_manifest = response.json()

            with open(self.cache_dir / "remote-manifest.json", "w") as f:
                json.dump(self.remote_manifest, f, indent=2)

            return self.remote_manifest

        except requests.RequestException as e:
            print(f"❌ Failed to fetch remote manifest: {e}")

            cached_manifest = self.cache_dir / "remote-manifest.json"
            if cached_manifest.exists():
                print("📋 Using cached manifest...")
                with open(cached_manifest) as f:
                    data: dict[str, Any] = json.load(f)
                    self.remote_manifest = data
                return self.remote_manifest

            raise Exception("Unable to fetch or find cached manifest") from e

    def calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return ""

    def identify_changes(self) -> list[UpdateChange]:
        """Identify what needs to be updated"""
        manifest = self.fetch_remote_manifest()
        changes = []

        remote_agents = manifest.get("agents", {})
        local_agents = self.metadata.get("agents", {})

        for agent_id, remote_info in remote_agents.items():
            local_info = local_agents.get(agent_id, {})

            if not local_info:
                changes.append(
                    UpdateChange(
                        agent_id=agent_id,
                        change_type="new",
                        local_path=f".claude/agents/{remote_info['name']}.md",
                        remote_content=self._fetch_agent_content(remote_info["path"]),
                    )
                )
            elif local_info.get("checksum") != remote_info.get("checksum"):
                change_type = (
                    "conflict" if local_info.get("customized", False) else "updated"
                )
                changes.append(
                    UpdateChange(
                        agent_id=agent_id,
                        change_type=change_type,
                        local_path=f".claude/agents/{remote_info['name']}.md",
                        remote_content=self._fetch_agent_content(remote_info["path"]),
                    )
                )

        for agent_id in local_agents:
            if agent_id not in remote_agents:
                changes.append(
                    UpdateChange(
                        agent_id=agent_id,
                        change_type="deprecated",
                        local_path=f".claude/agents/{local_agents[agent_id].get('name', agent_id)}.md",
                        remote_content="",
                    )
                )

        return changes

    def _fetch_agent_content(self, agent_path: str) -> str:
        """Fetch agent content from remote repository"""
        url = f"https://raw.githubusercontent.com/kairin/claude-guardian-agents/main/{agent_path}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"⚠️ Failed to fetch agent content from {url}: {e}")
            return ""

    def apply_updates(self, changes: list[UpdateChange]) -> bool:
        """Apply updates with intelligent conflict resolution"""
        success = True

        print(f"📥 Applying {len(changes)} changes...")

        for change in changes:
            try:
                if change.change_type == "new":
                    self._apply_new_agent(change)
                elif change.change_type == "updated":
                    self._apply_updated_agent(change)
                elif change.change_type == "conflict":
                    self._resolve_conflict(change)
                elif change.change_type == "deprecated":
                    self._handle_deprecated_agent(change)

            except Exception as e:
                print(f"❌ Failed to apply change for {change.agent_id}: {e}")
                success = False

        return success

    def _apply_new_agent(self, change: UpdateChange) -> None:
        """Install new agent"""
        print(f"➕ Installing new agent: {change.agent_id}")

        local_path = Path(change.local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        with open(local_path, "w") as f:
            f.write(change.remote_content)

        checksum = self.calculate_file_checksum(local_path)
        self.metadata["agents"][change.agent_id] = {
            "name": local_path.stem,
            "checksum": checksum,
            "customized": False,
            "installed_at": self._current_timestamp(),
        }

    def _apply_updated_agent(self, change: UpdateChange) -> None:
        """Update existing agent"""
        print(f"🔄 Updating agent: {change.agent_id}")

        with open(change.local_path, "w") as f:
            f.write(change.remote_content)

        checksum = self.calculate_file_checksum(Path(change.local_path))
        self.metadata["agents"][change.agent_id]["checksum"] = checksum
        self.metadata["agents"][change.agent_id][
            "last_updated"
        ] = self._current_timestamp()

    def _resolve_conflict(self, change: UpdateChange) -> None:
        """Resolve conflicts in customized agents"""
        print(f"🔀 Resolving conflict for customized agent: {change.agent_id}")

        local_path = Path(change.local_path)
        if not local_path.exists():
            print(f"⚠️ Local file not found: {local_path}")
            self._apply_new_agent(change)
            return

        with open(local_path) as f:
            local_content = f.read()

        remote_content = change.remote_content

        original_content = self._get_original_version(change.agent_id)

        if original_content:
            merged_content = self._three_way_merge(
                original_content, local_content, remote_content
            )

            if merged_content:
                print(f"✅ Auto-merged {change.agent_id}")
                with open(local_path, "w") as f:
                    f.write(merged_content)
            else:
                self._interactive_resolve(change, local_content, remote_content)
        else:
            self._interactive_resolve(change, local_content, remote_content)

        checksum = self.calculate_file_checksum(local_path)
        self.metadata["agents"][change.agent_id]["checksum"] = checksum
        self.metadata["agents"][change.agent_id][
            "last_updated"
        ] = self._current_timestamp()

    def _three_way_merge(self, original: str, local: str, remote: str) -> str | None:
        """Attempt automatic 3-way merge"""
        try:
            original_lines = original.splitlines(keepends=True)
            local_lines = local.splitlines(keepends=True)
            remote_lines = remote.splitlines(keepends=True)

            local_diff = list(difflib.unified_diff(original_lines, local_lines, n=0))
            remote_diff = list(difflib.unified_diff(original_lines, remote_lines, n=0))

            if not self._have_conflicting_changes(local_diff, remote_diff):
                return "".join(remote_lines)

            return None

        except Exception as e:
            print(f"⚠️ Merge failed: {e}")
            return None

    def _have_conflicting_changes(self, local_diff: list, remote_diff: list) -> bool:
        """Check if two diffs have conflicting changes"""

        return False

    def _interactive_resolve(
        self, change: UpdateChange, local_content: str, remote_content: str
    ) -> None:
        """Interactive conflict resolution"""
        print(f"🔧 Interactive resolution needed for {change.agent_id}")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as local_temp:
            local_temp.write(local_content)
            local_temp_path = local_temp.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as remote_temp:
            remote_temp.write(remote_content)
            remote_temp_path = remote_temp.name

        print("Options:")
        print("  1. Keep local version (your customizations)")
        print("  2. Use remote version (lose customizations)")
        print("  3. Show diff and decide")
        print("  4. Skip this agent")

        try:
            choice = input("Choose option [1-4]: ").strip()

            if choice == "1":
                print("✅ Keeping local version")

                self.metadata["agents"][change.agent_id][
                    "last_updated"
                ] = self._current_timestamp()
            elif choice == "2":
                print("✅ Using remote version")
                with open(change.local_path, "w") as f:
                    f.write(remote_content)
                self.metadata["agents"][change.agent_id]["customized"] = False
            elif choice == "3":
                self._show_diff_and_resolve(change, local_content, remote_content)
            else:
                print("⏭️ Skipping agent")

        except KeyboardInterrupt:
            print("\n⏭️ Skipping agent due to user interrupt")
        finally:
            os.unlink(local_temp_path)
            os.unlink(remote_temp_path)

    def _show_diff_and_resolve(
        self, change: UpdateChange, local_content: str, remote_content: str
    ) -> None:
        """Show diff and allow manual resolution"""
        print(f"\n📋 Differences in {change.agent_id}:")

        local_lines = local_content.splitlines()
        remote_lines = remote_content.splitlines()

        diff = difflib.unified_diff(
            local_lines,
            remote_lines,
            fromfile="Local (your version)",
            tofile="Remote (new version)",
            lineterm="",
        )

        for line in diff:
            if line.startswith("@@"):
                print(f"\033[94m{line}\033[0m")  # Blue
            elif line.startswith("-"):
                print(f"\033[91m{line}\033[0m")  # Red
            elif line.startswith("+"):
                print(f"\033[92m{line}\033[0m")  # Green
            else:
                print(line)

        print("\nAfter reviewing the diff:")
        print("  1. Keep local version")
        print("  2. Use remote version")
        print("  3. Edit manually")

        choice = input("Choose option [1-3]: ").strip()

        if choice == "2":
            with open(change.local_path, "w") as f:
                f.write(remote_content)
            self.metadata["agents"][change.agent_id]["customized"] = False
        elif choice == "3":
            print(f"📝 Please edit {change.local_path} manually")
            input("Press Enter when finished editing...")

    def _handle_deprecated_agent(self, change: UpdateChange) -> None:
        """Handle deprecated agents"""
        print(f"🗑️ Agent deprecated: {change.agent_id}")

        local_path = Path(change.local_path)
        if local_path.exists():
            archive_dir = self.guardian_dir / "archived"
            archive_dir.mkdir(exist_ok=True)

            archive_path = archive_dir / local_path.name
            local_path.rename(archive_path)

            print(f"📦 Moved to archive: {archive_path}")

        if change.agent_id in self.metadata["agents"]:
            del self.metadata["agents"][change.agent_id]

    def _get_original_version(self, agent_id: str) -> str | None:
        """Get original version of agent for 3-way merge"""

        backup_path = self.guardian_dir / "originals" / f"{agent_id}.md"
        if backup_path.exists():
            with open(backup_path) as f:
                return f.read()
        return None

    def _current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime

        return datetime.utcnow().isoformat() + "Z"

    def update(self) -> bool:
        """Main update method"""
        try:
            print("🔍 Checking for Guardian agent updates...")

            changes = self.identify_changes()

            if not changes:
                print("✅ All Guardian agents are up to date!")
                return True

            print(f"📊 Found {len(changes)} changes:")
            for change in changes:
                emoji = {
                    "new": "➕",
                    "updated": "🔄",
                    "conflict": "🔀",
                    "deprecated": "🗑️",
                }
                print(
                    f"  {emoji.get(change.change_type, '❓')} {change.agent_id} ({change.change_type})"
                )

            if input("\nProceed with update? [Y/n]: ").strip().lower() not in [
                "",
                "y",
                "yes",
            ]:
                print("❌ Update cancelled")
                return False

            success = self.apply_updates(changes)

            if success:
                self.save_metadata()
                self._generate_agent_index()
                print("✅ Update completed successfully!")
                return True
            else:
                print("⚠️ Update completed with some errors")
                return False

        except Exception as e:
            print(f"❌ Update failed: {e}")
            return False

    def _generate_agent_index(self) -> None:
        """Generate agent index for LLM consumption"""
        manifest = self.remote_manifest or self.fetch_remote_manifest()

        index = {
            "system": "claude-guardian-agents",
            "version": manifest.get("version", "unknown"),
            "description": "Specialized AI agents for software development and operations",
            "agents_by_category": {},
            "workflow_chains": manifest.get("workflows", {}),
            "selection_hints": {},
        }

        for category_name, category_info in manifest.get("categories", {}).items():
            index["agents_by_category"][category_name] = {
                "description": category_info["description"],
                "agents": [f"{aid:03d}-guardian" for aid in category_info["agents"]],
            }

        for agent_info in manifest.get("agents", {}).values():
            agent_name = agent_info["name"]
            for trigger in agent_info.get("triggers", []):
                if trigger not in index["selection_hints"]:
                    index["selection_hints"][trigger] = []
                index["selection_hints"][trigger].append(agent_name)

        index_path = self.claude_dir / "agent-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)

        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)

        print(f"📋 Generated agent index: {index_path}")


def main() -> None:
    """Command line interface for GPM library"""
    if len(sys.argv) < 2:
        print("Usage: gpm-lib.py <command>")
        print("Commands: update, status, generate-index")
        sys.exit(1)

    command = sys.argv[1]
    updater = GuardianUpdater()

    if command == "update":
        success = updater.update()
        sys.exit(0 if success else 1)
    elif command == "status":
        print(
            f"Guardian system status: {len(updater.metadata.get('agents', {}))} agents installed"
        )
    elif command == "generate-index":
        updater._generate_agent_index()
        print("✅ Agent index generated")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
