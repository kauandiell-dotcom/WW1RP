-- AI Trade / Diplo --

NDefines.NTrade.DISTANCE_TRADE_FACTOR = -0.0001			-- Trade factor is modified by distance times this vanilla -.02
NDefines.NAI.TRADEABLE_FACTORIES_FRACTION = 0.6	-- Will at most trade away this fraction of factories.
NDefines.NDiplomacy.NOT_READY_FOR_WAR_BASE = -100 -- AI should be unwilling to enter accept a call to war if not ready ---for war against the relevant enemies. vanilla -50 - suggested define by SensitiveDannyBoi
NDefines.NAI.LENDLEASE_FRACTION_OF_PRODUCTION = 0.1		-- Base fraction AI would send as lendlease 0.5 vanilla less base production used, perhaps will promote AI to send more?

-- AI Fuel Management --

NDefines.NAI.WANTED_MAX_FUEL_BUFFER_IN_DAYS_FOR_ARMY_MAX_CONSUMPTION = 365  -- AI will try to buffer at least this amount of days on max consumption, will trade if necesarry and will go into fuel saving mode/aggresive mode using this buffer 
NDefines.NAI.WANTED_MAX_FUEL_BUFFER_IN_DAYS_FOR_AIR_MAX_CONSUMPTION  = 365  -- AI will try to buffer at least this amount of days on max consumption, will trade if necesarry and will go into fuel saving mode/aggresive mode using this buffer
NDefines.NAI.WANTED_MAX_FUEL_BUFFER_IN_DAYS_FOR_NAVY_MAX_CONSUMPTION = 365  -- AI will try to buffer at least this amount of days on max consumption, will trade if necesarry and will go into fuel saving mode/aggresive mode using this buffer

-- AI Invasion --

NDefines.NAI.ENEMY_NAVY_STRENGTH_DONT_BOTHER = 3							-- If the enemy has a navy at least these many times stronger that the own, don't bother invading
NDefines.NAI.RELATIVE_STRENGTH_TO_INVADE = 0 --0.08			-- Compares the estimated strength of the country/faction compared to it's enemies to see if it should invade or stay at home to defend.
NDefines.NAI.RELATIVE_STRENGTH_TO_INVADE_DEFENSIVE = 0 --0.4	-- Compares the estimated strength of the country/faction compared to it's enemies to see if it should invade or stay at home to defend, but while being a defensive country.

NDefines.NAI.INVASION_DISTANCE_RANDOMNESS = 600	---more long naval invasions test delete if problematic								-- This higher the value the more unpredictable the invasions. Compares to actual map distance in pixels.
NDefines.NAI.INVASION_COASTAL_PROVS_PER_ORDER = 12 --24								-- AI will consider one extra invasion per number of provinces stated here (num orders = total coast / this)

NDefines.NAI.MAX_INVASION_SIZE = 18 --24									-- max invasion group size

-- AI Frontlines and Land Army Management --

NDefines.NAI.LAND_COMBAT_OUR_COMBATS_AIR_IMPORTANCE = 1000		-- Strategic importance of our armies in the combats

NDefines.NMilitary.PLAN_EXECUTE_BALANCED_LIMIT = -1.0			-- When looking for an attach target, this score limit ---is required in the battle plan to consider province for attack suggested define by SensitiveDannyBoi
NDefines.NMilitary.PLAN_PORVINCE_PORT_BASE_IMPORTANCE = 18.0		-- Added importance for area defense province with a port
NDefines.NMilitary.PLAN_PORVINCE_PORT_LEVEL_FACTOR = 0.5			-- Bonus factor for port level
NDefines.NAI.MAIN_ENEMY_FRONT_IMPORTANCE = 15.0			-- How much extra focus the AI should put on who it considers to be its current main enemy.
NDefines.NAI.AREA_DEFENSE_BASE_IMPORTANCE = 5.0					-- Area defense order base importance value (used for determining order of troop selections) default 1
NDefines.NAI.AREA_DEFENSE_CIVIL_WAR_IMPORTANCE = 5.0				-- Area defense order importance value when a country is in a civil war as target or revolter. vanilla 10000 lolwut?? am I missing something here :
NDefines.NMilitary.PLAN_PORVINCE_RESISTANCE_BASE_IMPORTANCE = 150.0 -- Used when calculating the calue of defense area provinces for the battle plan system (factored by resistance level) vanilla 10.0
NDefines.NMilitary.PLAN_PROVINCE_LOW_VP_IMPORTANCE_FRONT = 1.0    -- Used when calculating the calue of fronts in the battle plan system vanilla 2.0

