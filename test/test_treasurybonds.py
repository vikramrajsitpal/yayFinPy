from decimal import Decimal
from yayFinPy.treasury_bonds import TreasuryBond

def test_constructor():
	try:
		bond = TreasuryBond("^TNX")
		assert(bond != None)
		return 1
	except Exception as e:
		print("Test Failed: test_constructor: ", e)
	return 0

def test_constructor_failure():
	try:
		bond = TreasuryBond("INVALID")
	except:
		return 1
	print("Test Failed: test_constructor_failure")
	return 0

def test_bonds_attributes():   
	try:
		bond = TreasuryBond("^TNX")
		assert(bond != None)
		assert(type(bond.name) == str)
		assert(type(bond.age) == Decimal)
		assert(bond.name == "CBOE Interest Rate 10 Year T No")
		return 1
	except Exception as e:
		print("Test Failed: test_bonds_attributes", e)
	return 0


def test_bond_returns():
	try:
		bond = TreasuryBond("^TNX")
		returns_val = bond.returns()
		assert(type(returns_val) == Decimal)
		return 1
	except Exception as e:
		print("Test Failed: test_bond_returns", e)
	return 0    



if __name__ == '__main__':
	success = []
	success.append(test_constructor())
	success.append(test_constructor_failure())
	success.append(test_bonds_attributes())
	success.append(test_bond_returns())

	print("Treasury bonds Test Done: (%d/%d) Successful"%(sum(success), len(success)))