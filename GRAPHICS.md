Track()
-------

Is the object containing individual blocks that displays a complete sound signal


Sample()
--------

Is a region in the Track selected by dragging the mouse over the wave.

### Events

- play_sound(self, evn)
	* Reproduce the wave sample and display a process line with draw_time_lapse

- draw_sample(self)
	* Draw the sample sound spectrum in the Sample track


Window()
--------
Contain Tracks and Samples and handle window closing and menu context

### Events

- add_track(self)
	* creates a new Track using the Window instance as root for tk
- selectZoneStart(self, ev, nid)
	* detects the start to drag point in the track
	* nid: Track id
	* ev: tk click event
- selectZoneEnd(self, ev, state, nid)
	* detects the ending point of the selection
	* nid: Track id
	* state: indicates if the user is dragging or just clicking
	* ev: tk click event
- set_sample(self, data, nid)
	* creates a new Sample based on data
