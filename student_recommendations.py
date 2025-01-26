import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

class StudentAnalyzer:
    def __init__(self):
        self.historical_data = []
        self.current_quiz = None
        self.quiz_submission = None
        
    def load_data(self, historical_data: List[Dict], current_quiz: Dict, quiz_submission: Dict):
        """Load and initialize the data"""
        self.historical_data = historical_data
        self.current_quiz = current_quiz
        self.quiz_submission = quiz_submission
        
    def analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends across quizzes"""
        trends = {
            'accuracy_trend': [],
            'topics': defaultdict(list),
            'average_score': 0,
            'improvement_rate': 0
        }
        
        for quiz in self.historical_data:
            accuracy = float(quiz['accuracy'].strip(' %'))
            topic = quiz['quiz']['topic']
            score = quiz['score']
            
            trends['accuracy_trend'].append(accuracy)
            trends['topics'][topic].append(score)
        
        # Calculate averages and trends
        trends['average_score'] = sum(quiz['score'] for quiz in self.historical_data) / len(self.historical_data)
        
        # Calculate improvement rate
        if len(trends['accuracy_trend']) >= 2:
            initial = trends['accuracy_trend'][0]
            final = trends['accuracy_trend'][-1]
            trends['improvement_rate'] = ((final - initial) / initial) * 100
            
        return trends

    def identify_weak_areas(self) -> List[Dict[str, Any]]:
        """Identify topics and concepts where student needs improvement"""
        topic_performance = defaultdict(lambda: {'total_questions': 0, 'correct_answers': 0})
        
        for quiz in self.historical_data:
            topic = quiz['quiz']['topic']
            correct = quiz['correct_answers']
            total = quiz['total_questions']
            
            topic_performance[topic]['total_questions'] += total
            topic_performance[topic]['correct_answers'] += correct
        
        weak_areas = []
        for topic, stats in topic_performance.items():
            accuracy = (stats['correct_answers'] / stats['total_questions']) * 100
            if accuracy < 70:  # Threshold for weak areas
                weak_areas.append({
                    'topic': topic,
                    'accuracy': accuracy,
                    'total_attempts': stats['total_questions']
                })
                
        return sorted(weak_areas, key=lambda x: x['accuracy'])

    def generate_student_persona(self) -> Dict[str, Any]:
        """Generate a student persona based on performance patterns"""
        trends = self.analyze_performance_trends()
        
        persona = {
            'learning_style': self._determine_learning_style(),
            'consistency_score': self._calculate_consistency(),
            'strength_areas': self._identify_strengths(),
            'improvement_needed': self.identify_weak_areas(),
            'performance_level': self._determine_performance_level(trends['average_score'])
        }
        
        return persona

    def _determine_learning_style(self) -> str:
        """Determine student's learning style based on patterns"""
        speed_scores = [float(quiz.get('speed', 0)) for quiz in self.historical_data]
        accuracy_scores = [float(quiz['accuracy'].strip(' %')) for quiz in self.historical_data]
        
        avg_speed = sum(speed_scores) / len(speed_scores)
        avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
        
        if avg_speed > 90 and avg_accuracy > 80:
            return "Fast and Accurate"
        elif avg_speed > 90 and avg_accuracy <= 80:
            return "Quick but Needs More Practice"
        elif avg_speed <= 90 and avg_accuracy > 80:
            return "Methodical and Accurate"
        else:
            return "Building Foundations"

    def generate_recommendations(self) -> Dict[str, Any]:
        """Generate personalized recommendations based on analysis"""
        weak_areas = self.identify_weak_areas()
        persona = self.generate_student_persona()
        trends = self.analyze_performance_trends()
        
        recommendations = {
            'priority_topics': [area['topic'] for area in weak_areas[:3]],
            'suggested_practice_plan': self._create_practice_plan(weak_areas, persona),
            'improvement_strategies': self._suggest_strategies(persona),
            'next_steps': self._suggest_next_steps(trends)
        }
        
        return recommendations

    def _create_practice_plan(self, weak_areas: List[Dict], persona: Dict) -> List[Dict]:
        """Create a personalized practice plan"""
        plan = []
        for area in weak_areas:
            plan.append({
                'topic': area['topic'],
                'recommended_questions': 20 if area['accuracy'] < 50 else 10,
                'focus_areas': ['Basic Concepts', 'Practice Problems'] if area['accuracy'] < 50 else ['Advanced Problems'],
                'estimated_time': '2 hours' if area['accuracy'] < 50 else '1 hour'
            })
        return plan

    def _suggest_strategies(self, persona: Dict) -> List[str]:
        """Suggest learning strategies based on persona"""
        strategies = []
        if persona['learning_style'] == "Fast and Accurate":
            strategies.extend([
                "Focus on advanced problem-solving techniques",
                "Take on challenging topics",
                "Help peers and explain concepts to others"
            ])
        elif persona['learning_style'] == "Building Foundations":
            strategies.extend([
                "Review basic concepts thoroughly",
                "Practice with easier questions first",
                "Increase practice frequency"
            ])
        return strategies

    def _calculate_consistency(self) -> float:
        """Calculate student's consistency in performance"""
        scores = [quiz['score'] for quiz in self.historical_data]
        if not scores:
            return 0.0
        
        # Calculate standard deviation of scores
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Convert to consistency score (100 - normalized std dev)
        max_std_dev = 100  # maximum possible standard deviation
        consistency = 100 * (1 - (std_dev / max_std_dev))
        return round(consistency, 2)

    def _identify_strengths(self) -> List[str]:
        """Identify areas where student excels"""
        topic_performance = defaultdict(lambda: {'total_questions': 0, 'correct_answers': 0})
        
        for quiz in self.historical_data:
            topic = quiz['quiz']['topic']
            correct = quiz['correct_answers']
            total = quiz['total_questions']
            
            topic_performance[topic]['total_questions'] += total
            topic_performance[topic]['correct_answers'] += correct
        
        strengths = []
        for topic, stats in topic_performance.items():
            accuracy = (stats['correct_answers'] / stats['total_questions']) * 100
            if accuracy >= 80:  # Threshold for strength areas
                strengths.append(topic)
                
        return strengths

    def _determine_performance_level(self, average_score: float) -> str:
        """Determine student's performance level based on average score"""
        if average_score >= 80:
            return "High Achiever"
        elif average_score >= 60:
            return "Average Performer"
        else:
            return "Needs Improvement"

    def _suggest_next_steps(self, trends: Dict[str, Any]) -> List[str]:
        """Suggest next steps based on trends"""
        next_steps = []
        
        # Based on improvement rate
        if trends['improvement_rate'] < 0:
            next_steps.append("Focus on reviewing past mistakes and understanding core concepts")
        elif trends['improvement_rate'] < 10:
            next_steps.append("Maintain current study routine while gradually increasing difficulty")
        else:
            next_steps.append("Challenge yourself with more advanced topics")
            
        # Based on average score
        if trends['average_score'] < 60:
            next_steps.append("Schedule regular practice sessions focusing on fundamentals")
        elif trends['average_score'] < 80:
            next_steps.append("Work on improving accuracy in moderate difficulty questions")
            
        return next_steps
