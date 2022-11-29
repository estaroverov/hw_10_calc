
from telegram import *
import telegram.ext as te
import model_div
import model_logger
import model_minus
import model_mult
import model_sum
async def hello(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
global file

file = 'val.csv'
#####################

 
BEGIN, ADD, OP_RATIONAL, OP_COMPLEX = range(4)

async def start(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text( "Добро пожаловать в калькулятор-бот")
    reply_keyboard = [["Начнем"]]
    await update.message.reply_text(
        "Начнем",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Меню"
        ),
    )
    return BEGIN
async def begin(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Рациональные числа", "Комплексные числа"]]
    await update.message.reply_text(
        "Выберите пункт меню",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder="Меню"
        ),
    )
    return ADD
async def add(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Рациональные числа":
        await update.message.reply_text(
            "Операция с рациональными числами",
            reply_markup=ReplyKeyboardRemove()
        )
        return OP_RATIONAL
    elif update.message.text == "Комплексные числа":
        await update.message.reply_text(
            "Операция с комплексными числами",
            reply_markup=ReplyKeyboardRemove()
        )
        return OP_COMPLEX
    else: 
        await update.message.reply_text("Неверный ввод")
        return BEGIN

async def op_rational(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Повторить"]]
    await update.message.reply_text(
        "Результат: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder="Меню"
        )
    )
    msg = update.message.text.split()
    result = ''
    if len(msg) == 3:
        if msg[1] == "+":
            result = model_sum.do_it(float(msg[0]),float(msg[2]))
        elif msg[1] == '*':
            result = model_mult.do_it(float(msg[0]),float(msg[2]))
        elif msg[1] == '-':
            result = model_minus.do_it(float(msg[0]),float(msg[2]))
        elif msg[1] == '/':
            result = model_div.do_it(float(msg[0]),float(msg[2]))
        else:
            await update.message.reply_text("Ошибка. Неверный ввод, попробуйте ввод еще раз")
        model_logger.Logger(msg[0],msg[2],msg[1],result)
        await update.message.reply_text(str(result))
        return BEGIN
    else:
        await update.message.reply_text("Неверный ввод")
        return OP_RATIONAL

async def op_complex(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Повторить"]]
    await update.message.reply_text(
        "Результат: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder="Меню"
        )
    )
    msg = update.message.text.split()
    result = ''
    if len(msg) == 3:
        if msg[1] == "+":
            result = model_sum.do_it(complex(msg[0]),complex(msg[2]))
        elif msg[1] == '*':
            result = model_mult.do_it(complex(msg[0]),complex(msg[2]))
        elif msg[1] == '-':
            result = model_minus.do_it(complex(msg[0]),complex(msg[2]))
        elif msg[1] == '/':
            result = model_div.do_it(complex(msg[0]),complex(msg[2]))
        else:
            await update.message.reply_text("Ошибка. Неверный ввод, попробуйте ввод еще раз")
        model_logger.Logger(msg[0],msg[2],msg[1],result)
        await update.message.reply_text(str(result))
        return BEGIN
    else:
        await update.message.reply_text("Неверный ввод")
        return OP_COMPLEX




async def cancel(update: Update, context: te.ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Ввод завершен.", reply_markup=ReplyKeyboardRemove()
    )

    return te.ConversationHandler.END



def main() -> None:
    app = te.ApplicationBuilder().token(
    "ВАШ_ТОКЕН").build()
    conv_handler = te.ConversationHandler(
        entry_points=[te.CommandHandler("start", start)],
        states={
            BEGIN: [te.MessageHandler(te.filters.TEXT,begin)],
            ADD: [te.MessageHandler(te.filters.TEXT, add)],
            OP_RATIONAL: [te.MessageHandler(te.filters.TEXT,op_rational)],
            OP_COMPLEX: [te.MessageHandler(te.filters.TEXT,op_complex)],
            
        },
        fallbacks=[te.CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()