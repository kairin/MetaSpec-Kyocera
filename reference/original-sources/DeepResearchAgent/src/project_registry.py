"""
Project Registry System for DeepResearchAgent

Manages multiple projects, their configurations, and research history.
Ensures clean separation between different projects.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from dataclasses import dataclass, asdict
from enum import Enum


class ProjectStatus(Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    INACTIVE = "inactive"


@dataclass
class ResearchSession:
    """Represents a single research session for a project."""
    id: str
    timestamp: str
    task: str
    config_used: str
    results_summary: str
    output_files: list[str]
    status: str  # "completed", "failed", "in_progress"


@dataclass
class Project:
    """Represents a project in the registry."""
    id: str
    name: str
    path: str
    description: str
    status: ProjectStatus
    config_file: str
    created_at: str
    last_researched_at: str | None
    research_sessions: list[ResearchSession]
    tags: list[str]
    metadata: dict[str, Any]


class ProjectRegistry:
    """Manages the project registry and research history."""

    def __init__(self, registry_path: str | None = None):
        if registry_path is None:
            # Default to DeepResearchAgent root
            root = Path(__file__).resolve().parents[1]
            self.registry_path = root / "project_registry.json"
        else:
            self.registry_path = Path(registry_path)

        self.projects: dict[str, Project] = {}
        self._load_registry()

    def _load_registry(self):
        """Load project registry from file."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)

                for project_data in data.get('projects', []):
                    # Convert string status back to enum
                    project_data['status'] = ProjectStatus(
                        project_data['status'])

                    # Convert research sessions
                    sessions = []
                    for session_data in project_data.get(
                            'research_sessions', []):
                        sessions.append(ResearchSession(**session_data))
                    project_data['research_sessions'] = sessions

                    project = Project(**project_data)
                    self.projects[project.id] = project

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load registry: {e}")
                self.projects = {}

    def _save_registry(self):
        """Save project registry to file."""
        data = {
            'version': '1.0',
            'last_updated': datetime.now().isoformat(),
            'projects': []
        }

        for project in self.projects.values():
            project_dict = asdict(project)
            # Convert enum to string
            project_dict['status'] = project.status.value
            data['projects'].append(project_dict)

        # Ensure directory exists
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def add_project(self, name: str, path: str, description: str = "",
                    config_file: str = "configs/config_cli_fallback.py",
                    tags: list[str] | None = None) -> str:
        """Add a new project to the registry."""
        # Validate path exists
        if not os.path.exists(path):
            raise ValueError(f"Project path does not exist: {path}")

        # Generate unique ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_id = f"{name.lower().replace(' ', '_')}_{timestamp}"

        project = Project(
            id=project_id,
            name=name,
            path=path,
            description=description,
            status=ProjectStatus.ACTIVE,
            config_file=config_file,
            created_at=datetime.now().isoformat(),
            last_researched_at=None,
            research_sessions=[],
            tags=tags or [],
            metadata={}
        )

        self.projects[project_id] = project
        self._save_registry()
        return project_id

    def get_project(self, project_id: str) -> Project | None:
        """Get a project by ID."""
        return self.projects.get(project_id)

    def list_projects(self, status_filter: ProjectStatus | None = None
                      ) -> list[Project]:
        """List all projects, optionally filtered by status."""
        projects = list(self.projects.values())
        if status_filter:
            projects = [p for p in projects if p.status == status_filter]
        return sorted(projects, key=lambda p: p.created_at, reverse=True)

    def update_project_status(self, project_id: str, status: ProjectStatus):
        """Update project status."""
        if project_id in self.projects:
            self.projects[project_id].status = status
            self._save_registry()

    def add_research_session(self, project_id: str, task: str,
                             config_used: str, results_summary: str,
                             output_files: list[str], status: str) -> str:
        """Add a research session to a project."""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")

        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        session = ResearchSession(
            id=session_id,
            timestamp=datetime.now().isoformat(),
            task=task,
            config_used=config_used,
            results_summary=results_summary,
            output_files=output_files,
            status=status
        )

        self.projects[project_id].research_sessions.append(session)
        self.projects[project_id].last_researched_at = session.timestamp
        self._save_registry()

        return session_id

    def get_project_research_history(self, project_id: str
                                     ) -> list[ResearchSession]:
        """Get research history for a project."""
        if project_id not in self.projects:
            return []
        return self.projects[project_id].research_sessions

    def remove_project(self, project_id: str):
        """Remove a project from registry."""
        if project_id in self.projects:
            del self.projects[project_id]
            self._save_registry()

    def get_projects_by_tag(self, tag: str) -> list[Project]:
        """Get projects by tag."""
        return [p for p in self.projects.values() if tag in p.tags]

    def search_projects(self, query: str) -> list[Project]:
        """Search projects by name or description."""
        query_lower = query.lower()
        return [p for p in self.projects.values()
                if query_lower in p.name.lower() or
                query_lower in p.description.lower()]


# Global registry instance
project_registry = ProjectRegistry()
