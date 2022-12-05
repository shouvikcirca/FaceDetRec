import pytest

class TestModelvalidator:
	def test_properties(self)->None:
		from pairMatchingTesting import ModelValidator
		obj = ModelValidator(0.4)
		numProps = len(dir(obj))
		assert numProps == 35	

	def test_datasetprops(self)->None:
		from pairMatchingTesting import ModelValidator
		obj = ModelValidator(0.4)
		assert obj.dataPaths['LFW']['path'] == 'LFW'
		assert obj.dataPaths['LFW']['size'] == 500
		
