# -*- coding: utf-8 -*-
from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
	"""
	常用向量运算
	"""
	CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
	NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
	NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'
	ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two three dims msg'
	def __init__(self, coordinates):
		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple([Decimal(x) for x in coordinates])
			self.dimension = len(coordinates)
		except ValueError:
			raise ValueError('The coordinates must be nonempty!')
		except TypeError:
			raise TypeError('The coordinates must be iterable!')

	def __str__(self):
		return 'Vector: {}'.format(self.coordinates)

	def __eq__(self, v):
		return self.coordinates == v.coordinates

	def __iter__(self):
		return self

	# 加法
	def plus(self, v):
		new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)

	# 减法
	def minus(self, v):
		new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)

	# 向量乘法
	def times_scalar(self, c):
		new_coordinates = [Decimal(c)*x for x in self.coordinates]
		return Vector(new_coordinates)

	# 计算向量大小
	def magnitude(self):
		# 计算向量的平方
		coordinates_squared = [x**2 for x in self.coordinates]
		# 平方和再开根号
		return sum(coordinates_squared).sqrt()

	# 向量标准化
	def normalized(self):
		try:
			magnitude = self.magnitude()
			return self.times_scalar(Decimal('1.0') / Decimal(magnitude))
		except ZeroDivisionError:
			# 零向量错误
			raise Exception('Cannot normalize the zero vector')

	# 点乘积（内积）
	def dot(self, v):
		return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

	# 向量角度
	def angle_with(self, v, in_degrees=False):
		try:
			u1 = self.normalized()
			u2 = v.normalized()
			"""
			如果self和v指向同一个方向，那么他俩的标准化点积应该为1。但是有时候因为计算精度丢失，
			使比例大于1，这样会在acos函数中产生范围错误，所以需要提交精度，使用Decimal
			"""
			angle_in_radian = acos(u1.dot(u2))

			if in_degrees:
				degress_per_radian = 180.0 / pi
				return angle_in_radian * degress_per_radian
			else:
				return angle_in_radian
		except Exception as e:
			if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception('Cannot compute an angle with the zero vector')
			else:
				raise e

	# 判断是否是正交向量
	def is_orthogonal_to(self, v, tolerance=1e-10):
		return abs(self.dot(v)) < tolerance

	# 判断是否是平行向量
	def is_parallel_to(self, v):
		return ( self.is_zero() or 
			v.is_zero() or 
			self.angle_with(v) == 0 or 
			self.angle_with(v) == pi)

	# 判断是否为0向量
	def is_zero(self, tolerance=1e-10):
		return self.magnitude() < tolerance

	# 计算正交向量
	def component_orthogonal_to(self, basis):
		try:
			# 获取平行向量
			projection = self.component_parallel_to(basis)
			# 返回与平行向量相减的向量
			return self.minus(projection)
		except Exception as e:
			# 出现平行向量异常
			if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
				raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
			else:
				raise e

	# 计算平行向量
	def component_parallel_to(self, basis):
		try:
			# 获得标准化向量u
			u = basis.normalized()
			# 计算u和要投影的向量self的点积
			weight = self.dot(u)
			# 并用u乘以该点积结果
			return u.times_scalar(weight)
		except Exception as e:
			# 判断零向量的情况
			if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception('Cannot compute an angle with the zero vector')
			else:
				raise e

	# 向量积
	def cross(self, v):
		try:
			x_1, y_1, z_1 = self.coordinates
			x_2, y_2, z_2 = v.coordinates
			new_coordinates = [y_1*z_2 - y_2*z_1, 
							-(x_1*z_2 - x_2*z_1), 
								x_1*y_2 - x_2*y_1
							  ]
			return Vector(new_coordinates)
		except ValueError as e:
			msg = str(e)
			if msg == 'need more than 2 values to unpack':
				self_embedded_in_R3 = Vector(self.coordinates + ('0',))
				v_embedded_in_R3 = Vector(v.coordinates + ('0',))
			elif (msg == 'too many values to unpack' or 
				msg == 'need more than 1 value to unpack'):
				raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
			else:
				raise e

	# 计算三角形的面积
	def area_of_triangle_with(self, v):
		# 三角形面积等于1/2平行四边形的面积
		return self.area_of_parallelogram_with(v) / Decimal('2.0')

	# 计算平行四边形的面积
	def area_of_parallelogram_with(self, v):
		# 向量积的大小
		cross_product = self.cross(v)
		return cross_product.magnitude()


