from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from game import KitchenGame
from config import BOT_TOKEN
import random

user_games = {}

async def start(update, context):
    user_id = update.effective_user.id
    user_games[user_id] = KitchenGame()
    
    welcome_text = """
🎭 *Добро пожаловать в игру "Угадай цитату из Кухни!"* 🍳

Я буду показывать цитаты из сериала "Кухня", а ты угадывай, кто из персонажей их сказал.

📋 *Правила:*
• Всего 15 вопросов
• За правильный ответ получаешь очки
• Чем быстрее отвечаешь - тем больше очков
• В конце узнаешь свой уровень знания сериала

🚀 *Команды:*
/start - начать новую игру
/play - начать играть

*Готов проверить свои знания?* Жми /play! 🔥
    """
    
    await update.message.reply_text(welcome_text)

async def play(update, context):
    user_id = update.effective_user.id
    
    game = user_games[user_id]
    
    if game.is_game_over():
        await show_results(update, game)
        return
    
    quote = game.get_random_quote()
    
    answers = [quote['correct_character']] + quote['wrong_characters']
    random.shuffle(answers)
    
    all_buttons = []
    for variant in answers:
        button = InlineKeyboardButton(variant, callback_data=variant)
        all_buttons.append([button])

    keyboard = InlineKeyboardMarkup(all_buttons)
    
    question_text = f"""
🎯 *Вопрос {game.get_progress()}*

*"{quote['text']}"*

*Кто это говорит?*
    """
    
    await update.message.reply_text(question_text, reply_markup = keyboard)

async def handle_answer(update, context):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_answer = query.data
    
    if user_id not in user_games:
        await query.edit_message_text("❌ Игра не найдена. Нажми /start")
        return
    
    game = user_games[user_id]
    result = game.check_answer(user_answer)
    
    character_info = game.get_character_info(result['correct_answer'])
    
    if result['correct']:
        response = f"""
✅ *Правильно!* 

Это *{result['correct_answer']}* - {character_info}

🎯 *+{result['points']} очков*
📊 *Прогресс:* {game.get_progress()}
💯 *Общий счет:* {game.total_score}

*Следующий вопрос?* /play
        """
    else:
        response = f"""
❌ *Неверно!*

Правильный ответ: *{result['correct_answer']}* - {character_info}

📊 *Прогресс:* {game.get_progress()}
💯 *Общий счет:* {game.total_score}

*Продолжим?* /play
        """
    
    await query.edit_message_text(response)

async def show_results(update, game):
    results = game.get_final_results()
    
    result_text = f"""
🎉 *ИГРА ЗАВЕРШЕНА!*

📊 *Твои результаты:*
• Правильных ответов: {results['correct_answers']}/15
• Процент правильных: {results['percent']:.1f}%
• Общий счет: {results['total_score']} очков

🏆 *Твой уровень:* {results['level']}
💬 {results['description']}

*Хочешь сыграть еще?* /start
    """
    
    await update.message.reply_text(result_text)
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CallbackQueryHandler(handle_answer))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()