from .forms import ContactForm

def base_context(request):
    form = ContactForm()  # Создаем форму обратной связи
    return {'contact_form': form}  # Добавляем в контекст
