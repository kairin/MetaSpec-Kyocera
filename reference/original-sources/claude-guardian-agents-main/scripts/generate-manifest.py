#!/usr/bin/env python3
"""
Generate Correct Manifest - Creates accurate manifest.json from actual repository structure
"""


import json
import re
from pathlib import Path
from typing import Any


class ManifestGenerator:
    """Generate accurate manifest from repository structure"""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.agent_files: list = []
        self.categories: dict = {
            "strategy": {
                "name": "Strategic & Product",
                "description": "Product strategy, planning, and design agents",
                "agents": [],
            },
            "architecture": {
                "name": "Technical Architecture",
                "description": "System architecture and technical leadership agents",
                "agents": [],
            },
            "backend": {
                "name": "Backend Development",
                "description": "Backend, API, and database development agents",
                "agents": [],
            },
            "frontend": {
                "name": "Frontend Development",
                "description": "Frontend, UI, and web development agents",
                "agents": [],
            },
            "mobile": {
                "name": "Mobile Development",
                "description": "iOS, Android, and cross-platform mobile agents",
                "agents": [],
            },
            "quality": {
                "name": "Quality Engineering",
                "description": "Testing, QA, and quality assurance agents",
                "agents": [],
            },
            "devops": {
                "name": "DevOps & Infrastructure",
                "description": "DevOps, infrastructure, and deployment agents",
                "agents": [],
            },
            "security": {
                "name": "Security Operations",
                "description": "Security, compliance, and risk management agents",
                "agents": [],
            },
            "data": {
                "name": "Data Operations",
                "description": "Data engineering, analytics, and data management agents",
                "agents": [],
            },
            "operations": {
                "name": "IT Operations",
                "description": "IT operations, service management, and support agents",
                "agents": [],
            },
            "thinktank": {
                "name": "Think-Tank Reasoning",
                "description": "Parallel reasoning and problem-solving enhancement agents",
                "agents": [],
            },
        }

    def scan_repository(self) -> list[Path]:
        """Scan repository for all guardian agent files"""
        print("🔍 Scanning repository for Guardian agent files...")

        agent_pattern = "*guardian.md"
        specialized_agents = list(self.repo_root.glob(f"**/{agent_pattern}"))
        meta_agents = list(self.repo_root.glob("5-meta-agents/*.md"))
        self.agent_files = specialized_agents + meta_agents

        print(f"✅ Found {len(self.agent_files)} agent files")
        return self.agent_files

    def extract_agent_info(self, file_path: Path) -> dict | None:
        """Extract agent information from file"""
        try:
            filename = file_path.name
            id_match = re.match(r"(\d+)-", filename)
            if id_match:
                agent_id = id_match.group(1)
                agent_num = int(agent_id)
                category = self.categorize_agent(agent_num)
            else:
                # Handle meta-agents which do not have numerical IDs
                if "5-meta-agents" in str(file_path):
                    agent_id = filename.replace(
                        ".md", ""
                    )  # Use filename as ID for meta-agents
                    agent_num = (
                        0  # Assign a dummy number or handle categorization differently
                    )
                    category = "meta-agents"
                    if category not in self.categories:
                        self.categories[category] = {
                            "name": "Meta Agents",
                            "description": "Agents for orchestration and codebase analysis",
                            "agents": [],
                        }
                else:
                    agent_id = "unknown"
                    agent_num = 0  # Default to 0 or handle as error
                    category = "generic"  # Or a specific error category

            name = filename.replace(".md", "")

            title = self.generate_title(name)

            rel_path = file_path.relative_to(self.repo_root)

            tools, triggers = self.parse_agent_file(file_path)

            complexity = self.determine_complexity(name, triggers)

            return {
                "name": name,
                "title": title,
                "category": category,
                "complexity": complexity,
                "path": str(rel_path),
                "research_foundations": self.count_research_foundations(file_path),
                "tools": tools,
                "triggers": triggers,
            }

        except Exception as e:
            print(f"⚠️ Error processing {file_path}: {e}")

        return None  # Add explicit return for type safety

    def categorize_agent(self, agent_num: int) -> str:
        """Categorize agent based on ID number"""
        if 1 <= agent_num <= 30:
            if agent_num <= 6:
                return "strategy"
            elif 21 <= agent_num <= 25:
                return "strategy"
            else:
                return "strategy"
        elif 41 <= agent_num <= 45:
            return "architecture"
        elif 61 <= agent_num <= 69:
            if 61 <= agent_num <= 63:
                return "backend"
            elif 64 <= agent_num <= 66:
                return "frontend"
            elif 67 <= agent_num <= 69:
                return "mobile"
            else:
                return "development"
        elif 71 <= agent_num <= 73:
            return "quality"
        elif 81 <= agent_num <= 83:
            return "devops"
        elif agent_num == 91:
            return "operations"
        elif 92 <= agent_num <= 94:
            return "security"
        elif 95 <= agent_num <= 97:
            return "data"
        elif 98 <= agent_num <= 100:
            return "operations"
        elif 101 <= agent_num <= 120:
            return "thinktank"
        else:
            return "generic"

    def generate_title(self, name: str) -> str:
        """Generate human-readable title from agent name"""

        title = re.sub(r"^\d+-", "", name)
        title = re.sub(r"-guardian$", "", title)

        title = title.replace("-", " ").title()

        return f"{title} Guardian"

    def parse_agent_file(self, file_path: Path) -> tuple:
        """Parse agent file to extract tools and triggers"""
        tools = ["web_search", "web_fetch", "write", "read"]  # Default tools
        triggers = []

        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

                tools_match = re.search(r"tools:\s*\[(.*?)\]", content, re.MULTILINE)
                if tools_match:
                    tools_str = tools_match.group(1)
                    tools = [tool.strip().strip("'\"") for tool in tools_str.split(",")]

                desc_match = re.search(r"description:\s*([^\n]+)", content)
                if desc_match:
                    description = desc_match.group(1)

                    trigger_patterns = [
                        r"(\w+\s+\w+)\s+tasks",
                        r"Use for\s+([^.]+)",
                        r"MUST BE USED for\s+([^.]+)",
                    ]

                    for pattern in trigger_patterns:
                        matches = re.findall(pattern, description, re.IGNORECASE)
                        triggers.extend([match.strip().lower() for match in matches])

                if "backend" in file_path.name:
                    triggers.extend(
                        ["backend development", "api development", "database design"]
                    )
                elif "frontend" in file_path.name:
                    triggers.extend(
                        ["frontend development", "ui development", "web development"]
                    )
                elif "mobile" in file_path.name:
                    triggers.extend(
                        ["mobile development", "ios development", "android development"]
                    )
                elif "quality" in file_path.name:
                    triggers.extend(["testing", "quality assurance", "test automation"])
                elif "devops" in file_path.name:
                    triggers.extend(["devops", "infrastructure", "deployment", "ci/cd"])
                elif "security" in file_path.name:
                    triggers.extend(["security", "compliance", "risk management"])

        except Exception as e:
            print(f"⚠️ Could not parse {file_path}: {e}")

        return tools, list(set(triggers))

    def determine_complexity(self, name: str, triggers: list[str]) -> str:
        """Determine agent complexity based on name and role"""
        if "director" in name or "leadership" in name or "principal" in name:
            return "complex"
        elif "senior" in name:
            return "complex"
        elif "junior" in name:
            return "simple"
        else:
            return "moderate"

    def count_research_foundations(self, file_path: Path) -> int:
        """Count research foundations in agent file"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

                research_count = len(
                    re.findall(r"##\s*📚\s*Research Foundation", content)
                )
                if research_count > 0:
                    primary_count = len(re.findall(r"###\s*Primary Research", content))
                    return max(3, primary_count)  # Minimum 3 if research section exists
                else:
                    return 0
        except OSError:
            return 0

    def generate_manifest(self) -> dict:
        """Generate complete manifest from repository scan"""
        print("🔧 Generating complete manifest...")

        agent_files = self.scan_repository()

        agents = {}

        for file_path in agent_files:
            agent_info = self.extract_agent_info(file_path)
            if agent_info:
                agent_id = agent_info[
                    "name"
                ]  # Use the full name as ID for all agents for consistency
                agents[agent_id] = agent_info

                category = agent_info["category"]
                if category in self.categories:
                    self.categories[category]["agents"].append(agent_id)

        manifest = {
            "name": "claude-guardian-agents",
            "version": "2.3.0",
            "description": "Comprehensive system of specialized AI agents for software development and project management",
            "repository": "https://github.com/kairin/claude-guardian-agents",
            "license": "MIT",
            "updated_at": "2025-09-11T10:30:00Z",
            "categories": self.categories,
            "agents": agents,
            "integration": {
                "claude_code": {
                    "supported": True,
                    "agent_path": ".claude/agents/",
                    "index_file": "agent-index.json",
                    "auto_selection": True,
                },
                "spec_kit": {
                    "supported": True,
                    "repository": "https://github.com/kairin/spec-kit",
                    "sync_command": "gpm sync-specs",
                    "spec_path": "specs/",
                },
            },
            "metadata": {
                "total_agents": len(agents),
                "research_papers": sum(
                    [info["research_foundations"] for info in agents.values()]
                ),
                "supported_languages": 7,
                "min_gpm_version": "1.0.0",
            },
        }

        print(f"✅ Generated manifest with {len(agents)} agents")
        return manifest

    def save_manifest(
        self, manifest: dict[str, Any], output_path: str = "manifest.json"
    ) -> None:
        """Save manifest to file"""
        output_file = self.repo_root / output_path
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved manifest to {output_file}")


def main() -> None:
    """Generate manifest from current repository"""
    generator = ManifestGenerator()
    manifest = generator.generate_manifest()
    generator.save_manifest(manifest)

    print("\n📋 Manifest Summary:")
    print(f"  Total Agents: {manifest['metadata']['total_agents']}")
    print(f"  Categories: {len(manifest['categories'])}")
    #    print(f"  Workflows: {len(manifest['workflows'])}")

    print("\n📊 Category Breakdown:")
    for cat_info in manifest["categories"].values():
        print(f"  {cat_info['name']}: {len(cat_info['agents'])} agents")


if __name__ == "__main__":
    main()
