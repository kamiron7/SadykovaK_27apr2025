-- Выберите уникальные регионы сбора грибов
SELECT DISTINCT r.name
FROM Mushrooms m
JOIN Regions r ON m.primary_region_id = r.region_id;

-- Выведите название, сезон сбора и съедобность грибов, которые относятся к категории «Трубчатые»
SELECT m.name, m.season, m.edible
FROM Mushrooms m
JOIN Categories c ON m.category_id = c.category_id
WHERE c.name = 'Трубчатые';

-- Посчитайте количество грибов для каждой категории. Выведите название категории и количество в порядке убывания.
SELECT c.name AS category_name, COUNT(m.mushroom_id) AS mushroom_count
FROM Categories c
LEFT JOIN Mushrooms m ON m.category_id = c.category_id
GROUP BY c.name
ORDER BY mushroom_count DESC;

-- Выведите название и описание съедобных грибов, которые лучше всего собирать в пяти самых больших по размеру регионов
SELECT m.name, m.description
FROM Mushrooms m
JOIN Regions r ON m.primary_region_id = r.region_id
WHERE m.edible = TRUE
AND r.region_id IN (
    SELECT region_id
    FROM Regions
    ORDER BY size DESC
    LIMIT 5
);

-- Выведите названия всех грибов, которые растут весной,
-- относятся к категории «Пластинчатые» и которые лучше всего собирать в местах размером до 6000
SELECT m.name
FROM Mushrooms m
JOIN Categories c ON m.category_id = c.category_id
JOIN Regions r ON m.primary_region_id = r.region_id
WHERE m.season = 'весна'
  AND c.name = 'Пластинчатые'
  AND r.size <= 6000;