#Savvas

from django import forms

class SimulationForm(forms.Form):
	bitRate = forms.IntegerField(label='Bit Rate')
	updateInterval = forms.DecimalField(label='Update Interval', max_digits=2, decimal_places=1)

