# -*- coding: utf-8 -*-
from plane import Plane
from my_vector import Vector

p1 = Plane(normal_vector=Vector(['-0.412','3.806','0.728']), constant_term='-3.46')
p2 = Plane(normal_vector=Vector(['1.03','-9.515','-1.82']), constant_term='8.65')
print 'first pair of planes are parallel?: {}'.format(p1.is_parallel_to(p2))
print 'first pair of planes are equal?: {}'.format(p1 == p2)

p3 = Plane(normal_vector=Vector(['2.611','5.528','0.283']), constant_term='4.6')
p4 = Plane(normal_vector=Vector(['7.715','8.306','5.342']), constant_term='3.76')
print 'second pair of planes are parallel?: {}'.format(p3.is_parallel_to(p4))
print 'second pair of planes are equal?: {}'.format(p3 == p4)

p5 = Plane(normal_vector=Vector(['-7.926','8.625','-7.212']), constant_term='-7.95')
p6 = Plane(normal_vector=Vector(['-2.642','2.875','-2.404']), constant_term='-2.44')
print 'third pair of planes are parallel?: {}'.format(p5.is_parallel_to(p6))
print 'third pair of planes are equal?: {}'.format(p5 == p6)