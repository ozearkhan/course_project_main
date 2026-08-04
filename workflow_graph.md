---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	collect_requirements(collect_requirements)
	search(search)
	assemble_itinerary(assemble_itinerary)
	budget_check(budget_check)
	present_options(present_options)
	execute_booking(execute_booking)
	confirm(confirm)
	__end__([<p>__end__</p>]):::last
	__start__ --> collect_requirements;
	assemble_itinerary --> budget_check;
	budget_check -. &nbsp;budget_failed&nbsp; .-> __end__;
	budget_check -. &nbsp;within_budget&nbsp; .-> present_options;
	budget_check -. &nbsp;revise&nbsp; .-> search;
	collect_requirements --> search;
	execute_booking -. &nbsp;confirmed&nbsp; .-> confirm;
	execute_booking -. &nbsp;retry&nbsp; .-> search;
	present_options --> execute_booking;
	search --> assemble_itinerary;
	confirm --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
