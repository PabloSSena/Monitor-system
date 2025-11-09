from telegram import Bot,Update
from telegram.ext import  ContextTypes
from datetime import datetime
from config.database import hosts_collection
import os

from schemas.hosts_schema import list_hosts

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def send_notification(url):
        try:
            print("Enviando notificação para o Telegram...")
            bot = Bot(token=TOKEN)
            mensagem = (
                f"🔴 *ALERTA DE QUEDA*\n\n"
                f"URL: `{url}`\n"
                f"Status: Indisponível\n"
                f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )
            chatIds = list(hosts_collection.find({"url": url}, {"chat_id":1, "_id":0,  }))
            for chatId in chatIds:
                await bot.send_message(chat_id=chatId['chat_id'], text=mensagem, parse_mode='Markdown')
            return True
        except Exception as e:
            print(f"Erro ao enviar para o Telegram: {e}")
            return False


async def register_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id =  update.effective_chat.id
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "❌ Uso incorreto do comando.\n"
            "Use: /register <URL> \n"
            "Exemplo: /register http://example.com"
        )
        return
    try: 
        url = context.args[0]
        hosts_collection.insert_one({"chat_id": str(chat_id), "url": url})

    except Exception as e: 
        print(f'erro ao registrar serviço: {e}')    
    if(update and update.message):
        await update.message.reply_text(
            f"✅ Serviço registrado com sucesso!\n"
            f"URL: {url}\n"
            f"Você receberá notificações para este serviço."
        )
        
        
async def list_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id =  update.effective_chat.id
    hosts = []
    try: 
        hosts = list_hosts(hosts_collection.find({"chat_id": str(chat_id)}))
        
        if not hosts:
            await update.message.reply_text("Você não possui serviços registrados.")
            return
        
        services_list = "\n".join([f"🌐 {i+1}. {host['url']}" for i, host in enumerate(hosts)])

        print(hosts)
        if(update and update.message):
            await update.message.reply_text(
                f"✅ Serviços : \n"
                
                f"URL: {services_list}\n"
                
                f"Você receberá notificações para esses serviços."
            )
    except Exception as e: 
        print(f'erro ao listar serviços: {e}')    
        

