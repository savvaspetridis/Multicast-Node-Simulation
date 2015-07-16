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
	bitRate = forms.ChoiceField(required=False, label='Bit Rate', choices=BITRATES, widget=forms.Select(attrs={'ng-model' : 'bit_rate_update'}))

	
	INTERVALS = (
		(0.5, 0.5),
		(1.0, 1.0),
		(2.0, 2.0),
	)

	updateInterval = forms.TypedChoiceField(coerce=float, empty_value=0.0, label='Update Interval', choices=INTERVALS, widget=forms.Select(attrs={'ng-model' : 'intervalCount'})) # origninal
	# updateInterval = forms.ChoiceField(required=False, label='Update Interval', choices=INTERVALS)

	
	ALGORITHMS = (
		('NONE', 'None'),
		('RAND', 'k_Random'),
		('WORST', 'k_Worst'),
		('AMUSE', 'Amuse'),
	)
	
	# Raphael: just added widget field
	fbNodeAlg = forms.ChoiceField(label='Feedback Node Algorithm', required=False, choices=ALGORITHMS, widget=forms.Select(attrs={'ng-model' : 'my.option', 'ng-change' : 'check()'}))
	# widget=forms.Select(attrs={ 'ng-change' = 'check()'}))
	# fbNodeAlg = forms.ChoiceField(label='Feedback Node Algorithm', required=False, choices=ALGORITHMS) # orignal
	
	# Raphael: just added widgets again
	k = forms.IntegerField(label='k', required=False, widget=forms.NumberInput(attrs={'ng-show' : 'showK', 'ng-model' : 'k_nodes'}))
	# k = forms.IntegerField(label='k', required=False) # original
	d = forms.IntegerField(label='Distance:', required=False, widget=forms.NumberInput(attrs={'ng-show' : 'showDistance', 'ng-model': 'distance'}))
	# d = forms.IntegerField(label='Distance:', required=False) # original


	# for rate adaptation. may change from float or integer fields or vice versa
	

	H = forms.FloatField(label='H-low Threshold', required=False, widget=forms.NumberInput(attrs={'ng-model' : 'H'}))
	Delta = forms.FloatField(label='Delta', required=False, widget=forms.NumberInput(attrs={'ng-model' : 'Delta'}))
	W_min = forms.IntegerField(label='Window minimum', required=False, widget=forms.NumberInput(attrs={'ng-model' : 'W_min'}))
	W_max = forms.IntegerField(label='Window maximum', required=False, widget=forms.NumberInput(attrs={'ng-model' : 'W_max'}))
	time = forms.FloatField(label='Time:', required=False, widget=forms.NumberInput(attrs={'ng-model' : 'windowTime'}))
	A_max = forms.IntegerField(label='Maximum abnormal nodes', required=False, widget=forms.NumberInput(attrs={'ng-model' : 'A_max'}))





