#Savvas

from django import forms

class SimulationForm(forms.Form):
	BITRATES = (
		(6, 6),
		(9, 9),
		(12, 12),
		(18, 18),
		(24, 24),
		(36, 36),
		(48, 48),
		(54, 54), 
	)

	bitRate = forms.TypedChoiceField(coerce=int, empty_value=0, label='Bit Rate', choices=BITRATES)

	
	INTERVALS = (
		(0.5, 0.5),
		(1.0, 1.0),
		(2.0, 2.0),
	)

	updateInterval = forms.TypedChoiceField(coerce=float, empty_value=0.0, label='Update Interval', choices=INTERVALS)

	
	ALGORITHMS = (
		('RAND', 'k_Random'),
		('WORST', 'k_Worst'),
		('AMUSE', 'Amuse'),
	)
	
	fbNodeAlg = forms.ChoiceField(label='Feedback Node Algorithm', required=False, choices=ALGORITHMS)
	k = forms.IntegerField(label='k')
	d = forms.IntegerField(label='Distance:')


