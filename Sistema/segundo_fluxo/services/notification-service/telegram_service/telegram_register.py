import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
from telegram_service.telegram_notifier import register_service, list_services
from dotenv import load_dotenv

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    nome = update.effective_user.first_name
    
    if(update and update.message):
        await update.message.reply_text(
            f"✅ Olá *{nome}*!\n\n"
            f"Você foi cadastrado com sucesso!\n"
            f"Agora você receberá notificações quando algum serviço cair.\n\n"
            f"Seu Chat ID: `{chat_id}`\n\n"
            f"Comandos:\n"
            f"/register - Cadastrar Serviços\n"
            f"/status - Status de todos seus serviços\n",
            parse_mode='Markdown'
    )


def start_bot():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register",register_service ))
    app.add_handler(CommandHandler("status",list_services ))   
     
    
    def run_bot():
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            close_loop=False,
            stop_signals=None  
        )
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("🤖 Bot Telegram rodando...")
    print("Os usuários podem enviar /start para se cadastrar")

