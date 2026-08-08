

DEFAULT_SPEED = 60
DEFAULT_DEAD_SPEED = 50
DEFAULT_SPRINT_SPEED = 70
DEFAULT_ACCEL = 1

import time
from visualizer import *
from tracklist import *

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
        acceleration=self._get_acceleration(runner)
        target_speed=self._get_base_speed(runner)
        target_speed=self._get_corner_target(runner,target_speed,acceleration)
        target_speed=self._smooth_target_speed(runner,target_speed,dt)
        self._update_current_speed(runner,target_speed,acceleration,dt)
        self._update_hp(runner,dt)
        return runner.current_speed

    def _get_base_speed(self,runner):
        if runner.hp<=0:
            return DEFAULT_DEAD_SPEED+runner.speed/1000

        normal_speed=DEFAULT_SPEED*0.9+(runner.speed/20)*0.1
        sprint_speed=DEFAULT_SPRINT_SPEED*0.5+(runner.speed/20)*0.5

        if runner.distance>=self.circuit.length*2/3:
            return sprint_speed

        return normal_speed

    def _get_acceleration(self,runner):
        return DEFAULT_ACCEL*runner.power/1000

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

    def _update_hp(self,runner,dt):
        runner.hp=max(0,runner.hp-(runner.current_speed/1200*120)*dt)
