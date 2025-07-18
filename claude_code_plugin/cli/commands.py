"""
Command-line interface for Claude Code Context Plugin
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Optional

from ..core.monitor import ContextMonitor
from ..core.orchestrator import PluginOrchestrator
from ..core.plugin_manager import PluginManager
from ..config import load_config


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser"""
    parser = argparse.ArgumentParser(
        prog='claude-code-plugin',
        description='Claude Code Context Plugin - Smart context management for AI development'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Start context monitoring')
    monitor_parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    monitor_parser.add_argument('--interval', type=int, default=30, help='Monitoring interval (seconds)')
    
    # Orchestrate command
    orchestrate_parser = subparsers.add_parser('orchestrate', help='Manual orchestration')
    orchestrate_parser.add_argument('--intent', required=True, help='Session intent description')
    orchestrate_parser.add_argument('--dry-run', action='store_true', help='Show recommendation without executing')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show current context status')
    status_parser.add_argument('--verbose', action='store_true', help='Show detailed information')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show session history')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of sessions to show')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize plugin configuration')
    init_parser.add_argument('--force', action='store_true', help='Overwrite existing configuration')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Manage plugin configuration')
    config_parser.add_argument('--show', action='store_true', help='Show current configuration')
    config_parser.add_argument('--edit', action='store_true', help='Edit configuration file')
    
    return parser


async def monitor_command(args):
    """Start context monitoring"""
    try:
        config = load_config()
        monitor = ContextMonitor(config)
        
        print("🔄 Starting Claude Code Context Monitor...")
        print(f"📊 Monitoring interval: {args.interval} seconds")
        print(f"🎯 Token limit: {config.get('token_limit', 200000)}")
        print("Press Ctrl+C to stop monitoring")
        
        if args.daemon:
            print("🔧 Running as daemon...")
            # In a real implementation, this would fork to background
            
        await monitor.start_monitoring(interval=args.interval)
        
    except KeyboardInterrupt:
        print("\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error during monitoring: {e}")
        return 1


async def orchestrate_command(args):
    """Handle manual orchestration"""
    try:
        config = load_config()
        orchestrator = PluginOrchestrator(config)
        
        print(f"🎯 Analyzing session intent: {args.intent}")
        
        # Get session data (in real implementation, this would collect from Claude Code)
        session_data = {
            'intent': args.intent,
            'timestamp': 'now',
            'context_size': 'estimated'
        }
        
        decision = await orchestrator.make_decision(session_data)
        
        print(f"🤖 Decision: {decision.get('action', 'No action needed')}")
        print(f"💡 Reasoning: {decision.get('reasoning', 'Standard analysis')}")
        print(f"⏱️  Estimated time: {decision.get('estimated_time', 'Unknown')}")
        
        if args.dry_run:
            print("🧪 Dry run mode - no commands executed")
        else:
            print("✅ Recommendation ready for execution")
            
    except Exception as e:
        print(f"❌ Error during orchestration: {e}")
        return 1


async def status_command(args):
    """Show current context status"""
    try:
        config = load_config()
        monitor = ContextMonitor(config)
        
        status = await monitor.get_status()
        
        print("📊 Claude Code Context Status")
        print("=" * 40)
        print(f"🔋 Token Usage: {status.get('token_usage', 'Unknown')}")
        print(f"📈 Burn Rate: {status.get('burn_rate', 'Unknown')}")
        print(f"⏰ Time to Limit: {status.get('time_to_limit', 'Unknown')}")
        print(f"🎯 Session Type: {status.get('session_type', 'Unknown')}")
        print(f"📂 Context Files: {status.get('context_files', 'Unknown')}")
        
        if args.verbose:
            print("\n🔍 Detailed Information:")
            print(f"📅 Session Start: {status.get('session_start', 'Unknown')}")
            print(f"🔄 Last Update: {status.get('last_update', 'Unknown')}")
            print(f"💾 Sessions Saved: {status.get('sessions_saved', 'Unknown')}")
            print(f"🎯 Confidence: {status.get('confidence', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ Error getting status: {e}")
        return 1


async def history_command(args):
    """Show session history"""
    try:
        config = load_config()
        manager = PluginManager(config)
        
        sessions = await manager.get_session_history(limit=args.limit)
        
        print(f"📅 Recent Sessions (last {args.limit}):")
        print("=" * 50)
        
        for i, session in enumerate(sessions, 1):
            print(f"{i}. {session.get('name', 'Unknown')} "
                  f"({session.get('duration', 'Unknown')} - "
                  f"{session.get('date', 'Unknown')})")
            
        if not sessions:
            print("No sessions found")
            
    except Exception as e:
        print(f"❌ Error getting history: {e}")
        return 1


def init_command(args):
    """Initialize plugin configuration"""
    try:
        config_path = Path.home() / '.claude' / 'claude-code-plugin' / 'config.py'
        
        if config_path.exists() and not args.force:
            print(f"❌ Configuration already exists at {config_path}")
            print("Use --force to overwrite")
            return 1
            
        # Create config directory
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create default configuration
        default_config = '''# Claude Code Context Plugin Configuration

PLUGIN_CONFIG = {
    'token_limit': 200000,
    'burn_rate_threshold': 150,
    'auto_compact_threshold': 0.85,
    'checkpoint_interval': 15,  # minutes
    'monitoring_enabled': True,
    'smart_suggestions': True
}

WORKFLOW_CONFIG = {
    'coding_session_detection': True,
    'debugging_mode_optimization': True,
    'architecture_session_persistence': True,
    'learning_from_patterns': True,
    'proactive_recommendations': True
}
'''
        
        with open(config_path, 'w') as f:
            f.write(default_config)
            
        print(f"✅ Configuration initialized at {config_path}")
        print("🔧 Edit the configuration file to customize settings")
        
    except Exception as e:
        print(f"❌ Error initializing configuration: {e}")
        return 1


def config_command(args):
    """Manage plugin configuration"""
    try:
        config_path = Path.home() / '.claude' / 'claude-code-plugin' / 'config.py'
        
        if args.show:
            if config_path.exists():
                print(f"📄 Configuration file: {config_path}")
                print("=" * 50)
                with open(config_path, 'r') as f:
                    print(f.read())
            else:
                print("❌ Configuration file not found")
                print("Run 'claude-code-plugin init' to create one")
                return 1
                
        elif args.edit:
            if config_path.exists():
                import os
                editor = os.environ.get('EDITOR', 'nano')
                os.system(f"{editor} {config_path}")
            else:
                print("❌ Configuration file not found")
                print("Run 'claude-code-plugin init' to create one")
                return 1
        else:
            print("❌ Use --show or --edit with config command")
            return 1
            
    except Exception as e:
        print(f"❌ Error managing configuration: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'monitor':
            return asyncio.run(monitor_command(args))
        elif args.command == 'orchestrate':
            return asyncio.run(orchestrate_command(args))
        elif args.command == 'status':
            return asyncio.run(status_command(args))
        elif args.command == 'history':
            return asyncio.run(history_command(args))
        elif args.command == 'init':
            return init_command(args)
        elif args.command == 'config':
            return config_command(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())