# Claude Orchestration Workflow - Usage Guide

## Quick Start

### Basic Usage
```bash
# Automatic orchestration (recommended)
orchestrator auto

# With user intent
orchestrator auto --intent "implementing new features"

# Force specific command
orchestrator digest
orchestrator compact
orchestrator hybrid

# Check status
orchestrator status
```

### Installation
```bash
# Make scripts executable (already done)
chmod +x /Users/admin/.claude/commands/orchestrator_cli.sh
chmod +x /Users/admin/.claude/commands/orchestrator_engine.py

# Optional: Create alias for convenience
echo 'alias orchestrator="/Users/admin/.claude/commands/orchestrator_cli.sh"' >> ~/.zshrc
source ~/.zshrc
```

## Command Reference

### Primary Commands

#### `orchestrator auto`
**Purpose**: Intelligent automatic orchestration
**Usage**: 
```bash
orchestrator auto                              # Basic auto-orchestration
orchestrator auto --intent "debugging session"  # With context
orchestrator auto --verbose                   # Detailed output
orchestrator auto --dry-run                   # Preview without execution
```

#### `orchestrator status`
**Purpose**: Show current orchestration status
**Output**: 
- Session duration and token count
- Task completion count
- Complexity score
- Current configuration
- Recent command history
- Personalized recommendations

#### `orchestrator analyze`
**Purpose**: Analyze current context without execution
**Use Cases**:
- Understand current session metrics
- Get recommendations for optimization
- Debug orchestration decisions

### Force Commands

#### `orchestrator digest`
**Purpose**: Force digest command execution
**Usage**:
```bash
orchestrator digest                            # Auto-determine digest action
orchestrator digest --intent "implementation complete"  # With context
```

#### `orchestrator compact`
**Purpose**: Force compact command execution
**Usage**:
```bash
orchestrator compact                           # Standard compaction
orchestrator compact --intent "clarify concepts"  # With specific intent
```

#### `orchestrator hybrid`
**Purpose**: Execute combined digest + compact workflow
**Usage**:
```bash
orchestrator hybrid                            # Balanced hybrid execution
orchestrator hybrid --intent "session transition"  # Context-aware hybrid
```

### Configuration Commands

#### `orchestrator profile <name>`
**Purpose**: Set workflow profile for different development scenarios
**Profiles**:
- `dev` - Development-focused (high digest frequency)
- `research` - Research-focused (high compact frequency)
- `debug` - Debugging-focused (low automation)
- `doc` - Documentation-focused (comprehensive tracking)

**Usage**:
```bash
orchestrator profile dev                       # Set development profile
orchestrator profile research                 # Set research profile
orchestrator profile debug                    # Set debugging profile
orchestrator profile doc                      # Set documentation profile
```

#### `orchestrator config`
**Purpose**: Show current configuration
**Output**: Complete YAML configuration with all settings

### Monitoring Commands

#### `orchestrator monitor`
**Purpose**: Start real-time monitoring mode
**Features**:
- Continuous status updates every 30 seconds
- Automatic complexity alerts
- Live metrics display
- Press Ctrl+C to stop

#### `orchestrator metrics`
**Purpose**: Show performance metrics and command history
**Output**: Recent orchestration events with timestamps

### Advanced Usage

#### Verbose Mode
```bash
orchestrator auto --verbose                   # Detailed execution info
orchestrator status --verbose                 # Extended status information
```

#### Dry Run Mode
```bash
orchestrator auto --dry-run                   # Preview actions without execution
orchestrator digest --dry-run                 # See what digest would do
```

#### Custom Configuration
```bash
orchestrator auto --config /path/to/config.yaml  # Use custom config file
```

## Workflow Scenarios

### Development Session
```bash
# Start of session
orchestrator auto --intent "starting development session"

# During implementation
orchestrator auto --intent "implementing user authentication"

# After major milestone
orchestrator digest --intent "authentication system complete"

# End of session
orchestrator auto --intent "ending development session"
```

### Research Session
```bash
# Set research profile
orchestrator profile research

# During research
orchestrator auto --intent "researching API documentation"

# When context gets verbose
orchestrator compact --intent "summarize research findings"

# End of research
orchestrator digest --intent "research phase complete"
```

### Debugging Session
```bash
# Set debugging profile
orchestrator profile debug

# During debugging
orchestrator compact --intent "focusing on bug reproduction"

# When solution found
orchestrator digest --intent "bug fix implemented"
```

### Documentation Session
```bash
# Set documentation profile
orchestrator profile doc

# During documentation
orchestrator auto --intent "writing technical documentation"

# Regular progress captures
orchestrator digest --intent "documentation milestone"
```

## Configuration Details

### Workflow Profiles

#### Development Profile
```yaml
automation_level: "high"
digest_threshold: 2          # Digest after 2 completed tasks
session_duration_trigger: 25.0  # Digest after 25 minutes
token_threshold: 0.8         # Compact at 80% token usage
continuity_priority: "high"  # High emphasis on session continuity
```

#### Research Profile
```yaml
automation_level: "medium"
digest_threshold: 4          # Digest after 4 completed tasks
session_duration_trigger: 45.0  # Digest after 45 minutes
token_threshold: 0.7         # Compact at 70% token usage
continuity_priority: "medium"  # Medium emphasis on session continuity
```

#### Debugging Profile
```yaml
automation_level: "low"
digest_threshold: 5          # Digest after 5 completed tasks
session_duration_trigger: 60.0  # Digest after 60 minutes
token_threshold: 0.6         # Compact at 60% token usage
continuity_priority: "low"   # Low emphasis on session continuity
```

