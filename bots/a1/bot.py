from .stubs import *
import random

def sum(x):
	out = 0
	for y in list(x):
		out += y
	return out

def print(x):
	dlog(x)

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
	return sum([x * x for x in sub(left, right)])

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
	raise ValueError('rotate_right({:s})'.format(dir))

def rotate_left(dir):
	if dir == (1, -1): return (0, -1)
	if dir == (1, 0): return (1, -1)
	if dir == (1, 1): return (1, 0)
	if dir == (0, 1): return (1, 1)
	if dir == (-1, 1): return (0, 1)
	if dir == (-1, 0): return (-1, 1)
	if dir == (-1, -1): return (-1, 0)
	if dir == (0, -1): return (-1, -1)
	raise ValueError('rotate_left({:s})'.format(dir))

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



def vector_to_int(maxes, vec):
	assert len(maxes) == len(vec)
	
	encoded = 0
	for a, b in zip(maxes, vec):
		assert b <= a
		encoded *= a + 1
		encoded += b
	return encoded

def int_to_vector(maxes, encoded):
	out = []
	for a in maxes[::-1]:
		out = [encoded % (a + 1)] + out
		encoded //= (a + 1)
	assert encoded == 0
	return tuple(out)

def type_as_int(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.BUILDER: return 0
	if robot_type is RobotType.TANK: return 1
	if robot_type is RobotType.GUNNER: return 2
	if robot_type is RobotType.GRENADER: return 3
	if robot_type is RobotType.HQ: return 4
	if robot_type is RobotType.REFINERY: return 5
	if robot_type is RobotType.BARRACKS: return 6
	if robot_type is RobotType.TURRET: return 7
	if robot_type is RobotType.WALL: return 8
	raise ValueError('type_as_int({!s:s})'.format(robot_type))

def int_as_type(x):
	if x == 0: return RobotType.BUILDER
	if x == 1: return RobotType.TANK
	if x == 2: return RobotType.GUNNER
	if x == 3: return RobotType.GRENADER
	if x == 4: return RobotType.HQ
	if x == 5: return RobotType.REFINERY
	if x == 6: return RobotType.BARRACKS
	if x == 7: return RobotType.TURRET
	if x == 8: return RobotType.WALL
	raise ValueError('int_as_type({:d})'.format(x))



def is_ref_spot(hq_loc, loc):
	return ((hq_loc[0] - loc[0]) % 3 == 0) is ((hq_loc[1] - loc[1]) % 3 == 0)



def get_speed(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.BUILDER: return GameConstants.BUILDER_SPEED
	if robot_type is RobotType.TANK: return GameConstants.TANK_SPEED
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_SPEED
	if robot_type is RobotType.GRENADER: return GameConstants.GRENADER_SPEED
	raise ValueError('get_speed({!s:s})'.format(robot_type))

def get_build_radius(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.BUILDER: return GameConstants.BUILDER_SPAWN_RADIUS
	if robot_type is RobotType.HQ: return GameConstants.HQ_SPAWN_RADIUS
	if robot_type is RobotType.BARRACKS: return GameConstants.BARRACKS_SPAWN_RADIUS
	raise ValueError('get_build_radius({!s:s})'.format(robot_type))

def get_max_spawns(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.BUILDER: return GameConstants.BUILDER_MAX_SPAWNS
	if robot_type is RobotType.HQ: return GameConstants.HQ_MAX_SPAWNS
	if robot_type is RobotType.BARRACKS: return GameConstants.BARRACKS_MAX_SPAWNS
	raise ValueError('get_max_spawns({!s:s})'.format(robot_type))

def get_cost(robot_type):
	if robot_type is RobotType.BUILDER: return GameConstants.BUILDER_COST
	if robot_type is RobotType.TANK: return GameConstants.TANK_COST
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_COST
	if robot_type is RobotType.GRENADER: return GameConstants.GRENADER_COST
	if robot_type is RobotType.REFINERY: return GameConstants.REFINERY_COST
	if robot_type is RobotType.BARRACKS: return GameConstants.BARRACKS_COST
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_COST
	if robot_type is RobotType.WALL: return GameConstants.WALL_COST
	raise ValueError('get_cost({!s:s})'.format(robot_type))

def get_max_health(robot_type):
	if robot_type is RobotType.BUILDER: return GameConstants.BUILDER_HEALTH
	if robot_type is RobotType.TANK: return GameConstants.TANK_HEALTH
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_HEALTH
	if robot_type is RobotType.GRENADER: return GameConstants.GRENADER_HEALTH
	if robot_type is RobotType.HQ: return GameConstants.HQ_HEALTH
	if robot_type is RobotType.REFINERY: return GameConstants.REFINERY_HEALTH
	if robot_type is RobotType.BARRACKS: return GameConstants.BARRACKS_HEALTH
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_HEALTH
	if robot_type is RobotType.WALL: return GameConstants.WALL_HEALTH
	raise ValueError('get_max_health({!s:s})'.format(robot_type))

def get_damage(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.TANK: return GameConstants.TANK_DAMAGE
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_DAMAGE
	if robot_type is RobotType.GRENADER: return GameConstants.GRENADER_DAMAGE_DAMAGE
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_DAMAGE
	raise ValueError('get_damage({!s:s})'.format(robot_type))

def get_attack_range(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.TANK: return GameConstants.TANK_ATTACK_RANGE
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_ATTACK_RANGE
	if robot_type is RobotType.GRENADER:
		assert GameConstants.GRENADER_STUN_RANGE == GameConstants.GRENADER_DAMAGE_RANGE
		return GameConstants.GRENADER_DAMAGE_RANGE
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_ATTACK_RANGE
	raise ValueError('get_damage({!s:s})'.format(robot_type))

def get_attack_cost(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.TANK: return GameConstants.TANK_ATTACK_COST
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_ATTACK_COST
	if robot_type is RobotType.GRENADER: return GameConstants.GRENADER_DAMAGE_COST
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_ATTACK_COST
	raise ValueError('get_damage({!s:s})'.format(robot_type))

def get_attack_aoe(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.TANK: return GameConstants.TANK_ATTACK_AOE
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_ATTACK_AOE
	if robot_type is RobotType.GRENADER:
		assert GameConstants.GRENADER_STUN_AOE == GameConstants.GRENADER_DAMAGE_AOE
		return GameConstants.GRENADER_DAMAGE_AOE
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_ATTACK_AOE
	raise ValueError('get_damage({!s:s})'.format(robot_type))

def get_sensor_radius(robot_type = None):
	if robot_type is None: robot_type = get_type()
	if robot_type is RobotType.BUILDER: return GameConstants.BUILDER_SENSE_RANGE
	if robot_type is RobotType.TANK: return GameConstants.TANK_SENSE_RANGE
	if robot_type is RobotType.GUNNER: return GameConstants.GUNNER_SENSE_RANGE
	if robot_type is RobotType.GRENADER: return GameConstants.GRENADER_SENSE_RANGE
	if robot_type is RobotType.REFINERY: return GameConstants.REFINERY_SENSE_RANGE
	if robot_type is RobotType.BARRACKS: return GameConstants.BARRACKS_SENSE_RANGE
	if robot_type is RobotType.TURRET: return GameConstants.TURRET_SENSE_RANGE
	if robot_type is RobotType.WALL: return GameConstants.WALL_SENSE_RANGE
	raise ValueError('get_sensor_radius({!s:s})'.format(robot_type))



def try_build(robot_type, dir):
	# Don't build off map
	dest = add(get_location(), dir)
	if not on_the_map(dest): return False
	
	# Don't build if not enough money
	if get_oil() < get_cost(robot_type): return False
	
	# Don't build where occupied
	sensed = sense_location(dest)
	if sensed.type != RobotType.NONE: return False
	
	# Build
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

def try_build_anywhere(robot_type):
	for dir in NINE_DIRECTIONS:
		if try_build(robot_type, dir):
			return dir
	return None

def try_move(loc):
	if not on_the_map(loc): return False
	if not can_sense_location(loc): return False
	if R2(get_location(), loc) > get_speed(): return False
	sensed = sense_location(loc)
	if sensed.type != RobotType.NONE: return False
	move(loc)
	return True

def try_move_towards(dest):
	locs = [add(get_location(), delta) for delta in deltas_in(get_speed())]
	locs = sorted(locs, key = lambda x: R2(x, dest))
	for loc in locs:
		if try_move(loc):
			return loc
	return None

def try_move_away(dest):
	locs = [add(get_location(), delta) for delta in deltas_in(get_speed())]
	locs = sorted(locs, key = lambda x: R2(x, dest), reverse = True)
	for loc in locs:
		if try_move(loc):
			return loc
	return None

def try_move_randomly():
	locs = [add(get_location(), delta) for delta in deltas_in(get_speed())]
	random.shuffle(locs)
	for loc in locs:
		if try_move(loc):
			return loc
	return None

def try_attack(loc):
	if not on_the_map(loc): return False
	if R2(get_location(), loc) > get_attack_range(): return False
	if get_oil() < get_attack_cost(): return False

	attack(loc)
	return True



def radio_encode(non_friendly = None):
	value_maxes = (7, 39, 39, 199, 1, 9, 39, 39, 1)
	payload = [0] * 10

	payload[0] = type_as_int()
	payload[1] = get_location()[0]
	payload[2] = get_location()[1]
	payload[3] = get_health() - 1
	payload[4] = 1 if is_stunned() else 0
	if non_friendly is None:
		payload[5] = 0
		payload[6] = 0
		payload[7] = 0
	else:
		payload[5] = type_as_int(non_friendly.type) + 1
		payload[6] = non_friendly.location[0]
		payload[7] = non_friendly.location[1]
	payload[8] = 1 if get_team() is TeamColor.RED else 0

	s = random.getstate()
	random.seed(vector_to_int(value_maxes, payload[:9]))
	random.setstate(s)
	tag = random.randint(0, 255)
	payload[9] = tag

	add_to_blockchain(payload)

def radio_decode(payload):
	if len(payload) != 10:
		return None
	
	if payload[8] != (1 if get_team() is TeamColor.RED else 0):
		return None
	
	for x in payload[10:]:
		if x != 0:
			return None

	f_type = int_as_type(payload[0])
	if f_type is not RobotType.HQ and payload[5] == 0:
		return

	value_maxes = (7, 39, 39, 199, 1, 9, 39, 39, 1)
	s = random.getstate()
	random.seed(vector_to_int(value_maxes, payload[:9]))
	random.setstate(s)
	tag_c = random.randint(0, 255)
	tag_r = payload[9]
	if tag_r != tag_c:
		return None
	f_loc = (payload[1], payload[2])
	f_hp = payload[3] + 1
	f_stunned = True if payload[4] == 1 else False
	if payload[5] == 0:
		return ((f_type, f_loc, f_hp, f_stunned), None)
	else:
		e_type = int_as_type(payload[5] - 1)
		e_loc = (payload[6], payload[7])
		return ((f_type, f_loc, f_hp, f_stunned), (e_type, e_loc))



class Robot:
	def __init__(self):
		self.since_spawn = 0
		self.visible_robots = None
		self.visible_enemies = None
		self.hq_loc = None
		self.enemy_hq_loc = None
		self.visible_friendly_builders = None
		self.visible_friendly_barracks = None
		self.visible_friendly_gunners = None
		self.visible_walls = None
		self.radioed = None
		self.radioed_enemies = None

	def run(self):
		self.since_spawn += 1
		
		self.visible_robots = sense()
		self.visible_walls = [x for x in self.visible_robots if x.type is RobotType.WALL]
		robots = [x for x in self.visible_robots if x.type is not RobotType.WALL]
		self.visible_friends = [x for x in robots if x.team is get_team()]
		self.visible_enemies = [x for x in robots if x.team is not get_team()]
		self.visible_friendly_builders = [x for x in self.visible_friends if x.type is RobotType.BUILDER]
		self.visible_friendly_barracks = [x for x in self.visible_friends if x.type is RobotType.BARRACKS]
		self.visible_friendly_gunners = [x for x in self.visible_friends if x.type is RobotType.GUNNER]
		
		self.radioed = [[None for _ in range(40)] for _ in range(40)]
		self.radioed_enemies = []
		if get_round_num() - 1 >= 0:
			msgs = get_blockchain(get_round_num() - 1)
			for msg in msgs:
				r = radio_decode(msg)
				if r is not None:
					f, e = r
					f_type, f_loc, f_hp, f_stunned = f
					self.radioed[f_loc[0]][f_loc[1]] = (False, f_type)
					if e is not None:
						e_type, e_loc = e
						self.radioed[e_loc[0]][e_loc[1]] = (True, e_type)
						self.radioed_enemies += [(e_type, e_loc)]
					
					if self.hq_loc is None:
						if f_type is RobotType.HQ:
							self.hq_loc = f_loc

		if self.hq_loc is None:
			visible_friendly_hqs = [x for x in self.visible_friends if x.type is RobotType.HQ]
			if visible_friendly_hqs:
				self.hq_loc = visible_friendly_hqs[0].location

		if self.enemy_hq_loc is None:
			visible_enemy_hqs = [x for x in self.visible_enemies if x.type is RobotType.HQ]
			if visible_enemy_hqs:
				self.enemy_hq_loc = visible_enemy_hqs[0].location

		if self.enemy_hq_loc is None:
			if self.hq_loc is not None:
				self.enemy_hq_loc = sub((get_board_width() - 1, get_board_height() - 1), self.hq_loc)

		if self.hq_loc is None:
			if self.enemy_hq_loc is not None:
				self.hq_loc = sub((get_board_width() - 1, get_board_height() - 1), self.enemy_hq_loc)
		
		if self.enemy_hq_loc is not None:
			self.radioed_enemies += [(RobotType.HQ, self.enemy_hq_loc)]

	def finish_turn(self):
		# Write to blockchain
		non_friendlies = [x for x in self.visible_robots if x.team is not get_team()]
		non_friendly = random.choice(non_friendlies) if non_friendlies else None
		radio_encode(non_friendly)

class HQ(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()
				
		if is_stunned(): return
		
		if True not in [R2(get_location(), x[1]) <= 100 for x in self.radioed_enemies] and not self.visible_enemies:
			if get_oil() >= get_cost(RobotType.BUILDER) + get_cost(RobotType.REFINERY) * len(self.visible_friendly_builders):
				loc = try_build_anywhere(RobotType.BUILDER)
				if loc:
					return

		if get_oil() > 150:
			loc = try_build_anywhere(RobotType.BUILDER)
			if loc:
				return
		
		if not self.visible_friendly_builders:
			loc = try_build_anywhere(RobotType.BUILDER)
			if loc:
				return
		
		if self.visible_enemies:
			loc = try_build_anywhere(RobotType.BUILDER)
			if loc:
				return

class Builder(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()
		
		if is_stunned(): return

		# Drop a barracks if enemy is nearby
		if self.visible_enemies and not self.visible_friendly_barracks:
			for dir in EIGHT_DIRECTIONS:
				dest = add(get_location(), dir)
				if not is_ref_spot(self.hq_loc, dest): continue
				if try_build(RobotType.BARRACKS, dir):
					return

		# Build refineries if no enemies seen
		if get_oil() < 600:
			if True not in [R2(get_location(), x[1]) <= 100 for x in self.radioed_enemies] and not self.visible_enemies:
				for dir in EIGHT_DIRECTIONS:
					dest = add(get_location(), dir)
					if not is_ref_spot(self.hq_loc, dest): continue
					if try_build(RobotType.REFINERY, dir):
						return

		# Try to build in lattice
		if get_oil() > 100:
			weight_refinery = 100
			weight_turret = 0 if get_oil() < 150 else 100
			weight_barracks = 60

			if not self.visible_enemies and self.visible_friendly_barracks:
				weight_barracks = 0

			if get_oil() > 250:
				weight_refinery *= 0.4

			if self.visible_enemies:
				weight_refinery = 0
				weight_turret = 80
				weight_barracks = 20
			
			if not self.visible_enemies:
				weight_turret = 0

			choices = (RobotType.REFINERY, RobotType.TURRET, RobotType.BARRACKS)
			weights = (weight_refinery, weight_turret, weight_barracks)
			if sum(weights) > 0:
				robot_type = random.choices(choices, weights = weights)[0]
				for dir in EIGHT_DIRECTIONS:
					dest = add(get_location(), dir)
					if not is_ref_spot(self.hq_loc, dest): continue
					if try_build(robot_type, dir):
						return

		# Move randomly
		if get_round_num() > 800:
			if try_move_randomly(): return

		# Move randomly
		if try_move_randomly(): return

class Refinery(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()

class Barracks(Robot):
	def __init__(self):
		super().__init__()
		self.built_units = 0

	def run(self):
		super().run()
		
		if is_stunned(): return

		# Build tanks when there is surplus of oil
		if not self.visible_enemies:
			while get_oil() > 500:
				if not try_build_anywhere(RobotType.TANK): break
				self.built_units += 1
				if self.built_units >= 3: return

		# Build gunners according to economy
		if get_oil() > 100 and random.random() < 0.2:
			if try_build_anywhere(RobotType.GUNNER):
				self.built_units += 1
				if self.built_units >= 3: return

		# Build gunners when getting rushed
		while len(self.visible_enemies) >= (len(self.visible_friendly_gunners) + self.built_units):
			if not try_build_anywhere(RobotType.GUNNER): break
			self.built_units += 1
			if self.built_units >= 3: return

class Tank(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()

		if is_stunned():
			return

		# Hit enemy hq
		if self.enemy_hq_loc is not None:
			if try_attack(self.enemy_hq_loc):
				return

		# Hit enemy
		for enemy in self.visible_enemies:
			if try_attack(enemy.location):
				return
		
		# Hit wall if excess oil
		if get_oil() > 300:
			for wall in self.visible_walls:
				if try_attack(wall.location):
					return

		# Move to nearest enemy
		for enemy in sorted([x[1] for x in self.radioed_enemies] + [x.location for x in self.visible_enemies], key = lambda x: R2(get_location(), x)):
			loc = try_move_towards(enemy)
			if loc:
				return

		# Move randomly
		if try_move_randomly():
			return

class Gunner(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()

		if is_stunned():
			return

		# Hit enemy hq
		if self.enemy_hq_loc is not None:
			if try_attack(self.enemy_hq_loc):
				return

		# Hit enemy
		for enemy in self.visible_enemies:
			if try_attack(enemy.location):
				return
		
		# Hit wall if excess oil
		if get_oil() > 300:
			for wall in self.visible_walls:
				if try_attack(wall.location):
					return

		# Move to nearest enemy
		for enemy in sorted([x[1] for x in self.radioed_enemies] + [x.location for x in self.visible_enemies], key = lambda x: R2(get_location(), x)):
			loc = try_move_towards(enemy)
			if loc:
				return

		# Move randomly
		if try_move_randomly():
			return

class Grenader(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()
		
		if is_stunned(): return
		
		if self.enemy_hq_loc is not None:
			if try_attack(self.enemy_hq_loc):
				return
		
		if get_oil() > 300:
			for wall in self.visible_walls:
				if try_attack(wall.location):
					return

		if try_move_randomly(): return

class Turret(Robot):
	def __init__(self):
		super().__init__()

	def run(self):
		super().run()
		
		if is_stunned(): return

		if self.enemy_hq_loc is not None:
			if try_attack(self.enemy_hq_loc):
				return

		for enemy in self.visible_enemies:
			if try_attack(enemy.location):
				return
		
		if get_oil() > 300:
			for wall in self.visible_walls:
				if try_attack(wall.location):
					return



type_to_obj = {
	RobotType.BUILDER: Builder,
	RobotType.TANK: Tank,
	RobotType.GUNNER: Gunner,
	RobotType.GRENADER: Grenader,
	RobotType.HQ: HQ,
	RobotType.REFINERY: Refinery,
	RobotType.BARRACKS: Barracks,
	RobotType.TURRET: Turret
}



obj = type_to_obj[get_type()]
robot = obj()

def turn():
	robot.run()
	robot.finish_turn()