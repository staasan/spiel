from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackQueryHandler
from templates import templates
import requests
import os

class NoTokenError(Exception):
    pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to EndSpielBot! Learn endgames, most demanding stage of chess game!')

#Generated endgame: https://lichess.org/editor/{to_fen(generate(templates.king_pawn))
async def train(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
            [InlineKeyboardButton(x, callback_data=f"train:{x}")] for x in templates
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Select endgame to train',reply_markup=reply_markup)
async def send_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    template = query.data.split(":")[1].lower().replace(" ", "_")

    fen = requests.get(
        f"{api}get_endgame?template={template}",
        proxies={"http": "", "https": ""}).json()["fen"]
    if "Draw" in template:
        keyboard = [
        [
            InlineKeyboardButton("✅Stalemate", callback_data=f"result:won:{template}"),
            InlineKeyboardButton("❌Checkmate", callback_data=f"result:lost:{template}")
        ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("✅Checkmate", callback_data=f"result:won:{template}"),
                InlineKeyboardButton("❌Stalemate", callback_data=f"result:lost:{template}")
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.answer()
    color = "&color=white" if "w" in fen else "&color=black"
    await query.message.reply_photo(photo=f"https://lichess1.org/export/fen.gif?fen={fen}{color}",
        caption=f"<a href='https://lichess.org/editor/{fen.replace(" ","_")})'>Your endgame</a>",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
async def stats_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(x, callback_data=f"stats:{x}")] for x in templates
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Select endgame to see stats', reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    template_name = query.data.split(":")[1]
    await update.message.reply_text(f"{template_name}'s stats")
async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    _,result , endgame_type = query.data.split(":")
    await query.answer()
    payload = {
                "user":update.effective_user.id,
                "endgame_type": endgame_type,
                "result": result

            }
    requests.get(
        f"{api}add_result/",
            params=payload, proxies={"http": "", "https": ""})
if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if TOKEN is None:
        raise NoTokenError("Create .env file containing your token")
    api = "http://spiel:8000/api/"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('train', train))
    app.add_handler(CommandHandler('stats', stats_menu))
    app.add_handler(CallbackQueryHandler(send_game, pattern="train:"))
    app.add_handler(CallbackQueryHandler(stats, pattern="stats:"))
    app.add_handler(CallbackQueryHandler(send_result, pattern="result:"))

    print('Bot running...')
    app.run_polling()
