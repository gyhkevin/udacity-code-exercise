# -*- coding: utf-8 -*-
from decimal import Decimal, getcontext

from my_vector import Vector

getcontext().prec = 30

class Line(object):
	"""docstring for Line"""
	NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'
	def __init__(self, normal_vector=None, constant_term=None):
		self.dimension = 2

		if not normal_vector:
			all_zeros = ['0']*self.dimension
			normal_vector = Vector(all_zeros)
		self.normal_vector = normal_vector

		if not constant_term:
			constant_term = Decimal('0')
		self.constant_term = Decimal(constant_term)

		self.set_basepoint()

	def __str__(self):

		num_decimal_places = 3

		def write_coefficient(coefficient, is_initial_term=False):
			coefficient = round(coefficient, num_decimal_places)
			if coefficient % 1 == 0:
				coefficient = int(coefficient)

			output = ''

			if coefficient < 0:
				output += '-'
			if coefficient > 0 and not is_initial_term:
				output += '+'

			if not is_initial_term:
				output += ' '


			constant = int(constant)
		output += ' = {}'.format(constant)

		return output

	@staticmethod
	def first_nonzero_index(iterable):
		for k, item in enumerate(iterable):
			if not MyDecimal(item).is_near_zero():
				return k

		raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

	def __eq__(self, ell):

		if self.normal_vector.is_zero():
			if not ell.normal_vector.is_zero():
				return False
			else:
				diff = self.constant_term - ell.constant_term
				return MyDecimal(diff).is_near_zero()
		elif ell.normal_vector.is_zero():
			return False

		if not self.is_parallel_to(ell):
			return False

		x0 = self.basepoint
		y0 = ell.basepoint

		basepoint_difference = x0.minus(y0)

		n = self.normal_vector
		return basepoint_difference.is_orthogonal_to(n)

	def is_parallel_to(self, ell):
		n1 = self.normal_vector
		n2 = ell.normal_vector

		return n1.is_parallel_to(n2)

	def set_basepoint(self):
		try:
			n = self.normal_vector
			c = self.constant_term
			basepoint_coords = ['0']*self.dimension

			initial_index = Line.first_nonzero_index(n)
			initial_coefficient = n[initial_index]

			basepoint_coords[initial_index] = c/initial_coefficient
			self.basepoint = Vector(basepoint_coords)
		except Exception as e:
			raise e

	def intersection_with(self, ell):
		try:
			A, B = self.normal_vector.coordinates
			C, D = ell.normal_vector.coordinates
			k1 = self.constant_term
			k2 = ell.constant_term

			x_numerator = D*k1 - B*k2
			y_numerator = -C*k1 + A*k2
			one_over_denom = Decimal('1')/(A*D - B*C)
			
			return Vector(x_numerator, y_numerator).times_scalar(one_over_denom)

		except ZeroDivisionError:
			if self == ell:
				return self
			else:
				return None

class MyDecimal(Decimal):
	"""docstring for MyDecimal"""
	def __init__(self, arg):
		# super(MyDecimal, self).__init__()
		self.arg = arg

	def is_near_zero(self, eps=1e-10):
		return abs(self) < eps

		
ell1 = Line(normal_vector=Vector(['4.046','2.836']), constant_term='1.21')
ell2 = Line(normal_vector=Vector(['10.115','7.09']), constant_term='3.025')
print( 'intersection 1:', ell1.intersection_with(ell2))




