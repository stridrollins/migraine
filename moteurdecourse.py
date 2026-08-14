

from trackbuilder import *
from factories import *
from runner import *
from skills import *
EARLY_RACE = 0
MID_RACE = 1/3 
LATE_RACE = 2/3
LAST_SPURT = 5/6




DEFAULT_SPEED = 60
DEFAULT_DEAD_SPEED = 50
DEFAULT_SPRINT_SPEED = 70
DEFAULT_ACCEL = 1
DEFAULT_HP_DRAIN = 0.1


CURVATURE_SPEED_DRAIN=3.0
UPHILL_SPEED_FACTOR = -0.1
UPHILL_ACCEL_FACTOR = -0.2
UPHILL_HP_FACTOR = 0.1
DOWNHILL_SPEED_FACTOR = 0.05
DOWNHILL_ACCEL_FACTOR = 0.1
DOWNHILL_HP_FACTOR = -0.2

MAX_EQUALIZED_SPEED = 40


GE_HP_FACTOR = 1.35
GE_START_ACCEL_FACTOR =1.40
GE_TARGET_SPEED_1=1.040

GE_SPRINT_SPEED_FACTOR = 0.900



FR_HP_FACTOR = 1.15
FR_START_ACCEL_FACTOR =1.25
FR_TARGET_SPEED_1=1.000

FR_SPRINT_SPEED_FACTOR = 0.995


PC_HP_FACTOR = 1.05
PC_START_ACCEL_FACTOR = 1.10
PC_TARGET_SPEED_1= 1.000

PC_SPRINT_SPEED_FACTOR = 1

LS_HP_FACTOR = 0.95
LS_START_ACCEL_FACTOR = 1.00
LS_TARGET_SPEED_1= 0.999

LS_SPRINT_SPEED_FACTOR = 1.005

EC_HP_FACTOR = 0.85
EC_START_ACCEL_FACTOR = 0.90
EC_TARGET_SPEED_1= 0.999

EC_SPRINT_SPEED_FACTOR = 1.01






class Course:
    def __init__(self,circuit,conditions,runners):
        self.circuit=circuit
        self.conditions=conditions
        self.runners=runners
        self.runner_count = len(runners)
        self.finished=False
        
        self.time=0
        self.results=[]
        builder=TrackBuilder()
        self.track=builder.build(circuit)
###### marqueurs de circuit
        self.track_last_index = len(self.track) - 1
        self.length = circuit.length
        self.mid_race = self.length*MID_RACE
        self.late_race = self.length*LATE_RACE
        self.last_spurt = self.length*LAST_SPURT

######## marqueurs de position 
        self.pos0 = self.runner_count * 0
        self.pos5 = self.runner_count *0.05
        self.pos15 = self.runner_count * 0.15
        self.pos30 = self.runner_count * 0.3
        self.pos50 = self.runner_count * 0.5
        self.pos65 = self.runner_count * 0.65
        self.pos75 = self.runner_count * 0.75
        self.pos80 = self.runner_count *0.8
        self.pos100 = self.runner_count






###########corner_target_bullshit
        self.track_last_index = len(self.track) - 1
        self.lookahead_steps = int(350 / STEP)
        self.next_corner = [-1] * len(self.track)
        next_corner = -1
        for i in range(self.track_last_index, -1, -1):
            if self.track[i].curvature != 0:
                next_corner = i
            self.next_corner[i] = next_corner

        self.corners = []
        for i, point in enumerate(self.track):
            if point.curvature != 0:
                if i==0 or self.track[i-1].curvature ==0:
                    self.corners.append(i)

        self.corner_points = []
        self.straightaway_points = []
        self.uphill_points = []
        self.downhill_points=[]