NDefines.NAI.MICRO_POCKET_SIZE = 1
NDefines.NAI.COMBINED_ARMS_LEVEL = 1
NDefines.NAI.MAX_SUPPLY_DIVISOR = 1.75
NDefines.NAI.PLAN_FACTION_WEAK_TO_ABORT = 0.50
NDefines.NAI.PLAN_FACTION_NORMAL_TO_EXECUTE = 0.50

NDefines.NAI.RESERVE_TO_COMMITTED_BALANCE = 0.3
NDefines.NAI.AVERAGE_SUPPLY_USE_PESSIMISM = 2.5
NDefines.NAI.FRONT_EVAL_UNIT_SUPPLY_AND_ORG_LACK_IMPACT = 2.0

NDefines.NAI.MINIMUM_EQUIPMENT_TO_ASK_LEND_LEASE = 1500
NDefines.NAI.MINIMUM_CONVOY_TO_ASK_LEND_LEASE = 500
NDefines.NAI.MINIMUM_FUEL_DAYS_TO_ASK_LEND_LEASE = 10
NDefines.NAI.MINIMUM_FUEL_DAYS_TO_ACCEPT_LEND_LEASE = 5

NDefines.NAI.DIPLOMACY_SEND_MAX_FACTION = 0.75
NDefines.NAI.GENERATE_WARGOAL_THREAT_BASELINE = 0.6

NDefines.NAI.LENDLEASE_FRACTION_OF_PRODUCTION = 0.25 --0.5
NDefines.NAI.LENDLEASE_FRACTION_OF_STOCKPILE = 0.125 --0.25

NDefines.NAI.NEW_LEADER_EXTRA_PP_FACTOR = 1 --2.0								 -- Country must have at least this many times extra PP to get new admirals or army leaders
NDefines.NAI.DIPLOMACY_IMPROVE_RELATION_COST_FACTOR = 7.0                       -- Desire to boost relations subtracts the cost multiplied by this
NDefines.NAI.COMMAND_POWER_BEFORE_SPEND_ON_TRAITS = 65.0

NDefines.NAI.MIN_AI_UNITS_PER_TILE_FOR_STANDARD_COHESION = 2.0	-- How many units should we have for each tile along a front in order to switch to standard cohesion (less moving around)
NDefines.NAI.MIN_FRONT_SIZE_TO_CONSIDER_STANDARD_COHESION = 2000	-- How long should fronts be before we consider switching to standard cohesion (under this, standard cohesion fronts will switch back to relaxed)

NDefines.NAI.ASSIGN_TANKS_TO_WAR_FRONT = 8.0 --4.0
NDefines.NAI.ASSIGN_TANKS_TO_NON_WAR_FRONT = 0.2 --0.4

NDefines.NMilitary.PLAN_EXECUTE_RUSH = -10									-- When looking for an attach target, this score limit is required in the battle plan to consider province for attack

NDefines.NAI.FALLBACK_LOSING_FACTOR = 0.0 					                    -- The lower this number  the longer the AI will hold the line before sending them to the fallback line

NDefines.NAI.HOUR_BAD_COMBAT_REEVALUATE = 24                                 	-- if we are in combat for this amount and it goes shitty then try skipping it

NDefines.NAI.PLAN_ATTACK_MIN_ORG_FACTOR_LOW = 0.85							-- Minimum org % for a unit to actively attack an enemy unit when executing a plan
NDefines.NAI.PLAN_ATTACK_MIN_STRENGTH_FACTOR_LOW = 0.85						-- Minimum strength for a unit to actively attack an enemy unit when executing a plan

NDefines.NAI.PLAN_ATTACK_MIN_ORG_FACTOR_MED = 0.65							-- (LOW,MED,HIGH) corresponds to the plan execution agressiveness level.
NDefines.NAI.PLAN_ATTACK_MIN_STRENGTH_FACTOR_MED = 0.65	

NDefines.NAI.PLAN_ATTACK_MIN_ORG_FACTOR_HIGH = 0.5		
NDefines.NAI.PLAN_ATTACK_MIN_STRENGTH_FACTOR_HIGH = 0.5	

