# Создание собственного класса

class TitleMixin:
    '''Создание атрибута Title'''
    title = None

    def get_context_data(self, **kwargs):  # Для передачи контекста используем метод "get_context_data"
        context = super(TitleMixin, self).get_context_data(**kwargs)  # для сохранения функционала метода родительского класса
        context['title'] = self.title  # переопределение (расширение) метода родительского класса
        return context


# Вывод описания класса
# print(TitleMixin.__doc__)
