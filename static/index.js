document.addEventListener("DOMContentLoaded", function() {
    // Находим все скрытые карточки товаров
    var hiddenProducts = document.querySelectorAll('.card.hidden');
    
    // Если количество скрытых карточек товаров меньше или равно 4, делаем кнопку невидимой
    if (hiddenProducts.length <= 4) {
        document.querySelector('.btn').style.display = 'none';
    }

    document.querySelector('.btn').addEventListener('click', function() {
        // Находим все скрытые карточки товаров
        var hiddenProducts = document.querySelectorAll('.card.hidden');

        // Показываем следующие четыре скрытые карточки товаров
        for (var i = 0; i < 4; i++) {
            if (hiddenProducts[i]) {
                hiddenProducts[i].classList.remove('hidden');
            } 
        }
            if (!hiddenProducts[4]) {
                // Если больше нет скрытых карточек товаров, скрываем кнопку "Показать еще"
                this.style.display = 'none';
            }
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     var cards = document.querySelectorAll('.card');
//     var categoryCount = cards.length;

//     // Проверяем количество карточек в категории
//     if (categoryCount < 5) {
//         // Если в категории меньше 5 товаров, скрываем кнопку "Показать еще"
//         document.querySelector('.btn').style.display = 'none';
//     }
// });