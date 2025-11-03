import random
import time
from database import QUOTES_DATABASE

class KitchenGame:
    def __init__(self):
        self.used_quotes = []
        self.current_question = None
        self.start_time = None
        self.total_score = 0
        self.correct_answers = 0
        self.question_count = 0
        
    def get_random_quote(self):
        if self.question_count >= 15:
            return None

        available_quotes = []
        for quote in QUOTES_DATABASE:
            if quote['id'] not in self.used_quotes:
                available_quotes.append(quote)
        
        if len(available_quotes) == 0:
            self.used_quotes = []
            available_quotes = QUOTES_DATABASE
            
        quote = random.choice(available_quotes)
        
        self.used_quotes.append(quote['id'])
        self.current_question = quote
        self.start_time = time.time()
        self.question_count += 1
        
        return quote
    
    def check_answer(self, user_answer):
        time_taken = time.time() - self.start_time
  
        correct_answer = self.current_question['correct_character']
        
        is_correct = user_answer == correct_answer

        base_points = 50
        time_bonus = 20 - int(time_taken)
        if time_bonus < 0:
            time_bonus = 0
            
        points = base_points + time_bonus
        
        if is_correct:
            self.total_score += points
            self.correct_answers += 1
        
        result = {
            'correct': is_correct,
            'correct_answer': correct_answer,
            'points': points if is_correct else 0,
            'time_bonus': time_bonus,
            'question_number': self.question_count
        }
        
        return result
    
    def get_final_results(self):
        percent = (self.correct_answers / 15) * 100
    
        if percent >= 90:
            level = "👑 ЗНАТОК КУХНИ"
            description = "Ты знаешь сериал наизусть! Браво!"
        elif percent >= 70:
            level = "🏆 ШЕФ-ПОВАР"
            description = "Отлично! Ты настоящий фанат 'Кухни'!"
        elif percent >= 50:
            level = "🔪 СУ-ШЕФ" 
            description = "Хорошо! Ты внимательно смотрел(а) сериал!"
        elif percent >= 30:
            level = "🍳 ПОВАРЁНОК"
            description = "Неплохо, но можно и лучше!"
        else:
            level = "🍖 ОГУЗОК"
            description = "Пора пересмотреть сериал!"
        
        results = {
            'total_score': self.total_score,
            'correct_answers': self.correct_answers,
            'total_questions': 15,
            'percent': percent,
            'level': level,
            'description': description
        }
        
        return results
    
    def is_game_over(self):
        return self.question_count >= 15
    
    def get_progress(self):
        return f"{self.question_count}/15"
    
    def get_character_info(self, character_name):
        from database import CHARACTERS
        return CHARACTERS.get(character_name, character_name)