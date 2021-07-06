## Поиска вакансий
Описание: Поиск вакансий по ключевому слову в режиме вопрос - ответ. Для поиска используется обратный индекс, 
для увеличения полноты индекса - w2v обученный на hr данных. Движок автоматически обновляет вакансии и индексы.

## Кэш
Для запуска движка требуется memcahed, локальная запускается следующей командой:
```
docker run --name my-memcache -p 11211:11211 -d memcached
```
Дополнительные параметры для кэша:
```
-m 64    # Maximum memory to use, in megabytes. 64MB is default.
-p 11211    # Default port, but being explicit is nice.
-I 5m # Maximum memory to use with one key
```
Для приложения требуется запустить кэш с расширенной памятью
```
docker run --name my-memcache -I 5m -p 11211:11211 -d memcached
```

## gcloud
Аутентификация в кластере gcloud
```
gcloud container clusters get-credentials cluster-1 --zone europe-north1-a --project disco-sector-317101
```

## postgres
Команды для запуска postgres 9.6 контейнере
```
docker run -d  --name some-postgres -p 5434:5432 -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=user -e POSTGRES_DB=db postgres:9.6
```

## описание таблиц
vacancy_info
```
create table vacancy_info
(
	id int,
	title varchar,
	footer varchar,
	header varchar,
	requirements varchar,
	duties varchar,
	conditions varchar,
	date date,
	locality int,
	region int,
	company int
);
```
index_map
```
create table vacancy_info
(
	extended_index varchar,
	original_index varchar,
);
```
cache_index
```
create table cache_index
(
	original_index varchar,
	vacancy_id int,
);
```

## Типовые операции с таблицей
переименование таблицы
```
alter table vacancy_info rename to vacancy_content;
```
поисковой запрос к базе
```
select cache_index.vacancy_id, count(cache_index.vacancy_id) as counter from (select original_index from index_map
where extended_index = 'django') as times
join cache_index on times.original_index = cache_index.original_index
group by cache_index.vacancy_id
order by counter desc
```