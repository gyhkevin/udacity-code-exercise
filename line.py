# -*- coding: utf-8 -*-
from decimal import Decimal, getcontext

from my_vector import Vector

getcontext().prec = 30


class Line(object):
    """编写直线函数类"""
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2
        # 直线等式的常量
        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector
        # 直线法向量
        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)
        # 在二维空间里，通过法向量，可以快速获得直线的方向向量，法向量更容易类推到多维空间
        # 选择一个系数不为零的变量，并将另一个变量设为零，快速算出基准点
        self.set_basepoint()


    def set_basepoint(self):

        try:
            # n = self.normal_vector.coordinates
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    # str函数使用变量x1, x2, 输出直线等式的标准形式，可以类推到多维空间
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

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i + 1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    # 找到等式的第一个非零系数
    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    # 检查两条直线是否相同
    def __eq__(self, ell):
        # 如果某条直线的法向量是零向量
        if self.normal_vector.is_zero():
            if not ell.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - ell.constant_term
                return MyDecimal(diff).is_near_zero()
        elif ell.normal_vector.is_zero():
            return False
        # 检查两条直线是否平行
        if not self.is_parallel_to(ell):
            return False
        # 从每条线上选择一个点，然后观察连接这两个点的向量
        x0 = self.basepoint
        y0 = ell.basepoint
        # 计算连接这两条直线基准点的向量
        basepoint_difference = x0.minus(y0)
        # 如果该向量与两条直线的法向量正交，那么这两条直线是同一直线
        n = self.normal_vector
        return basepoint_difference.is_orthogonal_to(n)

    # 判断法向量是否平行
    def is_parallel_to(self, ell):
        n1 = self.normal_vector
        n2 = ell.normal_vector

        return n1.is_parallel_to(n2)

    def intersection_with(self, ell):
        try:
            A, B = self.normal_vector.coordinates
            C, D = ell.normal_vector.coordinates
            k1 = self.constant_term
            k2 = ell.constant_term

            x_numerator = D * k1 - B * k2
            y_numerator = -C * k1 + A * k2
            one_over_denom = Decimal('1') / (A * D - B * C)

            return Vector([x_numerator, y_numerator]).times_scalar(one_over_denom)

        except ZeroDivisionError:
            # 除数为零的错误
            if self == ell:
                return self
            else:
                return None


class MyDecimal(Decimal):
    """拓展Decimal类"""
    # 检测某个数值是否在误差范围内，避免因为四舍五入，而出现错误答案
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
