

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

UPHILL_SPEED_FACTOR = -0.1
UPHILL_ACCEL_FACTOR = -0.2
UPHILL_HP_FACTOR = 0.1
DOWNHILL_SPEED_FACTOR = 0.05
DOWNHILL_ACCEL_FACTOR = 0.1
DOWNHILL_HP_FACTOR = -0.2

MAX_EQUALIZED_SPEED = 40

FR_HP_FACTOR = 1.15
FR_START_ACCEL_FACTOR =1.2
FR_TARGET_SPEED_1=1.000
FR_TARGET_SPEED_2=1.001
FR_TARGET_FAILED=0.95
FR_SPRINT_SPEED_FACTOR = 0.995


PC_HP_FACTOR = 1.05
PC_START_ACCEL_FACTOR = 1.05
PC_TARGET_SPEED_1= 0.999
PC_TARGET_SPEED_2= 1.000
PC_TARGET_SPEED_3= 1.001
PC_SPRINT_SPEED_FACTOR = 1

LS_HP_FACTOR = 0.95
LS_START_ACCEL_FACTOR = 0.98
LS_TARGET_SPEED_1= 0.999
LS_TARGET_SPEED_2= 1.000
LS_TARGET_SPEED_3= 1.001
LS_SPRINT_SPEED_FACTOR = 1.005

EC_HP_FACTOR = 0.85
EC_START_ACCEL_FACTOR = 0.90
EC_TARGET_SPEED_1= 0.999
EC_TARGET_SPEED_2= 1.000
EC_SPRINT_SPEED_FACTOR = 1.01







class Course:
    def __init__(self,circuit,conditions,runners):
        self.circuit=circuit
        self.conditions=conditions
        self.runners=runners
        self.finished=False
   
        self.time=0
        self.results=[]
        builder=TrackBuilder()
        self.track=builder.build(circuit)

    def step(self,dt):
        self.update(dt)
        self.checkfinish()

    def checkfinish(self): 
        if len(self.results)==len(self.runners):
            self.finished=True

    def update(self,dt):
        self.time+=dt


        for runner in self.runners:
            if not runner.finished:
                runner.previous_distance = runner.distance

        ranking=sorted(self.runners,key=lambda r:r.distance,reverse=True)   
        for position, runner in enumerate(ranking, start=1):
            runner.position = position

        for runner in self.runners:
            if runner.finished:
                continue


            runner.update_skills(self, dt)
            current_speed=self.calculate_speed(runner,dt)
         



            speed_ms=current_speed/3.6
            runner.distance+=speed_ms*dt
            runner.track_index=min(int(runner.distance/STEP),len(self.track)-1)

            point=self.track[runner.track_index]
            runner.x=point.x
            runner.y=point.y

            if runner.distance>=self.circuit.length:
                runner.distance=self.circuit.length
                runner.finished=True
                self.results.append((len(self.results)+1,runner,self.time))

        self.update_overtakes()

        for runner in self.runners:

            if runner.finished:
                continue

            runner.update_skills(self, dt)

        
    def calculate_speed(self,runner,dt):

        target_speed,acceleration,hp_drain =self._get_base_speed(runner,dt)
        target_speed=self._get_corner_target(runner,target_speed,acceleration)
        target_speed=self._smooth_target_speed(runner,target_speed,dt)
        target_speed,acceleration, hp_drain = self._get_hill_target(runner,target_speed,acceleration,hp_drain)
        target_speed,acceleration, hp_drain = self._get_style_speed(runner,target_speed,acceleration,hp_drain)
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
            if runner.distance>=self.circuit.length*2/3:
                target_speed= sprint_speed
            else:
                target_speed=normal_speed
####Power=================================================================
        target_accel = base_accel
####Stamina ================================================================
        hp_drain=base_hp_drain
        