##Separer les corners des straight et uphill downhill pour les skills
        for i, point in enumerate(self.track):
            if point.curvature != 0:
                self.corner_points.append(i)
            else:
                self.straightaway_points.append(i)

            if point.gradient > 0 :
                self.uphill_points.append(i)
            elif point.gradient < 0 :
                self.downhill_points.append(i)



    def step(self,dt):
        self.update(dt)
        self.checkfinish()

    def checkfinish(self): 
        if len(self.results)==len(self.runners):
            self.finished=True



    def update(self,dt):
        self.time+=dt

        previous_positions = {
            runner: runner.position
            for runner in self.runners
        }

        for runner in self.runners:
            if not runner.finished:
                runner.previous_distance = runner.distance

        for runner in self.runners:
            if runner.finished:
                continue
            runner.update_skills(self, dt)
            current_speed=self.calculate_speed(runner,dt)
        

            speed_ms=current_speed/3.6
            runner.distance+=speed_ms*dt
            runner.track_index=min(int(runner.distance/STEP),self.track_last_index)

            point=self.track[runner.track_index]
            runner.x=point.x
            runner.y=point.y

            if runner.distance>=self.length:
                runner.distance=self.length
                runner.finished=True
                self.results.append((len(self.results)+1,runner,self.time))

        ranking = sorted(
            self.runners,
            key=lambda r: r.distance,
            reverse=True
        )

        for position, runner in enumerate(ranking, 1):
            old_position = previous_positions[runner]

            runner.position = position
            runner.overtakes_this_frame = max(0, old_position - position)
            runner.overtaken_this_frame = max(0, position - old_position)

            if runner.overtakes_this_frame:
                runner.overtakes += runner.overtakes_this_frame

            if runner.overtaken_this_frame:
                runner.overtaken += runner.overtaken_this_frame

        

        

        
    def calculate_speed(self,runner,dt):

        target_speed,acceleration,hp_drain =self._get_base_speed(runner,dt)
        target_speed,acceleration,hp_drain=self._get_natural_speed(runner,target_speed,acceleration,hp_drain)
        target_speed = self._get_skill_speed(runner,target_speed)

        target_speed=self._smooth_target_speed(runner,target_speed,dt)

        self._update_current_speed(runner,target_speed,acceleration,dt)
        self._hp_drain(runner,hp_drain)
        return runner.current_speed



    def _get_base_speed(self,runner,dt):
###formules====================================================
        dead_speed = DEFAULT_DEAD_SPEED+runner.speed/1000
        sprint_speed= DEFAULT_SPRINT_SPEED*0.5+(runner.speed/20)*0.5
        normal_speed=DEFAULT_SPEED*0.9+(runner.speed/20)*0.1
        base_accel = DEFAULT_ACCEL*runner.power/1000
        base_hp_drain = (runner.current_speed*DEFAULT_HP_DRAIN)*dt + (runner.current_speed*runner.hp_drain)*dt


