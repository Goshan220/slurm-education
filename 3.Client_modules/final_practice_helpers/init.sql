CREATE SCHEMA usage_stats;

CREATE TABLE usage_stats.resources
(
	id serial NOT NULL,
	resource text,
	team text,
	dimension text,
	collect_date date,
	usage float
);

CREATE unique INDEX resources_id_uindex
	ON usage_stats.resources (id);

ALTER TABLE usage_stats.resources
	ADD constraint resources_pk
		PRIMARY KEY (id);




