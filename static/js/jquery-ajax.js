// Когда html документ готов (прорисован)
$(document).ready(function () {

    var successMessage = $("#jq-notification");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 3сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 3000);

                var notification = $('#notification');

                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                if (cartCount > 0) {
                    $("#checkout-button").show();  // Показать кнопку
                }

            },
            

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // Ловим собыитие клика по кнопке удалить товар из корзины
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 3000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

                if (cartCount === 0) {
                    $("#checkout-button").hide();  // Скрыть кнопку
                }
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // // Теперь + - количества товара 
    // // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 3000);

                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }

    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 3 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 3000);
    }


    $('#staticBackdrop').on('hidden.bs.modal', function() {
        $(this).find('form')[0].reset();  // Сбрасываем поля формы при закрытии
        // Удаляем все сообщения об ошибках
        $(this).find('.alert').remove();
    });
    
    // Обработчик отправки формы через AJAX
    $("#contactForm").on("submit", function(e) {
        e.preventDefault();  // Останавливаем действие по умолчанию
        var formData = $(this).serialize();  // Получаем данные формы
    
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),  // URL из формы
            data: formData,
            success: function(data) {
                if (data.success) {
                    // Если успешно, закрываем модальное окно
                    $("#staticBackdrop").modal("hide");
    
                    // Добавляем зеленое уведомление
                    var notification = $('<div class="alert alert-success alert-dismissible fade show">Сообщение отправлено успешно!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button></div>');
                    
                    // Добавляем уведомление в начало контейнера
                    $("#notification-container").append(notification);
    
                    // Удаляем уведомление через 3 секунды
                    setTimeout(function() {
                        notification.alert("close");
                    }, 3000);
                }
            },
            error: function(data) {  // Если ошибка
                if (data.responseJSON && !data.responseJSON.success) {  // Проверяем ошибки валидации
                    const errors = data.responseJSON.errors;  // Получаем ошибки
                    const form = $("#contactForm");
    
                    // Удаляем предыдущие сообщения об ошибках
                    form.find(".alert").remove();
    
                    // Отображаем ошибки рядом с полями
                    Object.keys(errors).forEach(field => {
                        const errorMsg = `<div class="alert alert-danger">${errors[field].join(", ")}</div>`;
                        form.find(`[name=${field}]`).after(errorMsg);  // Показываем ошибки рядом с полем
                    });
                } else {
                    console.error("Ошибка при отправке формы");
                }
            }
        });
    });



    var isUserAuthenticated = $("#user-authenticated").val() === 'True';  // Проверка авторизации
    
    console.log("isUserAuthenticated:", isUserAuthenticated);  // Проверяем значение в консоли

    $("#checkout-button").on("click", function(e) {
        e.preventDefault();  // Блокируем действие по умолчанию

        if (!isUserAuthenticated) {
            $("#exampleModalToggle2").modal("show");  // Если неавторизован, открыть модальное окно
        } else {
            console.log("Redirecting to order creation");  // Проверка, что ветка отрабатывает
            window.location.href = '/orders/create_order/';  // Проверьте правильность URL
        }
    });
});