#determiner si corner/uphill etc

if self.course.track[runner.track_index].curvature != 0:
    corner = True
else:
    corner = False