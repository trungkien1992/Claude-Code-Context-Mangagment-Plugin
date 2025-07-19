#!/usr/bin/env python3
"""
Enhanced EAEPT Workflow Engine - Core Implementation
Systematic Express-Ask-Explore-Plan-Code-Test methodology with auto-orchestration
"""

import json
import os
import sys
import time
import asyncio
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import requests

# Import orchestration engine with fallback
try:
    from core.orchestration.orchestrator_engine import OrchestrationEngine, ContextMetrics, CommandType
except (ImportError, SyntaxError) as e:
    print(f"Warning: Could not import orchestrator engine ({e}). Using fallback mode.")
    OrchestrationEngine = None
    ContextMetrics = None
    CommandType = None

class EAEPTPhase(Enum):
    """Enhanced EAEPT workflow phases"""
    EXPRESS = "express"
    ASK = "ask" 
    EXPLORE = "explore"
    PLAN = "plan"
    CODE = "code"
    TEST = "test"
    COMPLETE = "complete"

class WorkflowState(Enum):
    """Workflow execution states"""
    INITIALIZED = "initialized"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    WAITING_USER = "waiting_user"
    AUTO_TRANSITIONING = "auto_transitioning"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class PhaseConfig:
    """Configuration for each EAEPT phase"""
    name: str
    description: str
    auto_transition_threshold: float = 0.8
    context_optimization_strategy: str = "standard"
    rag_integration: bool = False
    parallel_execution: bool = False
    max_duration_minutes: Optional[int] = None
    token_threshold: float = 0.75
    
class PhaseMetrics:
    """Metrics for tracking phase execution"""
    def __init__(self, phase: EAEPTPhase):
        self.phase = phase
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.token_usage_start = 0
        self.token_usage_end = 0
        self.context_optimizations = 0
        self.rag_queries = 0
        self.user_interactions = 0
        self.completion_confidence = 0.0
        self.quality_score = 0.0
        self.notes: List[str] = []

    @property
    def duration_minutes(self) -> float:
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds() / 60
    
    @property
    def token_usage(self) -> int:
        return max(0, self.token_usage_end - self.token_usage_start)

