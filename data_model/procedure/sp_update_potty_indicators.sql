create or replace procedure sp_update_potty_indicators()
language sql
begin atomic
	update kirby.fact_activity 
	set accurate_ind = case when note ilike '%outside%' then 0
		   when note ilike '%near%' or note ilike '%next to pp%' or  note ilike '%beside%pp%' then 0
		   when note ilike '%not precise%' then 0
		   when note ilike '%crate%' then 0
		   when note ilike '%under%desk%' then 0
		   when note ilike '%kitchen%' then 0
		   when note ilike '%not on pp%' then 0
		   when note ilike '%spot on%' then 1
		   when note ilike '%pppp%' then 1
		   when note ilike '%brpp%' then 1
		   when note ilike '%bapp%' then 1
		   when note ilike '%lrpp%' then 1
		   when note ilike '%br pp%' then 1 
		   when note ilike '%pp%' then 1
		   when note ilike '%out%' or note ilike '%outdoor%' then 1
		   when note is null then 0 else 0 end,
	self_initiated_ind = case when note ilike '%herself%' then 1 else 0 end,
	coporphagia_ind = case when note ilike '%eat%stop her%' then 0
	                       when note ilike '%eat%' and note not like '%treat%' then 1 else 0 end,
	update_datetime = current_timestamp,
	update_process = 'sp_update_potty_indicators'
	
	where note is not null and act_datetime >= '2025-02-18' and (activity ilike '%Poop%' or activity ilike '%Pee%')
	;

end;