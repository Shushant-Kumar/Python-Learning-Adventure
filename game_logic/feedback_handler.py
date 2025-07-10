"""
Frontend Feedback Handler
Utilities for displaying feedback messages and managing UI state transitions
"""

from typing import Dict, Any, Optional
import json


class FeedbackRenderer:
    """Handles rendering of feedback messages and UI transitions."""
    
    def __init__(self):
        self.feedback_templates = self._load_feedback_templates()
    
    def render_submission_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Render feedback for answer submission.
        
        Args:
            feedback_data: Feedback data from level validation
            
        Returns:
            Rendered feedback with UI instructions
        """
        feedback = feedback_data.get('feedback', {})
        feedback_type = feedback.get('type', 'info')
        
        # Base UI instructions
        ui_instructions: Dict[str, Any] = {
            'hide_submit_button': True,
            'show_feedback_panel': True,
            'disable_form': True,
            'scroll_to_feedback': True
        }
        
        # Type-specific UI modifications
        if feedback_type == 'success':
            ui_instructions.update({
                'highlight_color': '#4CAF50',
                'show_celebration_animation': True,
                'play_success_sound': True
            })
            
            if feedback.get('show_next_button'):
                ui_instructions.update({
                    'show_next_button': True,
                    'next_button_text': feedback.get('next_button_text', 'Continue'),
                    'next_button_action': 'proceed_to_next_level'
                })
                
            if feedback.get('show_retry'):
                ui_instructions.update({
                    'show_retry_button': True,
                    'retry_button_text': feedback.get('retry_button_text', 'Retry for Better Score'),
                    'retry_button_style': 'secondary'
                })
        
        elif feedback_type == 'error':
            ui_instructions.update({
                'highlight_color': '#F44336',
                'show_error_animation': True,
                'play_error_sound': True,
                'show_retry_button': True,
                'retry_button_text': feedback.get('retry_button_text', 'Try Again'),
                'retry_button_action': 'retry_level'
            })
            
        elif feedback_type == 'warning':
            ui_instructions.update({
                'highlight_color': '#FF9800',
                'show_warning_animation': True,
                'show_retry_button': True,
                'retry_button_text': feedback.get('retry_button_text', 'Try Again'),
                'retry_button_action': 'retry_level'
            })
        
        # Add study suggestions if available
        if feedback.get('study_suggestion'):
            ui_instructions.update({
                'show_study_panel': True,
                'study_text': feedback['study_suggestion']
            })
        
        return {
            'feedback': feedback,
            'ui_instructions': ui_instructions,
            'detailed_results': feedback_data.get('detailed_results', []),
            'progression_data': feedback_data.get('progression', {})
        }
    
    def render_question_feedback(self, question_results: list) -> list:
        """
        Render individual question feedback.
        
        Args:
            question_results: List of question result dictionaries
            
        Returns:
            List of rendered question feedback
        """
        rendered_results = []
        
        for result in question_results:
            rendered_result = {
                'question_number': result.get('question_number'),
                'is_correct': result.get('is_correct'),
                'feedback_type': result.get('feedback_type'),
                'feedback_message': result.get('feedback_message'),
                'explanation': result.get('explanation'),
                'ui_style': self._get_question_ui_style(result)
            }
            
            # Add answer details
            if result.get('options'):
                rendered_result['answer_details'] = {
                    'submitted_answer_text': self._get_option_text(
                        result.get('options'), 
                        result.get('submitted_answer')
                    ),
                    'correct_answer_text': self._get_option_text(
                        result.get('options'), 
                        result.get('correct_answer')
                    )
                }
            
            rendered_results.append(rendered_result)
        
        return rendered_results
    
    def _get_question_ui_style(self, result: Dict[str, Any]) -> Dict[str, str]:
        """Get UI styling for individual question feedback."""
        if result.get('is_correct'):
            return {
                'border_color': '#4CAF50',
                'background_color': '#E8F5E8',
                'icon': '✅',
                'text_color': '#2E7D32'
            }
        else:
            return {
                'border_color': '#F44336', 
                'background_color': '#FFEBEE',
                'icon': '❌',
                'text_color': '#C62828'
            }
    
    def _get_option_text(self, options: list, option_index: int) -> str:
        """Get text for an option by index."""
        if option_index is not None and 0 <= option_index < len(options):
            return options[option_index]
        return "Unknown"
    
    def generate_next_level_data(self, progression_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate data for next level transition.
        
        Args:
            progression_data: Progression information from level completion
            
        Returns:
            Data for next level transition
        """
        return {
            'can_proceed': progression_data.get('can_proceed', False),
            'next_level_id': progression_data.get('next_level_id'),
            'redirect_url': '/dashboard' if progression_data.get('redirect_to_dashboard') else None,
            'unlock_message': self._generate_unlock_message(progression_data),
            'rewards_earned': progression_data.get('rewards', {}),
            'stars_earned': progression_data.get('stars_earned', 0)
        }
    
    def _generate_unlock_message(self, progression_data: Dict[str, Any]) -> Optional[str]:
        """Generate unlock message for level progression."""
        if progression_data.get('next_level_unlocked'):
            next_level_id = progression_data.get('next_level_id')
            return f"🎉 Level {next_level_id} has been unlocked! You can now continue your learning journey."
        return None
    
    def _load_feedback_templates(self) -> Dict[str, Any]:
        """Load feedback message templates."""
        return {
            'perfect_score': "🌟 Perfect! You've mastered this topic completely!",
            'excellent': "⭐ Excellent work! You have a strong understanding!",
            'good': "✅ Good job! You've passed and can move forward!",
            'almost': "📚 Almost there! Review and try again!",
            'needs_work': "📖 Keep learning! Practice makes perfect!",
            'encouragement': [
                "Every expert was once a beginner!",
                "Learning is a journey, not a destination!",
                "You're making great progress!",
                "Don't give up - you've got this!",
                "Each attempt makes you stronger!"
            ]
        }

class DashboardRedirect:
    """Handles dashboard redirection and state updates."""
    
    @staticmethod
    def generate_redirect_data(player, level_completed: int) -> Dict[str, Any]:
        """
        Generate data for dashboard redirect after level completion.
        
        Args:
            player: Player object
            level_completed: ID of completed level
            
        Returns:
            Redirect data with updated dashboard state
        """
        return {
            'redirect_url': '/dashboard',
            'highlight_level': level_completed,
            'show_completion_message': True,
            'update_progress_bar': True,
            'refresh_level_map': True,
            'scroll_to_next_level': True,
            'celebration_data': {
                'completed_level': level_completed,
                'show_fireworks': True,
                'duration': 3000  # milliseconds
            }
        }
    
    @staticmethod
    def generate_level_unlock_notification(unlocked_level_id: int) -> Dict[str, Any]:
        """Generate notification for newly unlocked level."""
        return {
            'type': 'level_unlock',
            'title': 'New Level Unlocked!',
            'message': f'Level {unlocked_level_id} is now available to play!',
            'level_id': unlocked_level_id,
            'show_duration': 5000,  # milliseconds
            'action_button': {
                'text': 'Play Now',
                'action': f'start_level_{unlocked_level_id}'
            }
        }