NDefines.NAI.PLAN_FACTION_STRONG_TO_EXECUTE = 0.65 --0.80	0.60		        -- % or more of units in an order to consider ececuting the plan
NDefines.NAI.ORG_UNIT_STRONG = 0.75												-- Organization % for unit to be considered strong
NDefines.NAI.STR_UNIT_STRONG = 0.75												-- Strength (equipment) % for unit to be considered strong

NDefines.NAI.PLAN_FACTION_NORMAL_TO_EXECUTE = 0.65
NDefines.NAI.ORG_UNIT_NORMAL = 0.6 --6												-- Organization % for unit to be considered normal
NDefines.NAI.STR_UNIT_NORMAL = 0.6 --6												-- Strength (equipment) % for unit to be considered normal

NDefines.NAI.PLAN_FACTION_WEAK_TO_ABORT = 0.5 --0.50		0.65		        -- % or more of units in an order to consider ececuting the plan
NDefines.NAI.ORG_UNIT_WEAK = 0.35 --0.45												-- Organization % for unit to be considered weak
NDefines.NAI.STR_UNIT_WEAK = 0.4 --0.45												-- Strength (equipment) % for unit to be considered weak

NDefines.NAI.PLAN_AVG_PREPARATION_TO_EXECUTE = 0.5				            -- % or more average plan preparation before executing
NDefines.NAI.AI_FRONT_MOVEMENT_FACTOR_FOR_READY = 0.5			                -- If less than this fraction of units on a front is moving  AI sees it as ready for action


NDefines.NAI.PLAN_ACTIVATION_MAJOR_WEIGHT_FACTOR = 1		                    -- AI countries will hold on activating plans if stronger countries have plans in the same location. Majors count extra (value of 1 will negate this)
NDefines.NAI.PLAN_ACTIVATION_PLAYER_WEIGHT_FACTOR = 1 		                -- AI countries will hold on activating plans if player controlled countries have plans in the same location. Majors count extra (value of 1 will negate this)

NDefines.NAI.PLAN_MIN_SIZE_FOR_FALLBACK = 5000					                -- A country with less provinces than this will not draw fallback plans  but rather station their troops along the front

NDefines.NAI.GARRISON_FRACTION = 0.2					-- How large part of a front should always be holding the line rather than advancing at the enemy
NDefines.NAI.DIPLOMACY_REJECTED_WAIT_MONTHS_BASE = 1	-- AI will not repeat offers until at least this time has passed, and at most the double
NDefines.NAI.MIN_INVASION_PLAN_VALUE_TO_EXECUTE	 = 0.20	-- AI will typically avoid carrying out a plan it below this value (0.0 is considered balanced).
NDefines.NAI.ENTRENCHMENT_WEIGHT = 4.0					-- AI should favour units with less entrenchment when assigning units around.
NDefines.NAI.UNIT_ASSIGNMENT_TERRAIN_IMPORTANCE = 50.0	--- diminshed by 4x because of Greece-- Terrain score for units are multiplied by this when the AI is deciding which front they should be assigned to

NDefines.NAI.SEND_VOLUNTEER_EVAL_BASE_DISTANCE = 175.0  -- How far away it will evaluate sending volunteers if not a major power
NDefines.NAI.SEND_VOLUNTEER_EVAL_MAJOER_POWER = 1.0 	-- How willing major powers are to send volunteers.
NDefines.NAI.SEND_VOLUNTEER_EVAL_CONTAINMENT_FACTOR = 0.9 -- How much AI containment factors into its evaluation of sending volunteers.

NDefines.NAI.PLAN_ACTIVATION_SUPERIORITY_AGGRO = 10 --default 1.0		-- How aggressive a country is in activating a plan based on how superiour their force is.

--planning
NDefines.NAI.AI_FRONT_MOVEMENT_FACTOR_FOR_READY = 0.15 --default ??
NDefines.NAI.PLAN_VALUE_TO_EXECUTE = 0.15 --default ??

NDefines.NAI.MIN_PLAN_VALUE_TO_MICRO_INACTIVE = 0.2 --default 0.2				-- The AI will not consider members of groups which plan is not activated AND evaluates lower than this.
	