#### Documentation Profile
```yaml
automation_level: "high"
digest_threshold: 1          # Digest after 1 completed task
session_duration_trigger: 20.0  # Digest after 20 minutes
token_threshold: 0.8         # Compact at 80% token usage
continuity_priority: "high"  # High emphasis on session continuity
```

### Automatic Triggers

#### Digest Triggers
- **Session Duration**: > 30 minutes (configurable)
- **Task Completion**: >= 3 completed tasks (configurable)
- **Major Implementation**: Significant code changes detected
- **End of Session**: Long session archival

#### Compact Triggers
- **Token Usage**: > 75% of limit (configurable)
- **Repetitive Patterns**: > 3 repetitive discussions
- **Message Count**: > 25 messages in conversation
- **Topic Changes**: Significant context shifts

### Decision Engine Logic

#### Priority Scoring
The engine calculates scores for digest vs compact based on:

**Digest Score Factors**:
- Session duration weight: 30%
- Task completion weight: 40%
- Code implementation weight: 20%
- User intent weight: 30%
- Complexity weight: 20%

**Compact Score Factors**:
- Token usage weight: 50%
- Repetitive patterns weight: 30%
- Message count weight: 20%
- User intent weight: 40%
- Topic changes weight: 20%

#### Command Selection
- **Digest**: Score > 0.6 and higher than compact
- **Compact**: Score > 0.6 and higher than digest
- **Hybrid**: Both scores > 0.4
- **None**: Both scores < 0.4

## Best Practices

### For Development
1. **Start with profile**: `orchestrator profile dev`
2. **Use intent context**: Always provide meaningful intent
3. **Check status regularly**: `orchestrator status` for recommendations
4. **End session properly**: Let orchestrator handle session archival

### For Research
1. **Set research profile**: `orchestrator profile research`
2. **Use compact frequently**: When information gets overwhelming
3. **Digest key findings**: Use digest to capture important discoveries
4. **Query previous research**: Use `/digest --query` for historical context

### For Debugging
1. **Set debug profile**: `orchestrator profile debug`
2. **Focus sessions**: Use compact to maintain clarity
3. **Document solutions**: Use digest when bugs are resolved
4. **Track patterns**: Let orchestrator identify debugging patterns

### For Documentation
1. **Set doc profile**: `orchestrator profile doc`
2. **Frequent digests**: Capture documentation progress regularly
3. **Comprehensive tracking**: High automation for complete records
4. **Version control**: Coordinate with git for documentation versions

## Troubleshooting

### Common Issues

#### "Command not found"
```bash
# Check if scripts are executable
ls -la /Users/admin/.claude/commands/orchestrator_cli.sh
chmod +x /Users/admin/.claude/commands/orchestrator_cli.sh

# Create alias if needed
alias orchestrator="/Users/admin/.claude/commands/orchestrator_cli.sh"
```

#### "Python module not found"
```bash
# Install required modules
pip3 install pyyaml

# Check Python version
python3 --version  # Should be 3.6+
```

#### "RAG system not available"
```bash
# Check if RAG system is running
orchestrator status

# Start RAG system if needed
cd /Users/admin/AstraTrade-Project/claude-rag
python main.py
```

#### "Configuration not found"
```bash
# Check configuration file
ls -la /Users/admin/.claude/commands/orchestrator_config.yaml

# Reset to defaults
orchestrator config > /Users/admin/.claude/commands/orchestrator_config.yaml
```

### Debug Mode
```bash
# Enable verbose output
orchestrator auto --verbose

# Check what would be executed
orchestrator auto --dry-run

# Analyze current context
orchestrator analyze
```

### Performance Issues
```bash
# Check metrics
orchestrator metrics

# Monitor in real-time
orchestrator monitor

# Check session logs
tail -f /Users/admin/.claude/orchestrator_session.log
```

## Integration with Existing Workflows

### Git Integration
The orchestrator automatically detects git changes and can trigger digests on significant commits. Configure in `orchestrator_config.yaml`:

```yaml
integration_settings:
  git_integration: true
  auto_digest_on_commit: true
  commit_threshold: 5  # files changed
```

### Claude Code Integration
Seamlessly works with existing Claude Code sessions:

```yaml
integration_settings:
  claude_code_integration: true
  project_awareness: true
  workspace_detection: true
```

### IDE Integration
Future integration points for popular IDEs:

```yaml
integration_settings:
  vscode_integration: false
  jetbrains_integration: false
  sublime_integration: false
```

## Advanced Configuration

### Custom Triggers
Add custom triggers in `orchestrator_config.yaml`:

```yaml
custom_triggers:
  - name: "critical_bug_fix"
    condition: "intent contains 'critical' and code_changes > 10"
    action: "digest"
    priority: "high"
  
  - name: "architecture_decision"
    condition: "intent contains 'architecture' or intent contains 'design'"
    action: "digest"
    priority: "high"
```

### Webhook Integration
Configure webhooks for external systems:

```yaml
webhooks:
  - name: "slack_notifications"
    url: "https://hooks.slack.com/services/..."
    events: ["digest_created", "session_archived"]
  
  - name: "project_management"
    url: "https://api.project-tool.com/webhook"
    events: ["task_completed", "milestone_reached"]
```

This orchestration system provides intelligent, automated balance between `/digest` and `/compact` commands while maintaining full user control and customization capabilities.