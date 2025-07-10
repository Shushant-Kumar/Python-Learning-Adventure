"""
Event Dispatcher Module
Handles game events, notifications, and system-wide communication
"""

from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from enum import Enum
import threading
import queue
import time


class EventType(Enum):
    """Enumeration of all game event types."""
    # Level Events
    LEVEL_STARTED = "level_started"
    LEVEL_COMPLETED = "level_completed"
    LEVEL_FAILED = "level_failed"
    LEVEL_UNLOCKED = "level_unlocked"
    
    # Achievement Events  
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    ACHIEVEMENT_PROGRESS = "achievement_progress"
    
    # Player Events
    PLAYER_REGISTERED = "player_registered"
    PLAYER_LOGIN = "player_login"
    PLAYER_LOGOUT = "player_logout"
    PLAYER_STATS_UPDATED = "player_stats_updated"
    
    # Game State Events
    GAME_STARTED = "game_started"
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"
    GAME_ERROR = "game_error"
    
    # Learning Events
    QUIZ_ANSWERED = "quiz_answered"
    HINT_REQUESTED = "hint_requested"
    LEARNING_STREAK_UPDATED = "learning_streak_updated"
    
    # Animation Events
    ANIMATION_STARTED = "animation_started"
    ANIMATION_COMPLETED = "animation_completed"
    
    # System Events
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"
    SYSTEM_INFO = "system_info"


class Event:
    """Represents a game event with metadata."""
    
    def __init__(self, event_type: EventType, data: Optional[Dict[str, Any]] = None, 
                 source: str = "system", priority: int = 0):
        self.id = self._generate_event_id()
        self.type = event_type
        self.data = data or {}
        self.source = source
        self.priority = priority  # Higher numbers = higher priority
        self.timestamp = datetime.now().isoformat()
        self.handled = False
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def mark_handled(self):
        """Mark event as handled."""
        self.handled = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            'id': self.id,
            'type': self.type.value,
            'data': self.data,
            'source': self.source,
            'priority': self.priority,
            'timestamp': self.timestamp,
            'handled': self.handled
        }


class EventDispatcher:
    """Central event dispatcher for the game system."""
    
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._event_history: List[Event] = []
        self._event_queue = queue.PriorityQueue()
        self._running = False
        self._processor_thread = None
        self._max_history = 1000
        self._stats = {
            'events_dispatched': 0,
            'events_processed': 0,
            'listeners_registered': 0,
            'errors': 0
        }
    
    def start(self):
        """Start the event processing system."""
        if not self._running:
            self._running = True
            self._processor_thread = threading.Thread(target=self._process_events, daemon=True)
            self._processor_thread.start()
    
    def stop(self):
        """Stop the event processing system."""
        self._running = False
        if self._processor_thread:
            self._processor_thread.join(timeout=1.0)
    
    def subscribe(self, event_type: EventType, listener: Callable):
        """Subscribe a listener to an event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        
        self._listeners[event_type].append(listener)
        self._stats['listeners_registered'] += 1
    
    def unsubscribe(self, event_type: EventType, listener: Callable):
        """Unsubscribe a listener from an event type."""
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(listener)
            except ValueError:
                pass
    
    def dispatch(self, event_type: EventType, data: Optional[Dict[str, Any]] = None, 
                source: str = "system", priority: int = 0, immediate: bool = False):
        """Dispatch an event."""
        event = Event(event_type, data, source, priority)
        
        if immediate:
            self._handle_event(event)
        else:
            # Use negative priority for correct priority queue ordering (higher priority first)
            self._event_queue.put((-priority, time.time(), event))
        
        self._stats['events_dispatched'] += 1
        return event.id
    
    def _process_events(self):
        """Process events from the queue."""
        while self._running:
            try:
                # Wait for events with timeout
                _, _, event = self._event_queue.get(timeout=0.1)
                self._handle_event(event)
                self._event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self._stats['errors'] += 1
                print(f"Error processing event: {e}")
    
    def _handle_event(self, event: Event):
        """Handle a single event by notifying all listeners."""
        try:
            # Add to history
            self._event_history.append(event)
            self._trim_history()
            
            # Notify listeners
            listeners = self._listeners.get(event.type, [])
            for listener in listeners:
                try:
                    listener(event)
                except Exception as e:
                    print(f"Error in event listener for {event.type}: {e}")
                    self._stats['errors'] += 1
            
            event.mark_handled()
            self._stats['events_processed'] += 1
            
        except Exception as e:
            print(f"Error handling event {event.id}: {e}")
            self._stats['errors'] += 1
    
    def _trim_history(self):
        """Trim event history to maximum size."""
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]
    
    def get_event_history(self, event_type: Optional[EventType] = None, 
                         limit: int = 50) -> List[Event]:
        """Get recent event history."""
        if event_type:
            filtered_events = [e for e in self._event_history if e.type == event_type]
            return filtered_events[-limit:]
        else:
            return self._event_history[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get dispatcher statistics."""
        return {
            **self._stats,
            'queue_size': self._event_queue.qsize(),
            'active_listeners': sum(len(listeners) for listeners in self._listeners.values()),
            'event_types_with_listeners': len(self._listeners),
            'history_size': len(self._event_history)
        }
    
    def clear_history(self):
        """Clear event history."""
        self._event_history.clear()