#############=============================================================
        for skill in runner.skills:

            if not skill.active:
                continue

            for effect in skill.effects:

                if isinstance(effect, Velocity):
                    target_speed = effect.skill_speed(target_speed)

                elif isinstance(effect, Acceleration):
                    target_accel = effect.skill_acceleration(target_accel)
        return (target_speed,target_accel,hp_drain)

    def _get_corner_target(self,runner,target_speed,acceleration):
        current_index=runner.track_index
        lookahead=150
        max_index=min(current_index+int(lookahead/STEP),len(self.track)-1)
        for i in range(current_index+1,max_index+1):
            curvature=abs(self.track[i].curvature)
            if curvature<=0:
                continue
            K=3.0
            corner_factor=max(0.6,1-K*curvature)
            corner_speed=target_speed*corner_factor
            distance=(i-current_index)*STEP
            acceleration_ms=acceleration/3.6
            corner_speed_ms=corner_speed/3.6
            if acceleration_ms<=0:
                return target_speed
            allowed_speed_ms=(corner_speed_ms**2+2*acceleration_ms*distance)**0.5
            allowed_speed=allowed_speed_ms*3.6
            return min(target_speed,allowed_speed)
        return target_speed

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
        length = self.circuit.length
        nb_runners = len(self.runners)


        if runner.style=="escape":
            pass

        if runner.style=="front":
            hp_drain*=FR_HP_FACTOR
            if runner.distance < length*30/100:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= FR_START_ACCEL_FACTOR

            elif runner.distance > length*(MID_RACE) and runner.distance< length*(LATE_RACE):
                if runner.name=="Strid":
                    print(runner.position)
                if runner.position == 1:
                    target_speed *= FR_TARGET_SPEED_1 #FR -> Front Runner
                elif runner.position >= 1 and runner.position <= 4:
                    target_speed *= FR_TARGET_SPEED_2
                elif runner.position >= 5:
                    target_speed *= FR_TARGET_FAILED 

            elif runner.distance >= length*(LATE_RACE):
                target_speed = target_speed*FR_SPRINT_SPEED_FACTOR
            
        if runner.style=="pace":
          
            hp_drain *= PC_HP_FACTOR

            # Début : économie d'énergie
            if runner.distance < length*30/100:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= PC_START_ACCEL_FACTOR

            # Milieu : accélération progressive
            elif runner.distance > length * MID_RACE and runner.distance < length * LATE_RACE:
                if runner.position <=  nb_runners*0.15 :
                    target_speed *= PC_TARGET_SPEED_1
                elif runner.position <= nb_runners*0.5 and runner.position > nb_runners*0.15:
                    target_speed *= PC_TARGET_SPEED_2
                elif runner.position > nb_runners > 0.5:
                    target_speed *= PC_TARGET_SPEED_3

            # Fin : sprint modéré
            elif runner.distance >= length * LATE_RACE:
                target_speed *= PC_SPRINT_SPEED_FACTOR









        if runner.style=="late":
            hp_drain *= LS_HP_FACTOR
            if runner.distance < length*30/100:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= LS_START_ACCEL_FACTOR

            elif runner.distance > length * MID_RACE and runner.distance < length * LATE_RACE:
                if runner.position <=  nb_runners*0.5 :
                    target_speed *= LS_TARGET_SPEED_1
                elif runner.position >= nb_runners*0.5 and runner.position <= nb_runners*0.8:
                    target_speed *= LS_TARGET_SPEED_2
                elif runner.position > nb_runners > 0.8:
                    target_speed *= LS_TARGET_SPEED_3

            elif runner.distance >= length * LATE_RACE:
                target_speed *= LS_SPRINT_SPEED_FACTOR




        
        if runner.style=="end":
            hp_drain *= EC_HP_FACTOR
            if runner.distance < length*30/100:
                if runner.current_speed > MAX_EQUALIZED_SPEED and runner.current_speed < target_speed:
                    acceleration *= EC_START_ACCEL_FACTOR

            elif runner.distance < length * MID_RACE and runner.distance < length * LATE_RACE:
                if runner.position <=  nb_runners*0.8 :
                    target_speed *= EC_TARGET_SPEED_1
                elif runner.position >= nb_runners*0.8:
                    target_speed *= EC_TARGET_SPEED_2
            elif runner.distance >= length * LATE_RACE:
                target_speed *= EC_SPRINT_SPEED_FACTOR


        return (target_speed,acceleration,hp_drain)


    def _update_current_speed(self,runner,target_speed,acceleration,dt):
        if runner.current_speed<target_speed:

            accel_factor = acceleration * (1.04**abs(DEFAULT_SPRINT_SPEED-runner.current_speed))

            runner.current_speed=min(runner.current_speed+acceleration*accel_factor*dt,target_speed)
          
                
        else:
            runner.current_speed=max(runner.current_speed-acceleration*10*dt,target_speed)

    def _hp_drain(self,runner,hp_drain):
        runner.hp -= hp_drain
        runner.total_hp_drain = hp_drain

    def update_overtakes(self):
        for runner in self.runners:
            runner.overtakes_this_frame = 0

        for runner in self.runners:
            for other in self.runners:
                if runner is other:
                    continue

                was_behind = (
                    runner.previous_distance < other.previous_distance)
                is_now_ahead =(
                    runner.distance > other.distance
                )
                if was_behind and is_now_ahead:
                    runner.overtakes_this_frame +=1

                elif (
                runner.previous_distance > other.previous_distance
                and runner.distance < other.distance
                ):
                    runner.overtaken += 1
                    runner.overtaken_this_frame += 1