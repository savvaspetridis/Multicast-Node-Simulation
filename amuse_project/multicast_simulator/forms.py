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

	# bitRate = forms.TypedChoiceField(coerce=int, empty_value=0, label='Bit Rate', choices=BITRATES) #original
	bitRate = forms.ChoiceField(required=False, label='Bit Rate', choices=BITRATES, widget=forms.Select(attrs={'ng-show' : 'showBitRate'}))

	
	INTERVALS = (
		(0.5, 0.5),
		(1.0, 1.0),
		(2.0, 2.0),
	)

	updateInterval = forms.TypedChoiceField(coerce=float, empty_value=0.0, label='Update Interval', choices=INTERVALS) # origninal
	# updateInterval = forms.ChoiceField(required=False, label='Update Interval', choices=INTERVALS)

	
	ALGORITHMS = (
		('NONE', 'None'),
		('RAND', 'k_Random'),
		('WORST', 'k_Worst'),
		('AMUSE', 'Amuse'),
	)
	
	# Raphael: just added widget field
	fbNodeAlg = forms.ChoiceField(label='Feedback Node Algorithm', required=False, choices=ALGORITHMS, widget=forms.Select(attrs={'ng-model' : 'my.option'}))
	# fbNodeAlg = forms.ChoiceField(label='Feedback Node Algorithm', required=False, choices=ALGORITHMS) # orignal
	
	# Raphael: just added widgets again
	k = forms.IntegerField(label='k', required=False, widget=forms.NumberInput(attrs={'ng-show' : 'showK'}))
	# k = forms.IntegerField(label='k', required=False) # original
	d = forms.IntegerField(label='Distance:', required=False, widget=forms.NumberInput(attrs={'ng-show' : 'showDistance'}))
	# d = forms.IntegerField(label='Distance:', required=False) # original


