/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/
SELECT category.name AS Category, COUNT(film_category.film_id) AS Films
FROM (
    category JOIN film_category ON category.category_id = film_category.category_id
    )
GROUP BY category.name;


/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/
SELECT actor.first_name || ' ' || actor.last_name AS FullName, SUM(film.rental_rate * film.rental_duration) AS Profit
FROM (
    (actor JOIN film_actor ON actor.actor_id = film_actor.actor_id)
    JOIN film ON film.film_id = film_actor.film_id
     )
GROUP BY FullName
ORDER BY Profit desc
LIMIT 10;


/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/
SELECT category.name, SUM(film.rental_rate * film.rental_duration) AS Profit
FROM (
    (category JOIN film_category ON category.category_id = film_category.category_id)
    JOIN film ON film_category.film_id = film.film_id
     )
GROUP BY category.name
ORDER BY Profit
LIMIT 1;


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
SELECT film.title AS Film
FROM (film LEFT JOIN inventory ON film.film_id = inventory.film_id)
WHERE inventory.film_id IS NULL;


/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
SELECT actor.first_name || ' ' || actor.last_name AS Actor, COUNT(category.name) as Filmed
FROM(
    (((actor JOIN film_actor ON actor.actor_id = film_actor.actor_id)
    JOIN film ON film.film_id = film_actor.film_id)
    JOIN film_category ON film.film_id = film_category.film_id)
    JOIN category ON film_category.category_id = category.category_id
    )
WHERE category.name = 'Children'
GROUP BY Actor
ORDER BY Filmed desc
LIMIT 3;