-- For Diplomatic Letter --

NDefines.NGame.MAX_SCRIPTED_LOC_RECURSION = 1001

-- Politics Defines --

NDefines.NPolitics.BASE_POLITICAL_POWER_INCREASE = 3.0

-- Diplomacy Defines --

NDefines.NDiplomacy.EMBARGO_THREAT_THRESHOLD = -1 -- Target-generated threat threshold to allow embargo (affected by modifiers)
NDefines.NDiplomacy.EMBARGO_COST = 50

-- Country Defines --

NDefines.NCountry.POLITICAL_POWER_UPPER_CAP = 2000.0
NDefines.NCountry.STARTING_COMMAND_POWER = 10.0
NDefines.NCountry.BASE_MAX_COMMAND_POWER = 200.0
NDefines.NCountry.ATTACHE_XP_SHARE = 0.25 -- 0.15


-- Focus Defines --

NDefines.NFocus.FOCUS_POINT_DAYS = 9.2
NDefines.NFocus.MAX_SAVED_FOCUS_PROGRESS = 20 -- was 15

-- Building Defines --

NDefines.NBuildings.MAX_SHARED_SLOTS = 50
NDefines.NBuildings.MAX_BUILDING_LEVELS = 40
NDefines.NBuildings.RADAR_RANGE_MAX = 400


-- Production Defines --

NDefines.NProduction.BASE_FACTORY_SPEED_MIL = 3.0 -- vanilla was 4.50
NDefines.NProduction.BASE_FACTORY_SPEED_NAV = 5.0 -- Multiplied x2 from vanilla --

NDefines.NProduction.CONVOY_MAX_NAV_FACTORIES_PER_LINE = 50
NDefines.NProduction.FLOATING_HARBOR_MAX_NAV_FACTORIES_PER_LINE = 20
NDefines.NProduction.DEFAULT_MAX_NAV_FACTORIES_PER_LINE = 50
NDefines.NProduction.CAPITAL_SHIP_MAX_NAV_FACTORIES_PER_LINE = 20

NDefines.NProduction.MAX_MIL_FACTORIES_PER_LINE = 300
NDefines.NProduction.RAILWAY_GUN_MAX_MIL_FACTORIES_PER_LINE = 10

NDefines.NProduction.MAX_CIV_FACTORIES_PER_LINE = 15

-- Navy Defines --

NDefines.NNavy.AMPHIBIOUS_INVADE_ATTACK_LOW = 0.4 	-- [was 0.2] low and high cap of attack modifier scale. Scale interpolated by invasion progress.
NDefines.NNavy.AMPHIBIOUS_INVADE_ATTACK_HIGH = 1.0
NDefines.NNavy.SHORE_BOMBARDMENT_CAP = 0.50 -- multipler of how much effects divisions stats against invasions, important: this is the cap so 50% is not broken like you think, i mean admirals and generals traits like shore bombardement bonuses 25%
NDefines.NNavy.ANTI_AIR_TARGETING = 0.8 -- how good ships are at hitting aircraft
NDefines.NNavy.CARRIER_STACK_PENALTY = 8 -- The most efficient is 8 (old was 4) carriers in combat. 8+ brings the penalty to the amount of wings in battle.
NDefines.NNavy.CARRIER_STACK_PENALTY_EFFECT = 0.50 -- Each carrier above the optimal amount decreases the amount of airplanes being able to takeoff by such %.
NDefines.NNavy.ADMIRAL_TASKFORCE_CAP = 20 
NDefines.NNavy.MIN_GUN_COOLDOWN = 0.1 -- minimum cooldown for a gun
NDefines.NNavy.BASE_GUN_COOLDOWNS = { -- number of hours for a gun to be ready after shooting
	2.0,	-- big guns, wth was this one same with small guns. it was 1 omg!!
	4.0,	-- torpedoes
	1.0,	-- small guns
}

-- From Summer Beta (its up to paradox so never forget these to remove if they remove too)