NDefines.NAI.MAX_UNITS_FACTOR_AREA_ORDER = 2.0 --default 1.0					-- Factor for max number of units to assign to area defense orders
NDefines.NAI.DESIRED_UNITS_FACTOR_AREA_ORDER = 0.75	--default^			-- Factor for desired number of units to assign to area defense orders
NDefines.NAI.MIN_UNITS_FACTOR_AREA_ORDER = 0.5	--default^^				-- Factor for min number of units to assign to area defense orders

NDefines.NAI.MAX_UNITS_FACTOR_FRONT_ORDER = 3.0	--default 1.5			-- Factor for max number of units to assign to area front orders
NDefines.NAI.DESIRED_UNITS_FACTOR_FRONT_ORDER = 3.0	--default ^			-- Factor for desired number of units to assign to area front orders
NDefines.NAI.MIN_UNITS_FACTOR_FRONT_ORDER = 2.0	--default 1.0			-- Factor for min number of units to assign to area front orders

NDefines.NAI.MAX_UNITS_FACTOR_INVASION_ORDER = 1.0	--default 1.0	-- Factor for max number of units to assign to naval invasion orders
NDefines.NAI.DESIRED_UNITS_FACTOR_INVASION_ORDER = 1.0	--default ^		-- Factor for desired number of units to assign to naval invasion orders
NDefines.NAI.MIN_UNITS_FACTOR_INVASION_ORDER = 1.0	--default ^^			-- Factor for min number of units to assign to naval invasion orders

NDefines.NAI.FRONT_UNITS_CAP_FACTOR = 10.0 ----15.0 mad test here too 		--default 15.0				-- A factor applied to total front size and supply use. Primarily effects small fronts
NDefines.NAI.MAX_DIST_PORT_RUSH = 25.0	--default 20.0			-- If a unit is in enemy territory with no supply it will consider nearby ports within this distance.
	
NDefines.NAI.MIN_FIELD_STRENGTH_TO_BUILD_UNITS = 0.7	--default 0.7		-- Cancel unit production if below this to get resources out to units in the field
NDefines.NAI.MIN_MANPOWER_TO_BUILD_UNITS = 0.7	--default 0.7				-- Cancel unit production if below this to get resources out to units in the field

NDefines.NMilitary.PLAN_SPREAD_ATTACK_WEIGHT = 300-- 1.0 -- (was 12.0)	-- The higher the value, the less it should crowd provinces with multiple attacks.		#WICHTIG
NDefines.NMilitary.PLAN_MIN_AUTOMATED_EMPTY_POCKET_SIZE = 20		-- (was 2) -- The battle plan system will only automatically attack provinces in pockets that has no resistance and are no bigger than these many provinces

NDefines.NMilitary.FRONTLINE_EXPANSION_FACTOR = 0.0 -- #MOD was 0.0 remove if problematic -- was 0.6,				-- When attacking along a frontline, how much should units spread out as they advance. 0.0 means head (more or less) directly to the drawn frontline, with no distractions


-- AI Naval Air Management --

NDefines.NAI.NAVAL_STRIKE_PLANES_PER_SHIP = 40					-- Amount of bombers requested per enemy ship

