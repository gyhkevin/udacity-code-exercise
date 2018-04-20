# -*- coding: utf-8 -*-
from decimal import Decimal, getcontext
from copy import deepcopy

from my_vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):
    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]

    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector
        k = self[row].constant_term

        new_normal_vector = n.times_scalar(coefficient)
        new_constant_term = k * coefficient

        self[row] = Plane(normal_vector=new_normal_vector,
                          constant_term=new_constant_term)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        n1 = self[row_to_add].normal_vector
        n2 = self[row_to_be_added_to].normal_vector
        k1 = self[row_to_add].constant_term
        k2 = self[row_to_be_added_to].constant_term

        new_normal_vector = n1.times_scalar(coefficient).plus(n2)
        new_constant_term = (k1 * coefficient) + k2

        self[row_to_be_added_to] = Plane(normal_vector=new_normal_vector,
                                         constant_term=new_constant_term)

    def compute_triangular_form(self):
        # 复制原方程组
        system = deepcopy(self)
        num_equations = len(system)
        num_variables = system.dimension

        j = 0
        for i in xrange(num_equations):
            while j < num_variables:
                # 第i行第j个变量的系数
                c = MyDecimal(system[i].normal_vector[j])
                # 当前系数c等于0，则需要适合的行交换0
                if c.is_near_zero():
                    # 如果在i下面找到变量j的系数不为零的行，则将改行与i交换
                    swap_succeeded = system.swap_with_row_below_for_nonzero_coefficient_if_able(i, j)
                    if not swap_succeeded:
                        j += 1
                        continue
                # 清除行i下面所有具有变量i的项
                system.clear_coefficents_below(i, j)
                # 使j递增，以转到下个变量
                j += 1
                break
        return system

    # 寻找给定变量的非零系数
    def swap_with_row_below_for_nonzero_coefficient_if_able(self, row, col):
        num_equations = len(self)

        for k in xrange(row + 1, num_equations):
            coefficient = MyDecimal(self[k].normal_vector[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True

        return False

    def clear_coefficents_below(self, row, col):
        num_equations = len(self)
        beta = MyDecimal(self[row].normal_vector[col])
        # 计算给定行需要乘以的比例alpha，以便消除给定行下面的k
        for k in xrange(row + 1, num_equations):
            n = self[k].normal_vector
            gamma = n[col]
            # 计算alpha它会将给定行系数的倒数乘以行k中相应系数的负数
            alpha = -gamma / beta
            # 将alpha倍的给定行与行k相乘
            self.add_multiple_times_row_to_row(alpha, row, k)

    """
    计算RREF(Reduced Row-Echelon Form)
    这是一个独特的三角形，每个主变量（即首项变量）的系数都是1，且正好位于一个等式里
    """

    def compute_rref(self):
        tf = self.compute_triangular_form()

        num_equations = len(tf)
        # 计算主变量索引，即每行首项变量的索引列表
        pivot_indices = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(num_equations)[::-1]:
            j = pivot_indices[i]
            if j < 0:
                continue
            tf.scale_row_to_make_coefficient_equal_one(i, j)
            tf.clear_coefficents_above(i, j)

        return tf

    # 在给定行两边乘以指定行
    def scale_row_to_make_coefficient_equal_one(self, row, col):
        n = self[row].normal_vector
        # 指定变量的系数的倒数
        beta = Decimal('1.0') / n[col]
        self.multiply_coefficient_and_row(beta, row)

    def clear_coefficents_above(self, row, col):
        for k in range(row)[::-1]:
            n = self[k].normal_vector
            alpha = -(n[col])
            self.add_multiple_times_row_to_row(alpha, row, k)

    def compute_solution(self):
        try:
            # return self.do_gaussian_elimination_and_extract_solution()
            return self.do_gaussian_elimination_and_parametrize_solution()
        except Exception as e:
            if (str(e) == self.NO_SOLUTIONS_MSG or
                    str(e) == self.INF_SOLUTIONS_MSG):
                return str(e)
            raise e

    def do_gaussian_elimination_and_extract_solution(self):
        # 计算方程组的最简化的梯阵形式，然后看看是否有矛盾的等式
        rref = self.compute_rref()
        # 0=k的形式，或者太多主变量，如果有则抛出异常
        rref.raise_exception_if_contradictory_equation()
        rref.raise_exception_if_too_few_pivots()
        # 如果未有异常，则返回一个向量，向量坐标是方程的常量项
        num_variables = rref.dimension
        solution_coordinates = [rref.planes[i].constant_term for i in xrange(num_variables)]
        return Vector(solution_coordinates)

    def raise_exception_if_contradictory_equation(self):
        # 检测每个平面，法向量的坐标是否全为0
        for p in self.planes:
            try:
                # 如果全为0，则寻找常量项的非零项
                p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                # 如果在常量因子里找到非零项，则表明存在矛盾的等式，抛出相应的异常
                if str(e) == 'No nonzero elements found':
                    constant_term = MyDecimal(p.constant_term)
                    if not constant_term.is_near_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                raise e

    def raise_exception_if_too_few_pivots(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        # 计算非负索引的数量
        # 因为每行第一个非零项的索引返回的是-1，如果行里有非零项的话，所以非零索引的数量就是主变量的数量
        num_pivot = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension
        # 将该数字与变量总数对比，如果小于则表示有无数个解
        if num_pivot < num_variables:
            raise Exception(self.INF_SOLUTIONS_MSG)

    def do_gaussian_elimination_and_parametrize_solution(self):
        rref = self.compute_rref()

        rref.raise_exception_if_contradictory_equation()
        # 得出参数化形式的方向向量
        direction_vectors = rref.extract_direction_vectors_for_parametrization()
        # 得出基准点
        basepoint = rref.extract_basepoint_for_parametrization()
        # 创建并返回相应的参数化对象
        return Parametrization(basepoint, direction_vectors)

    def extract_direction_vectors_for_parametrization(self):
        # 通过不是主变量确定自由变量，然后对每个自由变量构建一个方向向量
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        free_variable_indices = set(range(num_variables)) - set(pivot_indices)

        direction_vectors = []

        for free_var in free_variable_indices:
            vector_coords = [0] * num_variables
            # 自由变量对应的坐标为1，表示将该变量设为等于它自己
            vector_coords[free_var] = 1
            # 对方程组中的每个等式确定主变量
            for i, p in enumerate(self.planes):
                pivot_var = pivot_indices[i]
                if pivot_var < 0:
                    break
                # 找到等式中自由变量的系数，然后将主变量对应的坐标设为该系数的倒数
                # 因为在参数形式化时，需要从等式两边消去自由变量
                vector_coords[pivot_var] = -p.normal_vector[free_var]
            direction_vectors.append(Vector(vector_coords))

        return direction_vectors

    def extract_basepoint_for_parametrization(self):
        num_variables = self.dimension
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()

        basepoint_coords = [0] * num_variables

        for i, p in enumerate(self.planes):
            pivot_var = pivot_indices[i]
            if pivot_var < 0:
                break
            basepoint_coords[pivot_var] = p.constant_term

        return Vector(basepoint_coords)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, i):
        return self.planes[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i + 1, p) for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class Parametrization(object):
    """docstring for Parametrization"""
    BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG = ('The basepoint and direction'
                                                      ' vectors should all live in the same dimension')

    def __init__(self, basepoint, direction_vectors):

        self.basepoint = basepoint
        self.direction_vectors = direction_vectors
        self.dimension = self.basepoint.dimension

        try:
            for v in direction_vectors:
                assert v.dimension == self.dimension
        except AssertionError:
            raise Exception(BASEPT_AND_DIR_VECTORS_MUST_BE_IN_SAME_DIM_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

s = LinearSystem([p0, p1, p2, p3])

print s.indices_of_first_nonzero_terms_in_each_row()
print '{},{},{},{}'.format(s[0], s[1], s[2], s[3])
print len(s)
print s

s[0] = p1
print s

print MyDecimal('1e-9').is_near_zero()
print MyDecimal('1e-11').is_near_zero()