NDefines.NNavy.CONVOY_HIT_PROFILE = 85.0
NDefines.NNavy.GUN_HIT_PROFILES = { -- hit profiles for guns, if target ih profile is lower the gun will have lower accuracy
	80.0,	-- big guns
	150.0,	-- torpedoes
	45.0,	-- small guns
}
NDefines.NNavy.NAVY_PIERCING_THRESHOLD_DAMAGE_VALUES = {	
	-- 0 armor will always receive maximum damage (so add overmatching at your own peril). the system expects at least 2 values, with no upper limit.
	1.00,
	1.00,
	0.70,
	0.40,
	0.30,
	0.10,
}

NDefines.NNavy.COMBAT_ARMOR_PIERCING_DAMAGE_REDUCTION = 0
NDefines.NNavy.ANTI_AIR_POW_ON_INCOMING_AIR_DAMAGE = 0.225	-- received air damage is calculated using following: 1 - ( (ship_anti_air + fleet_anti_air * SHIP_TO_FLEET_ANTI_AIR_RATIO )^ANTI_AIR_POW_ON_INCOMING_AIR_DAMAGE ) * ANTI_AIR_MULT_ON_INCOMING_AIR_DAMAGE
NDefines.NNavy.ANTI_AIR_MULT_ON_INCOMING_AIR_DAMAGE	= 0.18


-- Air Defines --

NDefines.NAir.SUPPLY_NEED_FACTOR = 0.22 -- 0.28

NDefines.NAir.AIR_WING_XP_LEVELS = {20, 40, 60, 80, 100, 140, 180, 220, 260, 300, 390, 480, 570, 660, 750, 780, 810, 840, 870, 900}
NDefines.NAir.AIR_WING_XP_TRAINING_MAX = 300.0
NDefines.NAir.AIR_WING_XP_TRAINING_MISSION_GAIN_DAILY = 4.5
NDefines.NAir.AIR_WING_COUNTRY_XP_FROM_TRAINING_FACTOR = 0.01
NDefines.NAir.AIR_WING_XP_LOSS_WHEN_KILLED = 200
NDefines.NAir.AIR_WING_MAX_STATS_ATTACK = 1000 -- Max stats was 200
NDefines.NAir.AIR_WING_MAX_STATS_DEFENCE = 1000 -- was 200
NDefines.NAir.AIR_WING_MAX_STATS_AGILITY = 1000 -- was 200
NDefines.NAir.AIR_WING_MAX_STATS_SPEED = 9999 -- Used to balance the damage done while bombing. was 1500
NDefines.NAir.AIR_WING_XP_LOSS_REDUCTION_OVER_FRIENDLY_TERRITORY_FACTOR = 0.7
NDefines.NAir.MISSION_COMMAND_POWER_COSTS = { -- command power cost per plane to create a mission
	0.0, -- AIR_SUPERIORITY
	0.0, -- CAS
	0.0, -- INTERCEPTION
	0.0, -- STRATEGIC_BOMBER
	0.0, -- NAVAL_BOMBER
	0.0, -- DROP_NUKE
	0.0, -- PARADROP
	0.0, -- NAVAL_KAMIKAZE
	0.0, -- PORT_STRIKE
	0.0, -- ATTACK_LOGISTICS
	0.025, -- AIR_SUPPLY --Was 0.05
	0.0, -- TRAINING
	0.0, -- NAVAL_MINES_PLANTING
	0.0, -- NAVAL_MINES_SWEEPING
	0.0, -- MISSION_RECON
	0.0, -- NAVAL_PATROL
}

NDefines.NAir.AA_INDUSTRY_AIR_DAMAGE_FACTOR = -0.10				-- 5x levels = 50% defense from bombing. Reduced since Technology would otherwise give you above 100% damage reduction.

-- From Summer Beta (its up to paradox so never forget these to remove if they remove too)

NDefines.NAir.COMBAT_BETTER_AGILITY_DAMAGE_REDUCTION = 0.45
NDefines.NAir.COMBAT_BETTER_SPEED_DAMAGE_INCREASE = 0.65
NDefines.NAir.THRUST_WEIGHT_AGILITY_FACTOR = 0.5 -- was 3.0

-- Military Defines --