NDefines.NAI.NAVAL_SHIP_AIR_IMPORTANCE = 10000 --2.0					-- Naval ship air importance
NDefines.NAI.NAVAL_IMPORTANCE_SCALE = 2 --0.65						-- Naval total importance scale (every naval score get's multiplied by it)

NDefines.NAI.NAVAL_PATROL_PLANES_PER_SHIP_PATROLLING = 20 --10.0		-- Amount of naval patrol planes per ship on a patrol mission
NDefines.NAI.NAVAL_PATROL_PLANES_PER_SHIP_RAIDING = 40 --10.0		-- Amount of naval patrol planes per ship on a convoy raid mission
NDefines.NAI.NAVAL_PATROL_PLANES_PER_SHIP_ESCORTING = 20 --10.0		-- Amount of naval patrol planes per ship on a convoy escort mission

-- AI Navy Management --

NDefines.NAI.ESTIMATED_CONVOYS_PER_DIVISION = 18			-- Not always correct, but mainly used to make sure AI does not go crazy vanilla 6
NDefines.NAI.MAX_DISTANCE_NAVAL_INVASION = 100.0				-- AI is extremely unwilling to plan naval invasions above this naval distance limit. van 250 this value is multiplied by 15.92 I think for the actual km distance, aka 250 ='s almost 4k km.
NDefines.NAI.RESEARCH_NAVAL_DOCTRINE_NEED_GAIN_FACTOR = 0.075 -- Multiplies value based on relative naval industry size / country size.
NDefines.NAI.NAVAL_MISSION_INVASION_BASE = 30000					-- Base score for region with naval invasion (modified dynamically by prioritizing orders)

NDefines.NAI.MAX_SCREEN_TASKFORCES_FOR_CONVOY_DEFENSE_MIN = 0.40 --0.20 -- maximum ratio of all screen-ships forces to be used in convoy defense (increases up to max as AI loses convoys).
NDefines.NAI.MAX_SCREEN_TASKFORCES_FOR_CONVOY_DEFENSE_MAX = 0.60 --0.70 -- maximum ratio of all screen-ships forces to be used in convoy defense (increases up to max as AI loses convoys).

NDefines.NAI.MAX_SCREEN_TASKFORCES_FOR_CONVOY_DEFENSE_MAX_CONVOY_THREAT = 500 -- 1500 -- AI will increase screen assignment for escort missions as threate increases

NDefines.NAI.HIGH_PRIO_NAVAL_MISSION_SCORES = {  -- priorities for regions to get assigned to a mission
	0, -- HOLD (consumes fuel HOLD_MISSION_MOVEMENT_COST fuel while moving)
	3800, -- PATROL - 100000	
	1000, -- STRIKE FORCE 
	4000, -- CONVOY RAIDING ---test to see if UK block Ethiopia was 1500
	3000, -- CONVOY ESCORT - 1000
	600, -- MINES PLANTING	
	300, -- MINES SWEEPING	
	0, -- TRAIN
	0, -- RESERVE_FLEET
	1000, -- NAVAL INVASION SUPPORT
}

NDefines.NAI.MAX_MISSION_PER_TASKFORCE = {  -- max mission region/taskforce ratio
	0, -- HOLD (consumes fuel HOLD_MISSION_MOVEMENT_COST fuel while moving)
	1.5, -- PATROL
	6, -- STRIKE FORCE
	6, -- CONVOY RAIDING
	4, -- CONVOY ESCORT
	2, -- MINES PLANTING
	2, -- MINES SWEEPING
	0, -- TRAIN
	0, -- RESERVE_FLEET
	10, -- NAVAL INVASION SUPPORT
}

NDefines.NAI.CAPITAL_TASKFORCE_MAX_CAPITAL_COUNT = 6 		-- optimum capital count for capital taskforces
NDefines.NAI.SCREEN_TASKFORCE_MAX_SHIP_COUNT = 8			-- optimum screen count for screen taskforces
NDefines.NAI.SUB_TASKFORCE_MAX_SHIP_COUNT = 10 				-- optimum sub count for sub taskforces

NDefines.NAI.MAX_SCREEN_TASKFORCES_FOR_MINE_SWEEPING = 0.10 -- maximum ratio of screens forces to be used in mine sweeping
NDefines.NAI.MAX_SCREEN_TASKFORCES_FOR_MINE_SWEEPING_PRIO_MAX_MINES = 250 -- highest mines for highest prio for mine missions
NDefines.NAI.MAX_SCREEN_TASKFORCES_FOR_MINE_LAYING = 0.05 -- maximum ratio of screens forces to be used in mine laying

-- AI Air Management --

NDefines.NAI.STR_BOMB_PLANES_PER_CIV_FACTORY = 200				-- Amount of planes requested per enemy civ factory
NDefines.NAI.STR_BOMB_PLANES_PER_MIL_FACTORY = 205				-- Amount of planes requested per enemy military factory
NDefines.NAI.STR_BOMB_PLANES_PER_NAV_FACTORY = 105				-- Amount of planes requested per enemy naval factory
NDefines.NAI.STR_BOMB_PLANES_PER_SUPPLY_HUB = 30                 -- Amount of planes requested per enemy supply node
NDefines.NAI.STR_BOMB_MIN_EXCORT_PLANES = 200					-- Min amount of planes requested to excort operations

-- AI Defense --

NDefines.NAI.LAND_DEFENSE_FIGHERS_PER_PLANE = 1				-- Amount of air superiority planes requested per enemy plane
NDefines.NAI.LAND_DEFENSE_INTERSEPTORS_PER_BOMBERS = 1		-- Amount of air interceptor planes requested per enemy bomber

NDefines.NAI.LAND_DEFENSE_CIVIL_FACTORY_IMPORTANCE = 800 -- 50			-- Strategic importance of civil factories
NDefines.NAI.LAND_DEFENSE_MILITARY_FACTORY_IMPORTANCE = 880 -- 70		-- Strategic importance of military factories
NDefines.NAI.LAND_DEFENSE_NAVAL_FACTORY_IMPORTANCE = 420 -- 30			-- Strategic importance of naval factories

-- AI Generic Defines --

NDefines.NAI.NAVY_PREFERED_MAX_SIZE = 1000		-- AI will generally attempt to merge fleets into this size, but as a soft limit.
NDefines.NAI.MAX_MICRO_ATTACKS_PER_ORDER = 3 -- AI goes through its orders and checks if there are situations to take advantage of

-- AI Researchs --

NDefines.NAI.MAX_AHEAD_RESEARCH_PENALTY = 10

-- AI Construction --

NDefines.NAI.BUILDING_TARGETS_BUILDING_PRIORITIES = { -- buildings in order of pirority when considering building targets strategies. First has the greatest priority, omitted has the lowest. NOTE: not all buildings are supported by building targets strategies.
	'infrastructure',
	'rubber_refinery',
	
	-- Synthetic Resources but Rubber --
	
	'aluminium_mill',
	'chromium_mill',
	'tungsten_mill',
	'steel_mill',
	
	'synthetic_refinery',
	'fuel_silo',
	
	-- Factories --
	
	'arms_factory',
	'dockyard',
	'industrial_complex',
}

-- AI XP Spend Priorities --

NDefines.NAI.DESIRE_USE_XP_TO_UNLOCK_LAND_DOCTRINE = 1.0     -- How quickly is desire to unlock land doctrines accumulated?
NDefines.NAI.DESIRE_USE_XP_TO_UNLOCK_NAVAL_DOCTRINE = 1.0    -- How quickly is desire to unlock naval doctrines accumulated?
NDefines.NAI.DESIRE_USE_XP_TO_UNLOCK_AIR_DOCTRINE = 1.0      -- How quickly is desire to unlock air doctrines accumulated?

NDefines.NAI.DESIRE_USE_XP_TO_UPDATE_LAND_TEMPLATE = 1000.0    -- How quickly is desire to update/create templates accumulated?

NDefines.NAI.DESIRE_USE_XP_TO_UPGRADE_LAND_EQUIPMENT = 100.0  -- How quickly is desire to update/create land equipment variants accumulated?
NDefines.NAI.DESIRE_USE_XP_TO_UPGRADE_NAVAL_EQUIPMENT = 100.0 -- How quickly is desire to update/create naval equipment variants accumulated?
NDefines.NAI.DESIRE_USE_XP_TO_UPGRADE_AIR_EQUIPMENT = 100.0   -- How quickly is desire to update/create air equipment variants accumulated?

NDefines.NAI.DESIRE_USE_XP_TO_UNLOCK_ARMY_SPIRIT = 10.0      -- How quickly is desire to unlock army spirits accumulated?
NDefines.NAI.DESIRE_USE_XP_TO_UNLOCK_NAVY_SPIRIT =  10.0     -- How quickly is desire to unlock naval spirits accumulated?
NDefines.NAI.DESIRE_USE_XP_TO_UNLOCK_AIR_SPIRIT = 10.0       -- How quickly is desire to unlock air spirits accumulated?

-- From Summer Beta (its up to paradox so never forget these to remove if they remove too)

NDefines.NAI.UPGRADES_DEFICIT_LIMIT_DAYS = 180

-- AI Diplomacy --

NDefines.NAI.DIPLOMACY_ACCEPT_ATTACHE_BASE = 100
NDefines.NAI.DIPLOMACY_ACCEPT_ATTACHE_OPINION_PENALTY = 0

-- AI Generic Defines --

NDefines.NAI.DEPLOY_MIN_TRAINING_PEACE_FACTOR = 0.10   -- Required percentage of training (1.0 = 100%) for AI to deploy unit in peacetime
NDefines.NAI.DEPLOY_MIN_EQUIPMENT_PEACE_FACTOR = 0.75  -- Required percentage of equipment (1.0 = 100%) for AI to deploy unit in peacetime
