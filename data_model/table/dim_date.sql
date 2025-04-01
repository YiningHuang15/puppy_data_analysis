create table kirby.dim_date
(
date_key int primary key,
date date,
year int,
quarter int,
month int,
day int,
MonthYear varchar(10),
month_name varchar(15),
month_name_short varchar(3),
day_of_week_name varchar(15),
day_of_week_name_short varchar(3),
day_of_week_num int,
rp_week_start_date date,
rp_day_of_week_num int
)
;