NDefines.NMilitary.BASE_DIVISION_BRIGADE_GROUP_COST = 0 			-- Base cost to unlock a regiment slot,
NDefines.NMilitary.BASE_DIVISION_BRIGADE_CHANGE_COST = 0			-- Base cost to change a regiment column.
NDefines.NMilitary.BASE_DIVISION_SUPPORT_SLOT_COST = 0 				-- Base cost to unlock a support slot.
NDefines.NMilitary.UNIT_LEADER_USE_NONLINEAR_XP_GAIN = false
NDefines.NMilitary.BASE_LEADER_TRAIT_GAIN_XP = 1
NDefines.NMilitary.UNIT_LEADER_INITIAL_TRAIT_SLOT = { 				-- trait slot for 0 level leader
	1.0, -- field marshal
	0.0, -- corps commander
	1.0, -- navy general
	0.0 -- operative
}

NDefines.NMilitary.UNIT_LEADER_TRAIT_SLOT_PER_LEVEL = { 			-- num extra traits on each level
	1.0, -- field marshal
	1.0, -- corps commander
	1.0, -- navy general
	0.0 -- operative
}

NDefines.NMilitary.PIERCING_THRESHOLDS = {	-- Our piercing / their armor must be this value to deal damage fraction equal to the index in the array below [higher number = higher penetration]. If armor is 0, 1.00 will be returned.
	1.00,
	0.75,
	0.50,
	0.00, --there isn't much point setting this higher than 0
}
NDefines.NMilitary.PIERCING_THRESHOLD_DAMAGE_VALUES = {	-- 0 armor will always receive maximum damage (so add overmatching at your own peril). the system expects at least 2 values, with no upper limit.
	1.00,
	0.80,
	0.65,
	0.50,
}


NDefines.NMilitary.MAX_DIVISION_SUPPORT_WIDTH = 2

NDefines.NMilitary.MAX_ARMY_EXPERIENCE = 1000
NDefines.NMilitary.MAX_NAVY_EXPERIENCE = 1000
NDefines.NMilitary.MAX_AIR_EXPERIENCE = 1000

NDefines.NMilitary.DEPLOY_TRAINING_MAX_LEVEL = 5
NDefines.NMilitary.UNIT_EXP_LEVELS = {0.02, 0.04, 0.06, 0.08, 0.1, 0.14, 0.18, 0.22, 0.26, 0.3, 0.39, 0.48, 0.57, 0.66, 0.75, 0.78, 0.81, 0.84, 0.87, 0.9}
NDefines.NMilitary.ARMY_EXP_BASE_LEVEL = 5
NDefines.NMilitary.TRAINING_MAX_LEVEL = 10
NDefines.NMilitary.EXPERIENCE_COMBAT_FACTOR = 0.03
NDefines.NMilitary.BASE_LEADER_TRAIT_GAIN_XP = 0.7
NDefines.NMilitary.UNIT_EXPERIENCE_PER_COMBAT_HOUR = 0.000175
NDefines.NMilitary.FIELD_EXPERIENCE_MAX_PER_DAY = 12
NDefines.NMilitary.ENCIRCLED_DISBAND_MANPOWER_FACTOR = 0.1
NDefines.NMilitary.PLAYER_ORDER_PLANNING_DECAY = 0.005
NDefines.NMilitary.DISBAND_MANPOWER_LOSS = 0.0
NDefines.NMilitary.PLAN_SPREAD_ATTACK_WEIGHT = 4.1 --AI should concentrate forces more a bit experimental. Increased from 4.0 to combat issues with AI death stacks - SpicyAlfredo
NDefines.NMilitary.FIELD_MARSHAL_XP_RATIO = 0.7
NDefines.NMilitary.COMMANDER_LEVEL_UP_STAT_WEIGHTS = {5, 5, 3, 4}
NDefines.NMilitary.NEW_COMMANDER_RANDOM_PERSONALITY_TRAIT_CHANCES = { -- Chances to gain a personality trait for new generals
	0.80, --50% for first trait
	0.40, --15% for second trait after that
	0.05, 
	0.01,
}

-- From Summer Beta (its up to paradox so never forget these to remove if they remove too)

NDefines.NMilitary.COMBAT_STACKING_START = 5				    -- at what nr of divisions stacking penalty starts
NDefines.NMilitary.COMBAT_STACKING_EXTRA = 3                   -- extra stacking from directions
NDefines.NMilitary.COMBAT_STACKING_PENALTY = -0.02             -- how much stackign penalty per division
NDefines.NMilitary.COMBAT_OVER_WIDTH_PENALTY = -1				-- over combat width penalty per %.