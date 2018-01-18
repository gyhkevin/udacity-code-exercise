# -*- coding: utf-8 -*-

import turtle

def draw_square(length, shape, color):
	brad = turtle.Turtle()
	brad.shape(shape)
	brad.color(color)
	# brad.speed(2)
	for x in xrange(4):
		brad.forward(length)
		brad.right(90)

	return brad

def draw_circle(radius, shape, color):
	c = turtle.Turtle()
	c.shape(shape)
	c.color(color)
	c.circle(radius)
	return c

def draw_triangle(length, shape, color):
	angle = turtle.Turtle()
	angle.shape(shape)
	angle.color(color)
	for x in xrange(3):
		angle.forward(length)
		angle.left(120)
	return angle

def draw_flower(length,shape,color,deg):
	f = turtle.Turtle()
	f.shape(shape)
	f.color(color)
	f.speed(10)

	for i in range(0, 360/deg):
		rotate = i * deg
		i += 1
		f.setheading(rotate)
		for x in xrange(1,3):
			f.forward(100)
			f.right(60)
			f.forward(100)
			f.right(120)

	f.setheading(270)
	f.forward(length)
	return f

def draw():
	window = turtle.Screen()
	window.bgcolor('red')
	# draw_square(100,'turtle','yellow')
	# draw_circle(50,'arrow','green')
	# draw_triangle(150, 'turtle', 'white')
	draw_flower(200,'turtle','yellow',10)
	window.exitonclick()
draw()