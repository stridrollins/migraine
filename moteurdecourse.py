

DEFAULT_SPEED = 60
DEFAULT_DEAD_SPEED = 50
DEFAULT_SPRINT_SPEED = 70
DEFAULT_ACCEL = 1
DEFAULT_HP_DRAIN = 0.1

UPHILL_SPEED_FACTOR = 1
UPHILL_ACCEL_FACTOR = 1
UPHILL_HP_FACTOR = 1
DOWNHILL_SPEED_FACTOR = 1
DOWNHILL_ACCEL_FACTOR = 1
DOWNHILL_HP_FACTOR = 1



import time
from visualizer import *
from tracklist import *
from runner import *

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

        ranking=sorted(self.runners,key=lambda r:r.distance,reverse=True)   

    def calculate_speed(self,runner,dt):

        target_speed,acceleration =self._get_base_speed(runner,dt)
        target_speed=self._get_corner_target(runner,target_speed,acceleration)



        target_speed=self._smooth_target_speed(runner,target_speed,dt)
        self._update_current_speed(runner,target_speed,acceleration,dt)
        
        return runner.current_speed

    def _get_base_speed(self,runner,dt):
###formules====================================================
        dead_speed = DEFAULT_DEAD_SPEED+runner.speed/1000
        sprint_speed= DEFAULT_SPRINT_SPEED*0.5+(runner.speed/20)*0.5
        normal_speed=DEFAULT_SPEED*0.9+(runner.speed/20)*0.1
        base_accel = DEFAULT_ACCEL*runner.power/1000
        base_hp_drain = max(0,runner.hp - (runner.current_speed*DEFAULT_HP_DRAIN)*dt - (runner.current_speed*runner.hp_drain)*dt)

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
        runner.hp=base_hp_drain
        
#############=============================================================
        for effect in runner.active_effects:
            if isinstance(effect,Velocity):
                target_speed = effect.skill_speed(target_speed)
            if isinstance(effect,Acceleration):
                target_accel = effect.skill_acceleration(target_accel)
            

            
        return (target_speed,target_accel)

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

    def _get_hill_target(self,runner,target_speed,acceleration):
        current_index = runner.track_index
        if self.track[current_index].gradient > 0:
            target_speed -= UPHILL_SPEED_FACTOR 
            acceleration -= UPHILL_ACCEL_FACTOR



    def _smooth_target_speed(self,runner,target_speed,dt):
        TARGET_SPEED_SMOOTHING=3.0
        runner.target_speed+=(target_speed-runner.target_speed)*TARGET_SPEED_SMOOTHING*dt
        return runner.target_speed

    def _update_current_speed(self,runner,target_speed,acceleration,dt):
        if runner.current_speed<target_speed:

            accel_factor = acceleration * (1.04**abs(DEFAULT_SPRINT_SPEED-runner.current_speed))

            runner.current_speed=min(runner.current_speed+acceleration*accel_factor*dt,target_speed)
          
                
        else:
            runner.current_speed=max(runner.current_speed-acceleration*10*dt,target_speed)

    def _get_hp_drain(self,runner,dt):
        runner.total_hp_drain = (runner.current_speed*DEFAULT_HP_DRAIN)*dt