"""
CLI Commands for Project Management in DeepResearchAgent
"""

import os

from src.project_registry import project_registry, ProjectStatus


def add_project_command(args):
    """Add a new project to the registry."""
    try:
        # Validate path
        if not os.path.exists(args.path):
            print(f"❌ Error: Path does not exist: {args.path}")
            return

        # Add project
        project_id = project_registry.add_project(
            name=args.name,
            path=args.path,
            description=args.description or "",
            config_file=args.config or "configs/config_cli_fallback.py",
            tags=args.tags or []
        )

        print("✅ Project added successfully!")
        print(f"   ID: {project_id}")
        print(f"   Name: {args.name}")
        print(f"   Path: {args.path}")

    except Exception as e:
        print(f"❌ Error adding project: {e}")


def list_projects_command(args):
    """List all projects in the registry."""
    projects = project_registry.list_projects()

    if not projects:
        print("📝 No projects found. Add your first project with:")
        print("   uv run python main.py --project-add \"My Project\"")
        print("   /path/to/project")
        return

    print(f"📋 Found {len(projects)} project(s):\n")

    for project in projects:
        status_icon = {
            ProjectStatus.ACTIVE: "🟢",
            ProjectStatus.ARCHIVED: "📦",
            ProjectStatus.INACTIVE: "⚪"
        }.get(project.status, "❓")

        print(f"{status_icon} {project.name}")
        print(f"   ID: {project.id}")
        print(f"   Path: {project.path}")
        print(f"   Status: {project.status.value}")
        print(f"   Sessions: {len(project.research_sessions)}")
        if project.last_researched_at:
            print(f"   Last Research: {project.last_researched_at[:19]}")
        if project.tags:
            print(f"   Tags: {', '.join(project.tags)}")
        print()


def research_command(args):
    """Run research on a specific project."""
    project = project_registry.get_project(args.project_id)

    if not project:
        print(f"❌ Project not found: {args.project_id}")
        print("\nAvailable projects:")
        list_projects_command(args)
        return

    print(f"🔬 Starting research on project: {project.name}")
    print(f"   Path: {project.path}")
    print(f"   Task: {args.task}")

    # Here we would integrate with the main agent
    # For now, just show what would happen
    print("\n⚠️  Research integration coming soon!")
    print("   This will run the agent with the project's configuration")
    # TODO: Integrate with main agent system


def history_command(args):
    """Show research history for a project."""
    project = project_registry.get_project(args.project_id)

    if not project:
        print(f"❌ Project not found: {args.project_id}")
        return

    sessions = project.research_sessions

    if not sessions:
        print(f"📝 No research history found for project: {project.name}")
        return

    print(f"📚 Research History for: {project.name}")
    print(f"   Total Sessions: {len(sessions)}\n")

    for session in sessions[-10:]:  # Show last 10 sessions
        status_icon = {
            "completed": "✅",
            "failed": "❌",
            "in_progress": "🔄"
        }.get(session.status, "❓")

        print(f"{status_icon} {session.timestamp[:19]}")
        task_preview = session.task[:60]
        if len(session.task) > 60:
            task_preview += "..."
        print(f"   Task: {task_preview}")
        print(f"   Config: {session.config_used}")
        print(f"   Status: {session.status}")
        if session.results_summary:
            summary_preview = session.results_summary[:100]
            if len(session.results_summary) > 100:
                summary_preview += "..."
            print(f"   Summary: {summary_preview}")
        print()


def remove_project_command(args):
    """Remove a project from the registry."""
    project = project_registry.get_project(args.project_id)

    if not project:
        print(f"❌ Project not found: {args.project_id}")
        return

    # Confirm removal
    confirm = input(f"Are you sure you want to remove project "
                    f"'{project.name}'? (y/N): ")
    if confirm.lower() not in ['y', 'yes']:
        print("❌ Removal cancelled.")
        return

    project_registry.remove_project(args.project_id)
    print(f"✅ Project removed: {project.name}")


def setup_project_cli(subparsers):
    """Setup project management CLI commands."""

    # Add project
    add_parser = subparsers.add_parser(
        'project-add',
        help='Add a new project to the registry'
    )
    add_parser.add_argument('name', help='Project name')
    add_parser.add_argument('path', help='Project path')
    add_parser.add_argument('-d', '--description', help='Project description')
    add_parser.add_argument('-c', '--config', help='Config file to use')
    add_parser.add_argument('-t', '--tags', nargs='*', help='Project tags')
    add_parser.set_defaults(func=add_project_command)

    # List projects
    list_parser = subparsers.add_parser(
        'project-list',
        help='List all projects in the registry'
    )
    list_parser.set_defaults(func=list_projects_command)

    # Research on project
    research_parser = subparsers.add_parser(
        'project-research',
        help='Run research on a specific project'
    )
    research_parser.add_argument('project_id', help='Project ID')
    research_parser.add_argument('task', help='Research task to perform')
    research_parser.set_defaults(func=research_command)

    # Show history
    history_parser = subparsers.add_parser(
        'project-history',
        help='Show research history for a project'
    )
    history_parser.add_argument('project_id', help='Project ID')
    history_parser.set_defaults(func=history_command)

    # Remove project
    remove_parser = subparsers.add_parser(
        'project-remove',
        help='Remove a project from the registry'
    )
    remove_parser.add_argument('project_id', help='Project ID')
    remove_parser.set_defaults(func=remove_project_command)


if __name__ == '__main__':
    # Test the registry
    print("🧪 Testing Project Registry...")

    # Add a test project
    try:
        project_id = project_registry.add_project(
            name="Test Project",
            path="/tmp/test",
            description="Test project for registry",
            tags=["test", "demo"]
        )
        print(f"✅ Test project added: {project_id}")

        # List projects
        projects = project_registry.list_projects()
        print(f"📋 Total projects: {len(projects)}")

        # Clean up
        project_registry.remove_project(project_id)
        print("✅ Test completed successfully")

    except Exception as e:
        print(f"❌ Test failed: {e}")