####Speed===============================================================
        if runner.hp<=0:
            target_speed = dead_speed
        else:
            if runner.distance>=self.length*2/3:
                target_speed= sprint_speed
            else:
                target_speed=normal_speed

        return target_speed,base_accel,base_hp_drain

    def _get_natural_speed(self,runner,target_speed,acceleration,hp_drain):
        target_speed = self._get_corner_target(runner,target_speed,acceleration)
        target_speed,acceleration,hp_drain = self._get_hill_target(runner,target_speed,acceleration,hp_drain)
        target_speed,acceleration,hp_drain = self._get_style_speed(runner,target_speed,acceleration,hp_drain)
        return target_speed,acceleration,hp_drain





    def _get_corner_target(self,runner,target_speed,acceleration):
        current_index = runner.track_index
        corner_index = self.next_corner[current_index]
        if corner_index == -1:
            return target_speed
        if corner_index > current_index + self.lookahead_steps:
            return target_speed
        curvature = abs(self.track[corner_index].curvature)
        corner_factor = max(
            0.6,
            1 - CURVATURE_SPEED_DRAIN * curvature
        )
        corner_speed = target_speed * corner_factor
        distance = (corner_index - current_index) * STEP
        acceleration_ms = acceleration / 3.6
        corner_speed_ms = corner_speed / 3.6
        if acceleration_ms <= 0:
            return target_speed
        allowed_speed_ms = (
            corner_speed_ms ** 2
            + 2 * acceleration_ms * distance
        ) ** 0.5
        return min(target_speed, allowed_speed_ms * 3.6)

    def _get_hill_target(self,runner,target_speed,acceleration, hp_drain):
        
        hill = self.track[runner.track_index].gradient
        if hill > 0:
            target_speed = target_speed * (1+UPHILL_SPEED_FACTOR * hill)
            acceleration *= (1+UPHILL_ACCEL_FACTOR * hill)
            hp_drain *= (1+UPHILL_HP_FACTOR * hill)
        if hill < 0:
            target_speed *= (1+DOWNHILL_SPEED_FACTOR * -hill)
            acceleration *= (1+DOWNHILL_ACCEL_FACTOR *-hill)
            hp_drain *= (1+DOWNHILL_HP_FACTOR * -hill)
        return (target_speed,acceleration,hp_drain)

    def _smooth_target_speed(self,runner,target_speed,dt):
        TARGET_SPEED_SMOOTHING=3.0
        runner.target_speed+=(target_speed-runner.target_speed)*TARGET_SPEED_SMOOTHING*dt
        return runner.target_speed

    def _get_style_speed(self,runner,target_speed, acceleration,hp_drain):
    

        if runner.style=="escape":
            hp_drain*=GE_HP_FACTOR
            
            if runner.distance < self.late_race:
 
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= GE_START_ACCEL_FACTOR
            
                target_speed *= GE_TARGET_SPEED_1 #FR -> Front Runner

            elif runner.distance >= self.late_race:
                target_speed = target_speed*GE_SPRINT_SPEED_FACTOR
       



            
        if runner.style=="front":
            hp_drain*=FR_HP_FACTOR
            if runner.distance < self.late_race:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= FR_START_ACCEL_FACTOR
          
                target_speed *= FR_TARGET_SPEED_1 #FR -> Front Runner

            elif runner.distance >= self.late_race:
                target_speed = target_speed*FR_SPRINT_SPEED_FACTOR
            
        if runner.style=="pace":
            hp_drain *= PC_HP_FACTOR
            if runner.distance < self.late_race:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= PC_START_ACCEL_FACTOR
           
                target_speed *= PC_TARGET_SPEED_1
    
            elif runner.distance >= self.late_race:
                target_speed *= PC_SPRINT_SPEED_FACTOR

        if runner.style=="late":
            hp_drain *= LS_HP_FACTOR
            if runner.distance < self.late_race:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= LS_START_ACCEL_FACTOR

                target_speed *= LS_TARGET_SPEED_1

            elif runner.distance >= self.late_race:
                target_speed *= LS_SPRINT_SPEED_FACTOR

        if runner.style=="end":
            hp_drain *= EC_HP_FACTOR
            if runner.distance < self.late_race:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= EC_START_ACCEL_FACTOR
 
                target_speed *= EC_TARGET_SPEED_1

            elif runner.distance >= self.late_race:
                target_speed *= EC_SPRINT_SPEED_FACTOR

        return (target_speed,acceleration,hp_drain)

    def _update_current_speed(self,runner,target_speed,acceleration,dt):
        if runner.current_speed<target_speed:
            accel_factor = 1.04**abs(DEFAULT_SPRINT_SPEED - runner.current_speed)
            runner.current_speed=min(runner.current_speed+acceleration*accel_factor*dt,target_speed)         
        else:
            runner.current_speed=max(runner.current_speed-acceleration*10*dt,target_speed)

    def _hp_drain(self,runner,hp_drain):
        runner.hp -= hp_drain
        runner.total_hp_drain = hp_drain


    def _get_skill_speed(self, runner, target_speed):

        skill_bonus = 0

        for skill in runner.skills:

            if not skill.active:
                continue

            for effect in skill.effects:

                if isinstance(effect, Velocity):
                    skill_bonus += effect.amount

        return target_speed + skill_bonus

