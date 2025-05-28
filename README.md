Крутилка by voltako

Запускать через krutilka.py

Она автоматически создаст операторов, пользователей согласно тз и лог для всех чатов

Потом, через модуль finder сделаем все возможные выгрузки, сохранит их в деректории search_result и выведет результаты в консоль

Решение второй задачи: 
а) select ticket_client from tickets where csat < 3
б) select ticket_id from tickets where text like '%отлично%' order by csat desc
в) select order_client_id as frequent_customer, sum(price) as max_sum from orders where place in ('Теремок','Вкусно и точка') and price between 2000 and 10000 and order_client_id in ( select order_client_id from orders where place in ('Теремок','Вкусно и точка') group by order_client_id having count(order_id) >5) group by order_client_id
г) SELECT o.order_id, o.price, o.place, c.client_id, c.username AS client_username, c.name AS client_name, c.age AS client_age, c.city AS client_city, t.ticket_id, t.csat AS ticket_rating, t.text AS ticket_message, t.date AS ticket_date FROM orders o LEFT JOIN clients c ON o.order_client_id = c.client_id LEFT JOIN tickets t ON o.order_id = t.ticket_order_id LIMIT 1000
