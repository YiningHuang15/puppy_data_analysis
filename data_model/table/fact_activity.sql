create table kirby.fact_activity
(
activity_id serial primary key,
activity varchar(50),
act_datetime timestamp,
note varchar(500),
insert_datetime timestamp,
insert_process varchar(50),
accurate_ind int,
self_initiated_ind int,
coporphagia_ind int,
update_datetime timestamp,
update_process timestamp
)
;