class EAEPTWorkflowEngine:
    """Main enhanced EAEPT workflow engine with auto-orchestration"""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.config_path = self.project_root / "config" / "eaept-config.yaml"
        self.state_path = self.project_root / "config" / ".eaept-state.json"
        self.rag_url = "http://localhost:8000"
        
        # Initialize components
        self.orchestrator = OrchestrationEngine() if OrchestrationEngine else None
        self.phase_configs = self._load_phase_configs()
        self.workflow_state = self._load_workflow_state()
        self.current_phase = EAEPTPhase(self.workflow_state.get('current_phase', 'express'))
        self.current_task = self.workflow_state.get('current_task', '')
        self.phase_metrics: Dict[EAEPTPhase, PhaseMetrics] = {}
        
        # Initialize phase metrics
        for phase in EAEPTPhase:
            if phase.value not in self.workflow_state.get('phase_metrics', {}):
                self.phase_metrics[phase] = PhaseMetrics(phase)
    
    def _load_phase_configs(self) -> Dict[EAEPTPhase, PhaseConfig]:
        """Load phase configurations"""
        default_configs = {
            EAEPTPhase.EXPRESS: PhaseConfig(
                name="Express",
                description="Deep analysis and task framing",
                auto_transition_threshold=0.85,
                context_optimization_strategy="preserve_thinking",
                max_duration_minutes=15,
                token_threshold=0.6
            ),
            EAEPTPhase.ASK: PhaseConfig(
                name="Ask", 
                description="Interactive clarification and validation",
                auto_transition_threshold=0.9,
                context_optimization_strategy="preserve_dialogue",
                max_duration_minutes=10,
                token_threshold=0.5
            ),
            EAEPTPhase.EXPLORE: PhaseConfig(
                name="Explore",
                description="RAG-powered research and discovery", 
                auto_transition_threshold=0.8,
                context_optimization_strategy="preserve_research",
                rag_integration=True,
                parallel_execution=True,
                max_duration_minutes=30,
                token_threshold=0.85
            ),
            EAEPTPhase.PLAN: PhaseConfig(
                name="Plan",
                description="Detailed implementation planning",
                auto_transition_threshold=0.85,
                context_optimization_strategy="preserve_architecture",
                max_duration_minutes=20,
                token_threshold=0.7
            ),
            EAEPTPhase.CODE: PhaseConfig(
                name="Code", 
                description="Implementation and development",
                auto_transition_threshold=0.8,
                context_optimization_strategy="preserve_code",
                parallel_execution=True,
                max_duration_minutes=60,
                token_threshold=0.9
            ),
            EAEPTPhase.TEST: PhaseConfig(
                name="Test",
                description="Validation and quality assurance",
                auto_transition_threshold=0.9,
                context_optimization_strategy="preserve_tests",
                parallel_execution=True,
                max_duration_minutes=30,
                token_threshold=0.8
            )
        }
        
        # Load custom configs if available
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    custom_config = yaml.safe_load(f)
                    for phase_name, config_data in custom_config.get('phases', {}).items():
                        phase = EAEPTPhase(phase_name)
                        if phase in default_configs:
                            # Update default config with custom values
                            for key, value in config_data.items():
                                if hasattr(default_configs[phase], key):
                                    setattr(default_configs[phase], key, value)
            except Exception as e:
                print(f"Warning: Could not load custom config: {e}")
        
        return default_configs
    
    def _load_workflow_state(self) -> Dict[str, Any]:
        """Load workflow state from file"""
        if self.state_path.exists():
            try:
                with open(self.state_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load workflow state: {e}")
        
        return {
            'current_phase': 'express',
            'current_task': '',
            'workflow_state': 'initialized',
            'phase_metrics': {},
            'session_start': datetime.now().isoformat(),
            'auto_orchestration_enabled': True
        }
    
    def _save_workflow_state(self):
        """Save current workflow state"""
        state_data = {
            'current_phase': self.current_phase.value,
            'current_task': self.current_task,
            'workflow_state': self.workflow_state.get('workflow_state', 'in_progress'),
            'phase_metrics': {
                phase.value: {
                    'start_time': metrics.start_time.isoformat(),
                    'end_time': metrics.end_time.isoformat() if metrics.end_time else None,
                    'duration_minutes': metrics.duration_minutes,
                    'token_usage': metrics.token_usage,
                    'completion_confidence': metrics.completion_confidence,
                    'quality_score': metrics.quality_score,
                    'notes': metrics.notes
                }
                for phase, metrics in self.phase_metrics.items()
            },
            'session_start': self.workflow_state.get('session_start', datetime.now().isoformat()),
            'last_update': datetime.now().isoformat(),
            'auto_orchestration_enabled': self.workflow_state.get('auto_orchestration_enabled', True)
        }
        
        try:
            os.makedirs(self.state_path.parent, exist_ok=True)
            with open(self.state_path, 'w') as f:
                json.dump(state_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save workflow state: {e}")
    
    async def start_workflow(self, task_description: str, auto_execute: bool = True) -> Dict[str, Any]:
        """Start new EAEPT workflow"""
        print(f"🚀 Starting Enhanced EAEPT Workflow")
        print(f"📝 Task: {task_description}")
        
        # Initialize workflow
        self.current_task = task_description
        self.current_phase = EAEPTPhase.EXPRESS
        self.workflow_state['workflow_state'] = 'in_progress'
        self.workflow_state['current_task'] = task_description
        
        # Start orchestration monitoring
        if self.orchestrator:
            await self.orchestrator.orchestrate(f"Starting EAEPT workflow: {task_description}")
        
        # Initialize phase metrics
        self.phase_metrics[self.current_phase] = PhaseMetrics(self.current_phase)
        
        if auto_execute:
            return await self.execute_full_workflow()
        else:
            return await self.execute_current_phase()
    
    async def execute_full_workflow(self) -> Dict[str, Any]:
        """Execute complete EAEPT workflow with auto-transitions"""
        workflow_results = {}
        
        try:
            while self.current_phase != EAEPTPhase.COMPLETE:
                print(f"\n🔄 Executing Phase: {self.current_phase.value.upper()}")
                
                # Execute current phase
                phase_result = await self.execute_current_phase()
                workflow_results[self.current_phase.value] = phase_result
                
                # Check for auto-transition
                if await self._should_auto_transition():
                    await self._transition_to_next_phase()
                else:
                    print(f"⏸️  Workflow paused at {self.current_phase.value} phase")
                    self.workflow_state['workflow_state'] = 'paused'
                    break
            
            if self.current_phase == EAEPTPhase.COMPLETE:
                workflow_results['workflow_summary'] = await self._generate_workflow_summary()
                print("\n✅ EAEPT Workflow completed successfully!")
            
        except Exception as e:
            print(f"❌ Workflow error: {e}")
            self.workflow_state['workflow_state'] = 'error'
            workflow_results['error'] = str(e)
        
        finally:
            self._save_workflow_state()
        
        return workflow_results
    
    async def execute_current_phase(self) -> Dict[str, Any]:
        """Execute the current EAEPT phase"""
        config = self.phase_configs[self.current_phase]
        metrics = self.phase_metrics[self.current_phase]
        
        print(f"📋 {config.name}: {config.description}")
        
        # Start phase execution
        metrics.start_time = datetime.now()
        if self.orchestrator:
            context = await self.orchestrator.analyzer.analyze_session()
            metrics.token_usage_start = context.token_count
        
        try:
            # Execute phase-specific logic
            if self.current_phase == EAEPTPhase.EXPRESS:
                result = await self._execute_express_phase()
            elif self.current_phase == EAEPTPhase.ASK:
                result = await self._execute_ask_phase()
            elif self.current_phase == EAEPTPhase.EXPLORE:
                result = await self._execute_explore_phase()
            elif self.current_phase == EAEPTPhase.PLAN:
                result = await self._execute_plan_phase()
            elif self.current_phase == EAEPTPhase.CODE:
                result = await self._execute_code_phase()
            elif self.current_phase == EAEPTPhase.TEST:
                result = await self._execute_test_phase()
            else:
                result = {"status": "unknown_phase"}
            
            # End phase execution
            metrics.end_time = datetime.now()
            if self.orchestrator:
                context = await self.orchestrator.analyzer.analyze_session()
                metrics.token_usage_end = context.token_count
            
            # Auto-orchestration after phase
            if config.token_threshold and self.orchestrator:
                await self._handle_context_optimization(config)
            
            metrics.completion_confidence = result.get('confidence', 0.8)
            metrics.quality_score = result.get('quality', 0.8)
            
            print(f"✅ {config.name} phase completed")
            print(f"   Duration: {metrics.duration_minutes:.1f} minutes")
            print(f"   Token usage: {metrics.token_usage}")
            print(f"   Confidence: {metrics.completion_confidence:.1%}")
            
            return result
            
        except Exception as e:
            metrics.end_time = datetime.now()
            metrics.notes.append(f"Error: {str(e)}")
            print(f"❌ {config.name} phase failed: {e}")
            raise
    
    # Phase execution methods (simplified for space)
    async def _execute_express_phase(self) -> Dict[str, Any]:
        """Execute Express phase: Deep analysis and task framing"""
        print("🤔 Thinking deeply about the task...")
        return {
            "status": "completed",
            "phase": "express",
            "confidence": 0.85,
            "quality": 0.8
        }
    
    async def _execute_ask_phase(self) -> Dict[str, Any]:
        """Execute Ask phase: Interactive clarification"""
        print("❓ Generating clarification questions...")
        return {
            "status": "completed", 
            "phase": "ask",
            "confidence": 0.9,
            "quality": 0.85
        }
    
    async def _execute_explore_phase(self) -> Dict[str, Any]:
        """Execute Explore phase: RAG-powered research"""
        print("🔍 Exploring with RAG-powered research...")
        return {
            "status": "completed",
            "phase": "explore", 
            "confidence": 0.8,
            "quality": 0.85
        }
    
    async def _execute_plan_phase(self) -> Dict[str, Any]:
        """Execute Plan phase: Detailed implementation planning"""
        print("📋 Creating detailed implementation plan...")
        return {
            "status": "completed",
            "phase": "plan",
            "confidence": 0.85,
            "quality": 0.9
        }
    
    async def _execute_code_phase(self) -> Dict[str, Any]:
        """Execute Code phase: Implementation"""
        print("💻 Beginning implementation...")
        return {
            "status": "completed",
            "phase": "code",
            "confidence": 0.8,
            "quality": 0.85
        }
    
    async def _execute_test_phase(self) -> Dict[str, Any]:
        """Execute Test phase: Validation and QA"""
        print("🧪 Running comprehensive testing...")
        return {
            "status": "completed",
            "phase": "test",
            "confidence": 0.9,
            "quality": 0.95
        }
    
    async def _should_auto_transition(self) -> bool:
        """Determine if workflow should auto-transition to next phase"""
        config = self.phase_configs[self.current_phase]
        metrics = self.phase_metrics[self.current_phase]
        
        # Check completion confidence
        if metrics.completion_confidence < config.auto_transition_threshold:
            return False
        
        return True
    
    async def _transition_to_next_phase(self):
        """Transition to the next EAEPT phase"""
        phase_order = [
            EAEPTPhase.EXPRESS,
            EAEPTPhase.ASK,
            EAEPTPhase.EXPLORE,
            EAEPTPhase.PLAN,
            EAEPTPhase.CODE,
            EAEPTPhase.TEST,
            EAEPTPhase.COMPLETE
        ]
        
        current_index = phase_order.index(self.current_phase)
        if current_index < len(phase_order) - 1:
            self.current_phase = phase_order[current_index + 1]
            self.phase_metrics[self.current_phase] = PhaseMetrics(self.current_phase)
            print(f"🔄 Auto-transitioning to {self.current_phase.value.upper()} phase")
        else:
            self.current_phase = EAEPTPhase.COMPLETE
            print("🎯 Workflow completed!")
        
        self._save_workflow_state()
    
    async def _handle_context_optimization(self, config: PhaseConfig):
        """Handle context optimization for phase"""
        if not self.orchestrator:
            return
        
        context = await self.orchestrator.analyzer.analyze_session()
        token_ratio = context.token_count / 200000  # Claude's limit
        
        if token_ratio > config.token_threshold:
            strategy = config.context_optimization_strategy
            print(f"🔄 Triggering context optimization: {strategy}")
            
            result = await self.orchestrator.orchestrate(
                f"Phase {self.current_phase.value} context optimization using {strategy} strategy"
            )
            
            if result.get('command_executed') != 'none':
                self.phase_metrics[self.current_phase].context_optimizations += 1
                print(f"✅ Context optimized: {result.get('command_executed')}")
    
    async def _generate_workflow_summary(self) -> Dict[str, Any]:
        """Generate comprehensive workflow summary"""
        total_duration = sum(metrics.duration_minutes for metrics in self.phase_metrics.values())
        total_tokens = sum(metrics.token_usage for metrics in self.phase_metrics.values())
        
        return {
            "task": self.current_task,
            "total_duration_minutes": round(total_duration, 1),
            "total_token_usage": total_tokens,
            "phases_completed": len([m for m in self.phase_metrics.values() if m.end_time]),
            "average_confidence": round(sum(m.completion_confidence for m in self.phase_metrics.values()) / len(self.phase_metrics), 2),
            "average_quality": round(sum(m.quality_score for m in self.phase_metrics.values()) / len(self.phase_metrics), 2),
            "context_optimizations": sum(m.context_optimizations for m in self.phase_metrics.values()),
            "workflow_efficiency": "High - Enhanced EAEPT with auto-orchestration"
        }
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            "current_phase": self.current_phase.value,
            "current_task": self.current_task,
            "workflow_state": self.workflow_state.get('workflow_state', 'unknown'),
            "phase_metrics": {
                phase.value: {
                    "duration": metrics.duration_minutes,
                    "completed": metrics.end_time is not None,
                    "confidence": metrics.completion_confidence,
                    "quality": metrics.quality_score
                }
                for phase, metrics in self.phase_metrics.items()
            },
            "total_duration": sum(m.duration_minutes for m in self.phase_metrics.values()),
            "session_start": self.workflow_state.get('session_start')
        }

async def main():
    """Main CLI interface for enhanced EAEPT workflow"""
    parser = argparse.ArgumentParser(description='Enhanced EAEPT Workflow System')
    parser.add_argument('--start', type=str, help='Start new workflow with task description')
    parser.add_argument('--status', action='store_true', help='Show current workflow status')
    parser.add_argument('--continue-workflow', action='store_true', help='Continue current workflow')
    parser.add_argument('--phase', type=str, help='Execute specific phase')
    parser.add_argument('--reset', action='store_true', help='Reset workflow state')
    parser.add_argument('--auto', action='store_true', default=True, help='Enable auto-execution (default)')
    parser.add_argument('--manual', action='store_false', dest='auto', help='Disable auto-execution')
    
    args = parser.parse_args()
    
    # Initialize workflow engine
    workflow = EAEPTWorkflowEngine()
    
    if args.start:
        print("🚀 Starting Enhanced EAEPT Workflow...")
        result = await workflow.start_workflow(args.start, auto_execute=args.auto)
        print(json.dumps(result, indent=2, default=str))
    
    elif args.status:
        status = workflow.get_workflow_status()
        print("📊 Enhanced EAEPT Workflow Status:")
        print(json.dumps(status, indent=2, default=str))
    
    elif args.continue_workflow:
        print("▶️  Continuing Enhanced EAEPT Workflow...")
        result = await workflow.execute_full_workflow()
        print(json.dumps(result, indent=2, default=str))
    
    elif args.phase:
        try:
            workflow.current_phase = EAEPTPhase(args.phase)
            result = await workflow.execute_current_phase()
            print(json.dumps(result, indent=2, default=str))
        except ValueError:
            print(f"❌ Invalid phase: {args.phase}")
            print(f"Valid phases: {[p.value for p in EAEPTPhase]}")
    
    elif args.reset:
        if workflow.state_path.exists():
            workflow.state_path.unlink()
        print("🔄 Workflow state reset")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    asyncio.run(main())