class GameEventManager:
    """High-level game event manager that provides convenient methods."""
    
    def __init__(self):
        self.dispatcher = EventDispatcher()
        self.dispatcher.start()
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Setup default event handlers for logging and debugging."""
        # Log important events
        important_events = [
            EventType.LEVEL_COMPLETED,
            EventType.ACHIEVEMENT_UNLOCKED,
            EventType.PLAYER_LOGIN,
            EventType.SYSTEM_ERROR
        ]
        
        for event_type in important_events:
            self.dispatcher.subscribe(event_type, self._log_important_event)
        
        # Handle system errors
        self.dispatcher.subscribe(EventType.SYSTEM_ERROR, self._handle_system_error)
    
    def _log_important_event(self, event: Event):
        """Log important events."""
        print(f"[{event.timestamp}] {event.type.value}: {event.source}")
    
    def _handle_system_error(self, event: Event):
        """Handle system errors."""
        error_data = event.data
        print(f"SYSTEM ERROR: {error_data.get('message', 'Unknown error')}")
        if error_data.get('critical', False):
            print("CRITICAL ERROR - System may be unstable")
    
    # Level Events
    def level_started(self, level_id: int, player_id: str, topic: str):
        """Dispatch level started event."""
        return self.dispatcher.dispatch(
            EventType.LEVEL_STARTED,
            {
                'level_id': level_id,
                'player_id': player_id,
                'topic': topic,
                'start_time': datetime.now().isoformat()
            },
            source=f"level_{level_id}"
        )
    
    def level_completed(self, level_id: int, player_id: str, score: float, 
                       passed: bool, time_taken: int):
        """Dispatch level completed event."""
        return self.dispatcher.dispatch(
            EventType.LEVEL_COMPLETED,
            {
                'level_id': level_id,
                'player_id': player_id,
                'score': score,
                'passed': passed,
                'time_taken': time_taken,
                'completion_time': datetime.now().isoformat()
            },
            source=f"level_{level_id}",
            priority=5  # High priority for level completion
        )
    
    def level_unlocked(self, level_id: int, player_id: str, unlocked_by: int):
        """Dispatch level unlocked event."""
        return self.dispatcher.dispatch(
            EventType.LEVEL_UNLOCKED,
            {
                'level_id': level_id,
                'player_id': player_id,
                'unlocked_by': unlocked_by
            },
            source="progression_system"
        )
    
    # Achievement Events
    def achievement_unlocked(self, achievement_id: str, player_id: str, 
                           achievement_data: Dict[str, Any]):
        """Dispatch achievement unlocked event."""
        return self.dispatcher.dispatch(
            EventType.ACHIEVEMENT_UNLOCKED,
            {
                'achievement_id': achievement_id,
                'player_id': player_id,
                'achievement_data': achievement_data
            },
            source="achievement_system",
            priority=7  # Very high priority for achievements
        )
    
    def achievement_progress(self, achievement_id: str, player_id: str, 
                           progress: float, target: float):
        """Dispatch achievement progress event."""
        return self.dispatcher.dispatch(
            EventType.ACHIEVEMENT_PROGRESS,
            {
                'achievement_id': achievement_id,
                'player_id': player_id,
                'progress': progress,
                'target': target,
                'percentage': (progress / target) * 100 if target > 0 else 0
            },
            source="achievement_system"
        )
    
    # Player Events
    def player_registered(self, player_id: str, username: str):
        """Dispatch player registered event."""
        return self.dispatcher.dispatch(
            EventType.PLAYER_REGISTERED,
            {
                'player_id': player_id,
                'username': username,
                'registration_time': datetime.now().isoformat()
            },
            source="auth_system"
        )
    
    def player_login(self, player_id: str, username: str):
        """Dispatch player login event."""
        return self.dispatcher.dispatch(
            EventType.PLAYER_LOGIN,
            {
                'player_id': player_id,
                'username': username,
                'login_time': datetime.now().isoformat()
            },
            source="auth_system"
        )
    
    def player_stats_updated(self, player_id: str, stats: Dict[str, Any]):
        """Dispatch player stats updated event."""
        return self.dispatcher.dispatch(
            EventType.PLAYER_STATS_UPDATED,
            {
                'player_id': player_id,
                'stats': stats,
                'update_time': datetime.now().isoformat()
            },
            source="stats_system"
        )
    
    # Learning Events
    def quiz_answered(self, level_id: int, player_id: str, question_id: str, 
                     answer: Any, correct: bool, time_taken: float):
        """Dispatch quiz answered event."""
        return self.dispatcher.dispatch(
            EventType.QUIZ_ANSWERED,
            {
                'level_id': level_id,
                'player_id': player_id,
                'question_id': question_id,
                'answer': answer,
                'correct': correct,
                'time_taken': time_taken
            },
            source=f"level_{level_id}"
        )
    
    def hint_requested(self, level_id: int, player_id: str, hint_type: str):
        """Dispatch hint requested event."""
        return self.dispatcher.dispatch(
            EventType.HINT_REQUESTED,
            {
                'level_id': level_id,
                'player_id': player_id,
                'hint_type': hint_type,
                'request_time': datetime.now().isoformat()
            },
            source=f"level_{level_id}"
        )
    
    def learning_streak_updated(self, player_id: str, new_streak: int, 
                              previous_streak: int):
        """Dispatch learning streak updated event."""
        return self.dispatcher.dispatch(
            EventType.LEARNING_STREAK_UPDATED,
            {
                'player_id': player_id,
                'new_streak': new_streak,
                'previous_streak': previous_streak,
                'streak_broken': new_streak < previous_streak
            },
            source="streak_system"
        )
    
    # Animation Events
    def animation_started(self, animation_type: str, context: Dict[str, Any]):
        """Dispatch animation started event."""
        return self.dispatcher.dispatch(
            EventType.ANIMATION_STARTED,
            {
                'animation_type': animation_type,
                'context': context,
                'start_time': datetime.now().isoformat()
            },
            source="animation_system"
        )
    
    def animation_completed(self, animation_type: str, duration: float):
        """Dispatch animation completed event."""
        return self.dispatcher.dispatch(
            EventType.ANIMATION_COMPLETED,
            {
                'animation_type': animation_type,
                'duration': duration,
                'completion_time': datetime.now().isoformat()
            },
            source="animation_system"
        )
    
    # System Events
    def system_error(self, error_message: str, error_details: Optional[Dict[str, Any]] = None, 
                    critical: bool = False):
        """Dispatch system error event."""
        return self.dispatcher.dispatch(
            EventType.SYSTEM_ERROR,
            {
                'message': error_message,
                'details': error_details or {},
                'critical': critical,
                'error_time': datetime.now().isoformat()
            },
            source="system",
            priority=10,  # Highest priority for errors
            immediate=critical  # Handle critical errors immediately
        )
    
    def system_warning(self, warning_message: str, warning_details: Optional[Dict[str, Any]] = None):
        """Dispatch system warning event."""
        return self.dispatcher.dispatch(
            EventType.SYSTEM_WARNING,
            {
                'message': warning_message,
                'details': warning_details or {},
                'warning_time': datetime.now().isoformat()
            },
            source="system"
        )
    
    def system_info(self, info_message: str, info_details: Optional[Dict[str, Any]] = None):
        """Dispatch system info event."""
        return self.dispatcher.dispatch(
            EventType.SYSTEM_INFO,
            {
                'message': info_message,
                'details': info_details or {},
                'info_time': datetime.now().isoformat()
            },
            source="system"
        )
    
    # Utility Methods
    def subscribe_to_event(self, event_type: EventType, handler: Callable):
        """Subscribe to an event type."""
        self.dispatcher.subscribe(event_type, handler)
    
    def get_recent_events(self, event_type: Optional[EventType] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent events as dictionaries."""
        events = self.dispatcher.get_event_history(event_type, limit)
        return [event.to_dict() for event in events]
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics including dispatcher stats."""
        return self.dispatcher.get_stats()
    
    def shutdown(self):
        """Shutdown the event system."""
        self.dispatcher.stop()


# Global event manager instance
event_manager = GameEventManager()
