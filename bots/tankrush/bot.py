from .stubs import *
import random

def on_the_map(loc):
	x, y = loc
	if x < 0: return False
	if y < 0: return False
	if x >= get_board_width(): return False
	if y >= get_board_height(): return False
	return True

def add(left, right):
	return tuple([x + y for x, y in zip(left, right)])

def sub(left, right):
	return tuple([x - y for x, y in zip(left, right)])

def R2(left, right):
	squared = [x * x for x in sub(left, right)]
	return squared[0] + squared[1]

NINE_DIRECTIONS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, 0))
EIGHT_DIRECTIONS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))
FOUR_DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))

NORTH = (0, -1)
NORTHEAST = (1, -1)
EAST = (1, 0)
SOUTHEAST = (1, 1)
SOUTH = (0, 1)
SOUTHWEST = (-1, 1)
WEST = (-1, 0)
NORTHWEST = (-1, -1)
CENTER = (0, 0)

def rotate_right(dir):
	if dir == (0, -1): return (1, -1)
	if dir == (1, -1): return (1, 0)
	if dir == (1, 0): return (1, 1)
	if dir == (1, 1): return (0, 1)
	if dir == (0, 1): return (-1, 1)
	if dir == (-1, 1): return (-1, 0)
	if dir == (-1, 0): return (-1, -1)
	if dir == (-1, -1): return (0, -1)
	raise ValueError('Tried to compute rotate_right({:s})'.format(dir))

def rotate_left(dir):
	if dir == (1, -1): return (0, -1)
	if dir == (1, 0): return (1, -1)
	if dir == (1, 1): return (1, 0)
	if dir == (0, 1): return (1, 1)
	if dir == (-1, 1): return (0, 1)
	if dir == (-1, 0): return (-1, 1)
	if dir == (-1, -1): return (-1, 0)
	if dir == (0, -1): return (-1, -1)
	raise ValueError('Tried to compute rotate_left({:s})'.format(dir))

def opposite(dir):
	return tuple([-x for x in dir])

def deltas_in(r2):
	out = []
	i = 0
	while i * i < r2: i += 1
	for dy in range(-i - 1, i + 1):
		for dx in range(-i - 1, i + 1):
			if R2((dx, dy), (0, 0)) <= r2:
				out += [(dx, dy)]
	return tuple(out)

def try_build(robot_type, dir):
	dest = add(get_location(), dir)
	if not on_the_map(dest): return False
	
	sensed = sense_location(dest)
	if sensed.type != RobotType.NONE: return False
	
	create(robot_type, dest)
	return True

def try_build_facing(robot_type, dir):
	dl = dir
	dr = dir
	for _ in range(4):
		if try_build(robot_type, dl): return dl
		dl = rotate_left(dl)
		dr = rotate_right(dr)
		if try_build(robot_type, dr): return dr
	return None

def try_move(loc):
	if not on_the_map(loc): return False
	if not can_sense_location(loc): return False
	sensed = sense_location(loc)
	if sensed.type != RobotType.NONE: return False
	move(loc)
	return True

class Robot:
	def __init__(self):
		self.since_spawn = 0
		self.hq_loc = None
		self.enemy_hq_loc = None

	def run(self):
		self.since_spawn += 1
		
		for robot in sense():
			if robot.team is get_team():
				if robot.type is RobotType.HQ:
					self.hq_loc = robot.location
					self.enemy_hq_loc = sub((get_board_width() - 1, get_board_height() - 1), self.hq_loc)
			else:
				pass

class HQ(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()
		
		exists_friendly_builder = False
		for robot in sense():
			if robot.team is get_team():
				if robot.type is RobotType.BUILDER:
					exists_friendly_builder = True
					break

		if not exists_friendly_builder:
			if GameConstants.BUILDER_COST <= get_oil():
				loc = try_build_facing(RobotType.BUILDER, NORTH)
				if loc:
					return

class Builder(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()

		exists_friendly_rax = False
		for robot in sense():
			if robot.team is get_team():
				if robot.type is RobotType.BARRACKS:
					exists_friendly_rax = True
					break

		if not exists_friendly_rax:
			for dir in EIGHT_DIRECTIONS:
				if try_build(RobotType.BARRACKS, dir):
					return

class Refinery(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()

class Barracks(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()
		n = 0
		for dir in EIGHT_DIRECTIONS:
			if GameConstants.TANK_COST + 20 <= get_oil():
				if try_build(RobotType.TANK, dir):
					n += 1
					if n >= 3:
						return

class Tank(Robot):
	def __init__(self):
		super().__init__()
		self.speed = GameConstants.TANK_SPEED
		self.attack_range = GameConstants.TANK_ATTACK_RANGE
		self.attack_cost = GameConstants.TANK_ATTACK_COST

	def run(self):
		super().run()
		
		for robot in sense():
			if robot.team is get_team():
				pass
			else:
				if R2(get_location(), robot.location) <= GameConstants.TANK_ATTACK_RANGE:
					if GameConstants.TANK_ATTACK_COST <= get_oil():
						attack(robot.location)
						return
		
		if self.enemy_hq_loc is not None:
			locs = EIGHT_DIRECTIONS
			locs = [add(get_location(), dir) for dir in locs]
			locs = sorted(locs, key = lambda x: R2(self.enemy_hq_loc, x))
			for loc in locs:
				if try_move(loc):
					return


class Gunner(Robot):
	def __init__(self):
		super().__init__()
		self.speed = GameConstants.GUNNER_SPEED
		self.attack_range = GameConstants.GUNNER_ATTACK_RANGE
		self.attack_cost = GameConstants.GUNNER_ATTACK_COST

	def run(self):
		super().run()

type_to_obj = {
	RobotType.HQ: HQ,
	RobotType.BUILDER: Builder,
	RobotType.REFINERY: Refinery,
	RobotType.BARRACKS: Barracks,
	RobotType.TANK: Tank,
	RobotType.GUNNER: Gunner
}

obj = type_to_obj[get_type()]
robot = obj()

def turn():
	robot.run()

